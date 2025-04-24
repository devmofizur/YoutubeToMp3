import os
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
    install_package("yt-dlp")
    install_package("tqdm")
    ffmpeg_path = install_ffmpeg()  # Ensure FFmpeg is installed and return its path
    return ffmpeg_path


def find_ffmpeg_bin():
    """Locate ffmpeg.exe binary."""
    ffmpeg_base = os.path.join(os.getcwd(), "ffmpeg")
    for root, dirs, files in os.walk(ffmpeg_base):
        if "ffmpeg.exe" in files:
            return os.path.join(root, "ffmpeg.exe")
    return None


def download_youtube_as_mp3(video_url, download_folder, ffmpeg_path):
    try:
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        ydl_opts = {
            'format': 'bestaudio/best',  # You can also specify the video format if needed
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),  # Template for output file names
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'ffmpeg_location': ffmpeg_path  # Pass the ffmpeg location here (if needed)
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([video_url])
            
            if result == 0:  # If download is successful
                # Get the latest downloaded file (just the most recently created file)
                downloaded_files = os.listdir(download_folder)
                if downloaded_files:
                    latest_file = max([f for f in downloaded_files if os.path.isfile(os.path.join(download_folder, f))], key=lambda f: os.path.getctime(os.path.join(download_folder, f)))
                    
                    # Remove the existing extension and add ".mp3"
                    base_name = os.path.splitext(latest_file)[0]
                    new_file_name = base_name + ".mp3"
                    
                    # Rename the file to .mp3
                    os.rename(os.path.join(download_folder, latest_file), os.path.join(download_folder, new_file_name))
                    print(f"{Fore.GREEN}Renamed {latest_file} to {new_file_name}")

                print(f"{Fore.GREEN}Downloaded: {video_url}")
                return True  # Return success
            else:
                return False  # Return failure
    except Exception as e:
        print(f"{Fore.RED}Error downloading {video_url}: {e}")
        return False


def download_batch(links, download_folder, ffmpeg_path):
    completed, skipped = 0, 0
    total = len(links)

    with tqdm(total=total, desc="Downloading", unit="video", leave=True) as pbar:
        for link in links:
            link = link.strip()
            pbar.set_postfix_str(f"[{completed}/{total}] (Skipped: {skipped})")
            success = download_youtube_as_mp3(link, download_folder, ffmpeg_path)
            if success:
                completed += 1
            else:
                skipped += 1
            pbar.set_postfix_str(f"[{completed}/{total}] (Skipped: {skipped})")
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
    
    download_folder = r"Your download folder path"

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
