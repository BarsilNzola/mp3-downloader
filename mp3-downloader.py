from pytube import YouTube
import os
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox

def download_audio():
    url = url_entry.get()
    destination = destination_entry.get() or '.'

    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        messagebox.showinfo("Success", f"{yt.title} has been successfully downloaded in .mp3 format.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_directory():
    folder = filedialog.askdirectory()
    destination_entry.delete(0, 'end')
    destination_entry.insert(0, folder)

# Create the main window
app = Tk()
app.title("YouTube Audio Downloader")

# URL input
Label(app, text="Enter YouTube URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = Entry(app, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Destination input
Label(app, text="Destination Folder:").grid(row=1, column=0, padx=10, pady=10)
destination_entry = Entry(app, width=50)
destination_entry.grid(row=1, column=1, padx=10, pady=10)
Button(app, text="Browse", command=browse_directory).grid(row=1, column=2, padx=10, pady=10)

# Download button
Button(app, text="Download", command=download_audio).grid(row=2, column=1, pady=20)

# Run the app
app.mainloop()