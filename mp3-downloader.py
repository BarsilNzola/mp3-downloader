from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError
import os
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox
import urllib.request
from time import sleep

# Patch pytube to avoid HTTP 4000 errors
def patch_pytube():
    # Set a smaller chunk size for downloads
    import pytube.request
    pytube.request.default_range_size = 1024 * 1024  # 1MB chunks
    
    # Add custom headers
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0'),
        ('Accept-Language', 'en-US,en;q=0.9'),
    ]
    urllib.request.install_opener(opener)

patch_pytube()

def download_audio():
    url = url_entry.get().strip()
    destination = destination_entry.get().strip() or '.'

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL!")
        return

    try:
        # Show "Downloading..." message
        status_label.config(text="Downloading...")
        app.update()  # Force UI update

        # Create YouTube object (removed timeout parameter)
        yt = YouTube(
            url,
            use_oauth=False,
            allow_oauth_cache=True
        )

        # Get audio stream (fallback method if filter fails)
        video = yt.streams.filter(only_audio=True).first()
        if not video:
            video = yt.streams.get_audio_only()

        # Download with retries
        max_retries = 3
        for attempt in range(max_retries):
            try:
                out_file = video.download(
                    output_path=destination,
                    skip_existing=False
                )
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                sleep(2)  # Wait before retrying

        # Convert to MP3
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        
        # Handle existing files
        if os.path.exists(new_file):
            os.remove(new_file)
            
        os.rename(out_file, new_file)
        
        messagebox.showinfo("Success", f"'{yt.title}' downloaded successfully!")
        status_label.config(text="Ready")

    except VideoUnavailable:
        messagebox.showerror("Error", "Video is unavailable or private")
    except RegexMatchError:
        messagebox.showerror("Error", "Invalid YouTube URL")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download:\n{str(e)}")
    finally:
        status_label.config(text="Ready")

def browse_directory():
    folder = filedialog.askdirectory()
    if folder:
        destination_entry.delete(0, 'end')
        destination_entry.insert(0, folder)

# Create the main window
app = Tk()
app.title("YouTube Audio Downloader")
app.resizable(False, False)

# URL input
Label(app, text="Enter YouTube URL:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
url_entry = Entry(app, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=5)

# Destination input
Label(app, text="Destination Folder:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
destination_entry = Entry(app, width=50)
destination_entry.grid(row=1, column=1, padx=10, pady=5)
Button(app, text="Browse", command=browse_directory).grid(row=1, column=2, padx=5, pady=5)

# Download button
Button(app, text="Download MP3", command=download_audio, width=15).grid(row=2, column=1, pady=10)

# Status label
status_label = Label(app, text="Ready", fg="blue")
status_label.grid(row=3, column=0, columnspan=3, pady=5)

# Run the app
app.mainloop()