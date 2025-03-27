; -- mp3.iss --
[Setup]
AppName=MP3 Downloader
AppVersion=1.0
AppPublisher=TheForeverKnights
DefaultDirName={autopf}\MP3 Downloader
DefaultGroupName=MP3 Downloader
OutputDir=output
OutputBaseFilename=MP3DownloaderSetup
Compression=lzma2/ultra
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
SetupIconFile=icon.ico
WizardStyle=modern
VersionInfoVersion=1.0.0
VersionInfoCompany=TheForeverKnights

[Files]
; Define Python Path
#define PythonPath GetEnv("LOCALAPPDATA") + "\Programs\Python\Python313"
; FFmpeg and FFprobe binaries
; Include FFmpeg in the installation
Source: "dist\ffmpeg\*"; DestDir: "{app}\ffmpeg"; Flags: recursesubdirs


; Main executable
Source: ".\dist\mp3-downloader.exe"; DestDir: "{app}"; Flags: ignoreversion

; Tcl/Tk files
Source: "{#PythonPath}\tcl\*"; DestDir: "{app}\tcl"; Flags: recursesubdirs

; Optional icon
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\MP3 Downloader"; Filename: "{app}\mp3-downloader.exe"; IconFilename: "{app}\icon.ico"
Name: "{autodesktop}\MP3 Downloader"; Filename: "{app}\mp3-downloader.exe"; IconFilename: "{app}\icon.ico"

[Run]
Filename: "{app}\mp3-downloader.exe"; Description: "Run MP3 Downloader"; Flags: nowait postinstall skipifsilent
