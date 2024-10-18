import os
import subprocess
import threading
import glob
import time
from concurrent.futures import ThreadPoolExecutor

# Directories for storing video chunks and m3u8 files
VIDEO_OUTPUT = "app/media/chunks"
PLAYLIST_OUTPUT = "app/media/playlists"
PLAYLIST_FILE = f"{PLAYLIST_OUTPUT}/playlist.m3u8"

# Set up an executor for background tasks
executor = ThreadPoolExecutor(max_workers=1)

# Sets up the directory structure if it doesn't exist
def setup_media_directories():
    os.makedirs(VIDEO_OUTPUT, exist_ok=True)
    os.makedirs(PLAYLIST_OUTPUT, exist_ok=True)

def update_m3u8_playlist():
    try:
        # List all video chunks in the output directory
        chunk_files = sorted(glob.glob(f"{VIDEO_OUTPUT}/video_*.ts"))
        if not chunk_files:
            print("No video chunks found to create m3u8 file.")
            return

        # Create the .m3u8 content
        m3u8_content = "#EXTM3U\n"
        m3u8_content += "#EXT-X-VERSION:3\n"
        m3u8_content += "#EXT-X-TARGETDURATION:10\n"
        m3u8_content += "#EXT-X-MEDIA-SEQUENCE:0\n\n"

        # Flag to check if it's the first segment
        first_segment = True

        for chunk_file in chunk_files:
            duration = 10.0  # Assuming each chunk is 10 seconds
            chunk_filename = os.path.basename(chunk_file)

            # Add #EXT-X-DISCONTINUITY tag before segments after the first
            if not first_segment:
                m3u8_content += "#EXT-X-DISCONTINUITY\n"
            else:
                first_segment = False

            m3u8_content += f"#EXTINF:{duration},\n/api/v1/streaming/chunks/{chunk_filename}\n"

        # Add the #EXT-X-ENDLIST tag to signify the end of the playlist
        m3u8_content += "\n#EXT-X-ENDLIST\n"

        # Write the .m3u8 file to the playlist directory
        with open(PLAYLIST_FILE, "w") as f:
            f.write(m3u8_content)
        print(f"Updated m3u8 file with {len(chunk_files)} chunks.")

    except Exception as e:
        print(f"Error updating m3u8 file: {e}")

# Continuously monitors and processes new video files, updating the .m3u8 file
def process_video_files():
    processed_files = set()
    while True:
        files = sorted(glob.glob(f"{VIDEO_OUTPUT}/video_*.ts"))
        new_files = [file for file in files if file not in processed_files]
        if new_files:
            for file in new_files:
                processed_files.add(file)
                print(f"New chunk detected: {file}")
            # Update the .m3u8 file whenever a new chunk is detected
            update_m3u8_playlist()
        time.sleep(1)

# Extracts video from the stream and segments it for processing
def process_video(stream_url: str):
    try:
        # Run the video processing in a separate thread
        executor.submit(run_ffmpeg, stream_url)
    except Exception as e:
        print(f"Error processing video: {e}")

# Function to run the FFmpeg command
def run_ffmpeg(stream_url: str):
    setup_media_directories()

    # FFmpeg command to segment the video every 10 seconds
    command = [
        "ffmpeg",
        "-i", stream_url,
        "-c:v", "copy",        # Copy the video codec as is (no re-encoding)
        "-c:a", "aac",         # Audio codec
        "-f", "segment",       # Segment format
        "-segment_time", "10", # Duration of each segment
        "-strftime", "1",      # Include date-time in the output filenames
        "-reset_timestamps", "1",  # Reset timestamps for each segment
        f"{VIDEO_OUTPUT}/video_%Y%m%d%H%M%S.ts"
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Video extraction started from {stream_url}")

    # Start the background thread to process video files
    threading.Thread(target=process_video_files, daemon=True).start()

    # Wait for the FFmpeg process to complete
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"FFmpeg error: {stderr.decode()}")

