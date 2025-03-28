# YouTube MP3 Downloader (yt-dlp Version)

A GUI application to download YouTube audio as MP3 files using yt-dlp.

## Features
- Uses modern yt-dlp engine
- Built-in FFmpeg for reliable conversion
- Real-time progress tracking

## Installation

### For End Users
1. Download the latest `MP3DownloaderSetup.exe` from [Releases]
2. Run the installer and follow the prompts
3. Launch from Start Menu or Desktop shortcut

### For Developers
```bash
# Build installer yourself:
iscc mp3.iss
# Output will be in /output/MP3DownloaderSetup.exe
```

**Post-Installation**:
- The installer automatically adds:
  - Desktop shortcut (optional during install)
  - Start Menu entry
  - Uninstaller via Windows Apps

## Building from Source
```bash
# Install requirements
pip install yt-dlp pyinstaller

# Build executable
pyinstaller mp3-downloader.spec