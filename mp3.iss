[Setup]
AppName=YouTube Audio Downloader
AppVersion=1.0
DefaultDirName={pf}\YouTube Audio Downloader
DefaultGroupName=YouTube Audio Downloader
OutputDir=.
OutputBaseFilename=YouTubeAudioDownloaderSetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\mp3-downloader.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\YouTube Audio Downloader"; Filename: "{app}\mp3-downloader.exe"