# importing packages
from pytube import YouTube
import os

# url input from user
yt = Youtube(str(input("Enter the URL of the video you want to download: \n>>> ")))

#extract only audio