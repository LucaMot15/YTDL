# YTDL — YouTube Downloader

A clean web UI for downloading YouTube videos and playlists, built with Python (Flask) + yt-dlp.

## Features
- ✅ Download single videos or full playlists
- ✅ MP4 video or MP3 audio
- ✅ Quality selection (best, 1080p, 720p, 480p, 360p)
- ✅ Real-time progress bar with speed & ETA
- ✅ Clean, dark-themed web interface

## Requirements

- Python 3.8+
- `ffmpeg` installed on your system (required for MP3 conversion and video merging)

### Install ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html and add to PATH.

## Setup

```bash
# 1. Clone / navigate to the project folder
cd yt-downloader

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Then open your browser at: **http://localhost:5000**

## Usage

1. Paste a YouTube video or playlist URL
2. Click **FETCH** to load video info
3. Choose **MP4** (video) or **MP3** (audio only)
4. Select quality (video only)
5. Click **DOWNLOAD** and watch the progress bar
6. Click **SAVE FILE** when done

## Project Structure

```
yt-downloader/
├── app.py              # Flask backend
├── requirements.txt    # Python dependencies
├── downloads/          # Downloaded files (auto-created)
└── templates/
    └── index.html      # Frontend UI
```

## Notes

- Downloaded files are saved to the `downloads/` folder and served for one-click saving.
- For production use, consider adding cleanup logic to remove old files from `downloads/`.
- yt-dlp is regularly updated to maintain YouTube compatibility — run `pip install -U yt-dlp` to update.
