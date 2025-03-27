# YouTube MP3 Downloader (yt-dlp Version)

A GUI application to download YouTube audio as MP3 files using yt-dlp.

## Features
- Uses modern yt-dlp engine
- Built-in FFmpeg for reliable conversion
- Real-time progress tracking

## Installation
1. Download the latest release
2. Run `MP3DownloaderSetup.exe`
3. The app includes its own FFmpeg - no separate installation needed

## Building from Source
```bash
# Install requirements
pip install yt-dlp pyinstaller

# Build executable
pyinstaller mp3-downloader.spec