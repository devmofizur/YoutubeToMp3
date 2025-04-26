import os
import yt_dlp
import subprocess
import platform

def download_mp4(video_url):
    # Create "YouTube_Video" folder in current directory
    download_folder = os.path.join(os.getcwd(), "YouTube_Video")
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'quiet': False,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    return download_folder

def open_folder(folder_path):
    system = platform.system()
    if system == "Windows":
        os.startfile(folder_path)
    elif system == "Darwin":  # macOS
        subprocess.Popen(["open", folder_path])
    else:  # Linux and others
        subprocess.Popen(["xdg-open", folder_path])

if __name__ == "__main__":
    video_link = input("Enter YouTube video link: ").strip()
    folder = download_mp4(video_link)
    print("\n✅ Download complete. Saved to 'YouTube_Video' folder.")
    open_folder(folder)
