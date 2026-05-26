<div align="center">

# 📥 YTDL

**A clean, fast web UI for downloading YouTube videos and playlists.**

Built with Python · Flask · yt-dlp

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-latest-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)

</div>

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎬 Video & Playlist | Download single videos or entire playlists |
| 🎵 MP4 / MP3 | Choose between video or audio-only output |
| 📊 Quality Selection | Best, 1080p, 720p, 480p, 360p |
| ⏱️ Live Progress | Real-time progress bar with speed & ETA |
| 🌙 Dark UI | Clean, dark-themed web interface |

---

## 🛠️ Requirements

- **Python** 3.8+
- **ffmpeg** — required for MP3 conversion and video merging

### Install ffmpeg

<details>
<summary><b>macOS</b></summary>

```bash
brew install ffmpeg
```
</details>

<details>
<summary><b>Ubuntu / Debian</b></summary>

```bash
sudo apt install ffmpeg
```
</details>

<details>
<summary><b>Windows</b></summary>

Download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html) and add to your system PATH.
</details>

---

## 🚀 Setup

```bash
# 1. Clone the repo
git clone https://github.com/LucaMot15/YTDL.git
cd YTDL

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Then open your browser at **[http://localhost:5000](http://localhost:5000)**

---

## 📖 Usage

1. Paste a YouTube video or playlist URL
2. Click **FETCH** to load video info
3. Choose **MP4** (video) or **MP3** (audio only)
4. Select a quality (video only)
5. Click **DOWNLOAD** and watch the progress bar
6. Click **SAVE FILE** when complete

---

## 📁 Project Structure

```
YTDL/
├── app.py              # Flask backend
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Frontend UI
└── downloads/          # Downloaded files (auto-created)
```

> **Note:** The `downloads/` folder is created automatically at runtime. For production use, consider adding cleanup logic to remove old files.

---

## 🔧 Keeping yt-dlp Updated

YouTube changes frequently. If downloads stop working, update yt-dlp:

```bash
pip install -U yt-dlp
```

---

## 📄 License

This project is open source. Feel free to fork and modify.
