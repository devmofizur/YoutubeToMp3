# YouTube Video to MP3 Downloader

This Python script allows you to download YouTube videos as MP3 files. The script supports downloading single videos, playlists, and multiple videos using YouTube URLs. It also ensures the downloaded files are properly named and converted to MP3 format.

## Features

- Download single YouTube videos as MP3.
- Download YouTube playlists as MP3 files.
- Batch download multiple videos (comma-separated URLs).
- Automatically handles FFmpeg for video conversion (if required).
- Simple and interactive command-line interface.

---

## Requirements

- Python 3.x (preferably Python 3.7 or above)
- `yt-dlp` (YouTube downloader)
- `FFmpeg` (for video processing)
- `tqdm` (for showing download progress)

---

## Installation Guide

### Step 1: Install Python

Make sure you have **Python 3.x** installed on your system. You can download it from the official website: [Python Downloads](https://www.python.org/downloads/).

To check if Python is installed correctly, run the following command in your terminal:

```bash
python --version

Step 2: Install Required Packages
To install the necessary Python dependencies, open a terminal (or command prompt) and run the following command:

bash
Copy
Edit
pip install -r requirements.txt
This will install the following required packages:

yt-dlp: A YouTube video downloader (replacement for youtube-dl).

tqdm: A library for displaying download progress.

Alternatively, you can install them manually:

bash
Copy
Edit
pip install yt-dlp tqdm
Step 3: Install FFmpeg (Video Processing)
FFmpeg is required to process and convert video files to MP3 format. If FFmpeg is not already installed on your system, follow these steps to download and install it:

For Windows:
Download the latest FFmpeg release from FFmpeg Official Site.

Extract the contents of the downloaded ZIP file.

Add the bin folder (where ffmpeg.exe is located) to your system's PATH environment variable:

Open System Properties > Advanced > Environment Variables.

Under System Variables, find the Path variable and click Edit.

Add the full path to the bin folder (e.g., C:\ffmpeg\bin).

Verify FFmpeg installation by running the following command in your terminal:

bash
Copy
Edit
ffmpeg -version
For macOS:
bash
Copy
Edit
brew install ffmpeg
For Linux:
bash
Copy
Edit
sudo apt update
sudo apt install ffmpeg
Step 4: Verify Dependencies
Once you have installed the dependencies, you can check if the necessary tools are properly installed by running the following commands:

bash
Copy
Edit
yt-dlp --version
ffmpeg -version
Both commands should return their respective version numbers.

How to Use the Script
Clone the repository (if you haven't already):

bash
Copy
Edit
git clone https://github.com/devmofizur/YoutubeToMp3.git
cd YoutubeToMp3
Set Your Download Folder Path:

In the script file Download Youtube video to audio.py, you will need to set the download_folder variable to your desired download folder path.

python
Copy
Edit
download_folder = r"Your download folder path"
Run the script:

To start the downloader script, execute the following command:

bash
Copy
Edit
python "Download Youtube video to audio.py"
Choose download type:

After running the script, you will be prompted to choose the download type:

1: Download a single YouTube video as MP3.

2: Download a YouTube playlist as MP3.

3: Download multiple YouTube videos (comma-separated URLs).

Enter the option number and follow the on-screen prompts to provide the YouTube URL(s).

Download Progress:

While downloading, you will see a progress bar indicating the download progress, including the percentage and estimated time remaining.

