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

# Configurable chunk duration in seconds
CHUNK_DURATION = 10 # Change this value to different fixed duration later. Currently using 10 seconds.

# Set up an executor for background tasks
executor = ThreadPoolExecutor(max_workers=1)

# Sets up the directory structure if it doesn't exist
def setup_media_directories():
    os.makedirs(VIDEO_OUTPUT, exist_ok=True)
    os.makedirs(PLAYLIST_OUTPUT, exist_ok=True)

# Function to update the m3u8 playlist file dynamically
def update_m3u8_playlist():
    try:
        # List all video chunks in the output directory
        chunk_files = sorted(glob.glob(f"{VIDEO_OUTPUT}/video_*.ts"))
        if not chunk_files:
            print("No video chunks found to create m3u8 file.")
            return

        # Calculate the media sequence number based on the number of segments
        media_sequence = int(os.path.splitext(os.path.basename(chunk_files[0]))[0].split('_')[1])

        # Create the .m3u8 content
        m3u8_content = "#EXTM3U\n"
        m3u8_content += "#EXT-X-VERSION:3\n"
        m3u8_content += "#EXT-X-PLAYLIST-TYPE:LIVE\n"
        m3u8_content += f"#EXT-X-TARGETDURATION:{CHUNK_DURATION}\n"
        m3u8_content += f"#EXT-X-MEDIA-SEQUENCE:{media_sequence}\n\n"

        for chunk_file in chunk_files:
            chunk_filename = os.path.basename(chunk_file)
            m3u8_content += f"#EXTINF:{CHUNK_DURATION},\n/api/v1/live/chunks/{chunk_filename}\n"

        # Do NOT add the #EXT-X-ENDLIST tag for live streaming

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
            # Update the .m3u8 file whenever new chunks are detected
            update_m3u8_playlist()
        time.sleep(1)

# Extracts video from the stream and segments it for processing
def process_video(stream_url: str):
    try:
        # Run the video processing in a separate thread
        executor.submit(run_ffmpeg, stream_url)
    except Exception as e:
        print(f"Error processing video: {e}")

# Function to run the FFmpeg command with configurable chunk duration
def run_ffmpeg(stream_url: str):
    setup_media_directories()

    playlist_path = os.path.join(PLAYLIST_OUTPUT, "playlist.m3u8")
    segment_filename = os.path.join(VIDEO_OUTPUT, "video_%d.ts")

    # FFmpeg command to use the HLS muxer for segmenting
    command = [
        "ffmpeg",
        "-i", stream_url,
        "-c:v", "copy",                   # Copy video codec without re-encoding
        "-c:a", "copy",                   # Copy audio codec without re-encoding
        "-f", "hls",                      # Use HLS muxer instead of segment format
        "-hls_time", str(CHUNK_DURATION), # Duration of each segment
        "-hls_list_size", "0",            # Keep all segments in the playlist (for live streaming)
        "-hls_segment_filename", segment_filename,  # Pattern for segment filenames
        playlist_path
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Video extraction started from {stream_url}")

    # Start the background thread to process video files
    threading.Thread(target=process_video_files, daemon=True).start()

    # Wait for the FFmpeg process to complete
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"FFmpeg error: {stderr.decode()}")

