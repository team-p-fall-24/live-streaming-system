import os
import subprocess
import threading
import glob
import time

# Directories for storing video chunks and m3u8 files
VIDEO_OUTPUT = "app/media/chunks"
PLAYLIST_OUTPUT = "app/media/playlists"

# Sets up the directory structure if it doesn't exist
def setup_media_directories():
    os.makedirs(VIDEO_OUTPUT, exist_ok=True)
    os.makedirs(PLAYLIST_OUTPUT, exist_ok=True)

# Processes an individual video file: any custom logic or processing can be applied here
def process_video_file(file):
    print(f"Processing file {file}")
    # Add custom processing logic here (e.g., logging, post-processing)
    return

# Continuously monitors and processes new video files
def process_video_files():
    processed_files = set()
    while True:
        files = glob.glob(f"{VIDEO_OUTPUT}/video_*.ts")
        for file in files:
            if file not in processed_files:
                processed_files.add(file)
                process_video_file(file)
        time.sleep(1)

# Generates the .m3u8 playlist file based on the video chunks
def generate_m3u8_playlist():
    try:
        # List all video chunks in the output directory
        chunk_files = sorted(glob.glob(f"{VIDEO_OUTPUT}/video_*.ts"))
        if not chunk_files:
            print("No video chunks found to create m3u8 file.")
            return

        # Create the .m3u8 content
        m3u8_content = "#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-TARGETDURATION:10\n"
        m3u8_content += "#EXT-X-PLAYLIST-TYPE:VOD\n"

        for chunk_file in chunk_files:
            duration = 10  # Assuming each chunk is 10 seconds
            chunk_filename = os.path.basename(chunk_file)
            m3u8_content += f"#EXTINF:{duration},\n{chunk_filename}\n"

        m3u8_content += "#EXT-X-ENDLIST\n"

        # Write the .m3u8 file to the playlist directory
        playlist_path = f"{PLAYLIST_OUTPUT}/playlist.m3u8"
        with open(playlist_path, "w") as f:
            f.write(m3u8_content)
        print(f"Generated m3u8 file: {playlist_path}")

    except Exception as e:
        print(f"Error generating m3u8 file: {e}")

# Extracts video from the stream and segments it for processing
def process_video(stream_url: str):
    try:
        # Ensure the output directories exist
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
        print("Start processing video files...")
        threading.Thread(target=process_video_files, daemon=True).start()

        # Wait for the FFmpeg process to complete
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"FFmpeg error: {stderr.decode()}")

        # Generate the m3u8 file after processing
        generate_m3u8_playlist()

    except subprocess.CalledProcessError as e:
        print(f"Error processing video: {e}")
