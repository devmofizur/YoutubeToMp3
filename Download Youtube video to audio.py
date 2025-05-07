import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
import yt_dlp
import time
from tqdm import tqdm
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

def install_package(package):
    """Install Python package silently."""
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}Error installing {package}. Please install manually.")
        sys.exit(1)


def install_ffmpeg():
    """Check if FFmpeg is installed globally."""
    try:
        # Check if ffmpeg is available in the system's PATH
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{Fore.GREEN}FFmpeg is already installed and accessible.")
    except FileNotFoundError:
        print(f"{Fore.YELLOW}FFmpeg not found, downloading...")
        ffmpeg_zip_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        zip_path = "ffmpeg.zip"
        ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")

        urllib.request.urlretrieve(ffmpeg_zip_url, zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_dir)

        os.remove(zip_path)
        print(f"{Fore.GREEN}FFmpeg downloaded and extracted to: {ffmpeg_dir}")
        
    return os.path.join(os.getcwd(), "ffmpeg", "bin", "ffmpeg.exe")


def install_dependencies():
    """Install required Python packages and FFmpeg."""
    print(f"{Fore.CYAN}Checking dependencies...")
    install_package("yt_dlp")
    install_package("tqdm")
    ffmpeg_path = install_ffmpeg()  # Ensure FFmpeg is installed and return its path
    return ffmpeg_path


def find_ffmpeg_bin():
    """Locate ffmpeg.exe in the global system PATH."""
    # Search for ffmpeg in directories listed in the system's PATH environment variable
    ffmpeg_bin = shutil.which("ffmpeg")

    if ffmpeg_bin:
        print(f"Found ffmpeg.exe at: {ffmpeg_bin}")  # Debugging print statement
        return ffmpeg_bin
    else:
        print("ffmpeg.exe not found in global PATH.")
        return None


def download_youtube_as_mp3(video_url, download_folder, ffmpeg_path):
    try:
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        ffmpeg_path = find_ffmpeg_bin()
        if ffmpeg_path is None:
            return False  # Can't proceed without ffmpeg

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'no_warnings': True,
            'ignoreerrors': True,
            'ffmpeg_location': ffmpeg_path
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return True  # Success
    except Exception:
        return False  # Failure


def extract_video_links_from_playlist(playlist_url):
    """Extract individual video URLs from a playlist"""
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': True,
            'no_warnings': True,
            'ignoreerrors': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(playlist_url, download=False)
            entries = info_dict.get('entries', [])
            video_urls = [entry['url'] for entry in entries if 'url' in entry]
            return video_urls
    except Exception:
        return []


def download_batch(links, download_folder, ffmpeg_path):
    print(f"Total Video : {links}")
    all_links = []

    # If it's a single playlist URL, extract actual video links
    if len(links) == 1 and "playlist" in links[0]:
        all_links = extract_video_links_from_playlist(links[0])
    else:
        all_links = links

    completed, skipped = 0, 0
    total = len(all_links)
    
    with tqdm(total=total, desc="Downloading", unit="video", ncols=80) as pbar:
        for idx, link in enumerate(all_links, 1):
            success = download_youtube_as_mp3(link.strip(), download_folder, ffmpeg_path)
            if success:
                completed += 1
            else:
                skipped += 1

            pbar.set_postfix_str(f"Complete : {completed} | Skip : {skipped}")
            pbar.update(1)

    input(f"{Fore.CYAN}Downloads complete. Press Enter to exit...")


def create_playlist_folder(base_download_folder):
    """Create a unique folder for the playlist."""
    n = 1
    while True:
        folder_name = f"playlist_{n}"
        playlist_folder = os.path.join(base_download_folder, folder_name)
        if not os.path.exists(playlist_folder):
            os.makedirs(playlist_folder)
            print(f"{Fore.GREEN}Playlist folder '{folder_name}' created successfully.")
            return playlist_folder
        n += 1


if __name__ == "__main__":
    ffmpeg_path = install_dependencies()  # This will install dependencies and FFmpeg
    
    current_path = os.getcwd()
    download_folder = os.path.join(current_path, "mp3")

    print(f"\n{Fore.CYAN}Choose download type:")
    print(f"{Fore.YELLOW}1. Download Single Video")
    print(f"{Fore.YELLOW}2. Download Playlist")
    print(f"{Fore.YELLOW}3. Download Multiple Videos (comma-separated URLs)")

    choice = input(f"{Fore.CYAN}Enter choice (1/2/3): ").strip()

    if choice == "1":
        url = input(f"{Fore.CYAN}Enter YouTube video URL: ").strip()
        download_batch([url], download_folder, ffmpeg_path)

    elif choice == "2":
        url = input(f"{Fore.CYAN}Enter YouTube playlist URL: ").strip()
        playlist_folder = create_playlist_folder(download_folder)
        download_batch([url], playlist_folder, ffmpeg_path)

    elif choice == "3":
        urls = input(f"{Fore.CYAN}Enter multiple YouTube video URLs separated by commas:\n").split(",")
        download_batch(urls, download_folder, ffmpeg_path)

    else:
        print(f"{Fore.RED}Invalid option. Exiting.")