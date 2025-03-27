import os
import time
import threading
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, ttk, StringVar
from tkinter.font import Font
import yt_dlp

# Set the local FFmpeg path (ensure ffmpeg.exe is in the same folder as this script)
ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg", "ffmpeg.exe")

# ===== MAIN APPLICATION =====
class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Audio Downloader")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        # Custom font
        self.font = Font(family="Segoe UI", size=10)
        self.bold_font = Font(family="Segoe UI", size=10, weight="bold")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TButton', font=self.font, padding=6)
        self.style.configure('TEntry', padding=5)
        self.style.configure('TLabel', font=self.font)
        
        # Variables
        self.download_speed = StringVar()
        self.download_speed.set("")
        self.status_text = StringVar()
        self.status_text.set("Ready")
        
        # UI Elements
        self.setup_ui()
        
    def setup_ui(self):
        header = Label(self.root, text="YouTube to MP3 Downloader", font=("Segoe UI", 14, "bold"))
        header.pack(pady=(10, 20))
        
        url_frame = ttk.Frame(self.root)
        url_frame.pack(fill="x", padx=20, pady=5)
        
        ttk.Label(url_frame, text="YouTube URL:").pack(side="left")
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(side="left", padx=10, expand=True, fill="x")
        
        dest_frame = ttk.Frame(self.root)
        dest_frame.pack(fill="x", padx=20, pady=5)
        
        ttk.Label(dest_frame, text="Save to:").pack(side="left")
        self.dest_entry = ttk.Entry(dest_frame, width=40)
        self.dest_entry.pack(side="left", padx=10, expand=True, fill="x")
        
        browse_btn = ttk.Button(dest_frame, text="Browse", command=self.browse_directory)
        browse_btn.pack(side="left")
        
        download_btn = ttk.Button(self.root, text="Download MP3", command=self.start_download)
        download_btn.pack(pady=15)
        
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=5)
        
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(fill="x", padx=20)
        
        ttk.Label(progress_frame, textvariable=self.download_speed).pack(side="left")
        ttk.Label(progress_frame, textvariable=self.status_text).pack(side="right")
    
    def browse_directory(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_entry.delete(0, 'end')
            self.dest_entry.insert(0, folder)
    
    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL!")
            return
            
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button) and widget['text'] == "Download MP3":
                widget.config(state='disabled')
                break
        
        threading.Thread(target=self.download_audio, daemon=True).start()
    
    def download_audio(self):
        url = self.url_entry.get().strip()
        destination = self.dest_entry.get().strip() or '.'
        
        self.status_text.set("Downloading...")
        self.root.update()
        
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(destination, '%(title)s.%(ext)s'),
                'ffmpeg_location': ffmpeg_path,  # 👈 Specify the local ffmpeg path
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [self.progress_hook],
                'quiet': True,  # 👈 Hides CLI output
                'noprogress': True  # 👈 Prevents yt-dlp from printing its own progress
            }

            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            self.status_text.set("Download complete!")
            messagebox.showinfo("Success", "Download completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download:\n{str(e)}")
        finally:
            self.progress['value'] = 0
            self.download_speed.set("")
            
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.Button) and widget['text'] == "Download MP3":
                    widget.config(state='normal')
                    break
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '0.0%').strip('%')
            
            # Ensure percent_str contains a valid number before conversion
            try:
                percent = float(percent_str)
                self.progress['value'] = percent
                self.status_text.set(f"Downloading: {percent:.2f}%")
            except ValueError:
                self.status_text.set("Downloading...")

            self.root.update_idletasks()

        elif d['status'] == 'finished':
            self.progress['value'] = 100
            self.status_text.set("Processing audio...")
            self.root.update_idletasks()

if __name__ == "__main__":
    root = Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
