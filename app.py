import os
import json
import threading
import uuid
from flask import Flask, request, jsonify, send_file, render_template, Response
import yt_dlp

app = Flask(__name__)

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# In-memory job store: job_id -> progress info
jobs = {}


def make_progress_hook(job_id):
    def hook(d):
        job = jobs.get(job_id, {})
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded = d.get("downloaded_bytes", 0)
            percent = (downloaded / total * 100) if total else 0
            speed = d.get("speed") or 0
            eta = d.get("eta") or 0
            jobs[job_id] = {
                **job,
                "status": "downloading",
                "percent": round(percent, 1),
                "speed": format_bytes(speed) + "/s" if speed else "—",
                "eta": format_eta(eta),
                "filename": d.get("filename", ""),
            }
        elif d["status"] == "finished":
            jobs[job_id] = {
                **job,
                "status": "processing",
                "percent": 99,
                "speed": "—",
                "eta": "Almost done…",
                "filename": d.get("filename", ""),
            }
        elif d["status"] == "error":
            jobs[job_id] = {**job, "status": "error", "error": str(d.get("error", "Unknown error"))}
    return hook


def format_bytes(b):
    if b < 1024:
        return f"{b:.0f} B"
    elif b < 1024 ** 2:
        return f"{b/1024:.1f} KB"
    elif b < 1024 ** 3:
        return f"{b/1024**2:.1f} MB"
    return f"{b/1024**3:.2f} GB"


def format_eta(seconds):
    if not seconds:
        return "—"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h {m}m {s}s"
    elif m:
        return f"{m}m {s}s"
    return f"{s}s"


def run_download(job_id, url, fmt, quality):
    job = jobs[job_id]
    out_tmpl = os.path.join(DOWNLOAD_DIR, f"{job_id}_%(title)s.%(ext)s")

    if fmt == "mp3":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": out_tmpl,
            "progress_hooks": [make_progress_hook(job_id)],
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "quiet": True,
        }
    else:
        quality_map = {
            "best": "bestvideo+bestaudio/best",
            "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
            "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
        }
        ydl_opts = {
            "format": quality_map.get(quality, "bestvideo+bestaudio/best"),
            "outtmpl": out_tmpl,
            "progress_hooks": [make_progress_hook(job_id)],
            "merge_output_format": "mp4",
            "quiet": True,
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # Find the actual output file
            files = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith(job_id)]
            if files:
                final_file = os.path.join(DOWNLOAD_DIR, files[0])
                jobs[job_id] = {
                    **jobs[job_id],
                    "status": "done",
                    "percent": 100,
                    "eta": "Done!",
                    "speed": "—",
                    "file": final_file,
                    "title": info.get("title", "download"),
                }
            else:
                jobs[job_id] = {**jobs[job_id], "status": "error", "error": "Output file not found"}
    except Exception as e:
        jobs[job_id] = {**jobs[job_id], "status": "error", "error": str(e)}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/info", methods=["POST"])
def get_info():
    data = request.json
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    try:
        with yt_dlp.YoutubeDL({"quiet": True, "noplaylist": False}) as ydl:
            info = ydl.extract_info(url, download=False)
        is_playlist = info.get("_type") == "playlist"
        if is_playlist:
            entries = info.get("entries", [])
            return jsonify({
                "type": "playlist",
                "title": info.get("title", "Playlist"),
                "count": len(entries),
                "thumbnail": entries[0].get("thumbnail") if entries else None,
            })
        else:
            formats = info.get("formats", [])
            heights = sorted(set(
                f["height"] for f in formats if f.get("height") and f.get("vcodec") != "none"
            ), reverse=True)
            return jsonify({
                "type": "video",
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "channel": info.get("channel") or info.get("uploader"),
                "available_qualities": heights,
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/download", methods=["POST"])
def start_download():
    data = request.json
    url = data.get("url", "").strip()
    fmt = data.get("format", "mp4")
    quality = data.get("quality", "best")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {"status": "starting", "percent": 0, "speed": "—", "eta": "—"}

    thread = threading.Thread(target=run_download, args=(job_id, url, fmt, quality), daemon=True)
    thread.start()

    return jsonify({"job_id": job_id})


@app.route("/api/progress/<job_id>")
def progress(job_id):
    def stream():
        import time
        while True:
            job = jobs.get(job_id)
            if not job:
                yield f"data: {json.dumps({'status': 'not_found'})}\n\n"
                break
            yield f"data: {json.dumps(job)}\n\n"
            if job["status"] in ("done", "error"):
                break
            time.sleep(0.5)
    return Response(stream(), mimetype="text/event-stream")


@app.route("/api/download-file/<job_id>")
def download_file(job_id):
    job = jobs.get(job_id)
    if not job or job.get("status") != "done":
        return jsonify({"error": "File not ready"}), 404
    filepath = job.get("file")
    if not filepath or not os.path.exists(filepath):
        return jsonify({"error": "File missing"}), 404
    title = job.get("title", "download")
    ext = os.path.splitext(filepath)[1]
    return send_file(filepath, as_attachment=True, download_name=f"{title}{ext}")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
