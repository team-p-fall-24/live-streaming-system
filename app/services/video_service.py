# video_service.py
import os
import subprocess

# Directory paths for storing video chunks and playlists
VIDEO_OUTPUT = "app/media/chunks"       # Directory for video chunk output
PLAYLIST_OUTPUT = "app/media/playlists" # Directory for playlist output

# Function to ensure the video and playlist directories exist
def setup_video_directory():
    os.makedirs(VIDEO_OUTPUT, exist_ok=True)       
    os.makedirs(PLAYLIST_OUTPUT, exist_ok=True)    

# Function to segment video from a streaming URL into chunks of a specified duration
def segment_video(stream_url: str, chunk_duration: int):
    # Ensure the necessary directories are set up
    setup_video_directory()

    # Define the path for the output playlist and video segments
    playlist_path = os.path.join(PLAYLIST_OUTPUT, "playlist.m3u8")  # Path .m3u8 output
    segment_filename = os.path.join(VIDEO_OUTPUT, "video_%d.ts")    # Pattern of segments

    # FFmpeg command for video segmentation
    command = [
        "ffmpeg",                              # The command to call FFmpeg
        "-i", stream_url,                      # Input URL of the video stream
        "-c:v", "copy",                        # Copy the video codec without re-encoding
        "-c:a", "copy",                        # Copy the audio codec without re-encoding
        "-f", "hls",                           # Specify the output format as HLS
        "-hls_time", str(chunk_duration),      # Duration of each HLS segment in seconds
        "-hls_list_size", "0",                 # Keep all segments in the playlist
        "-hls_segment_filename", segment_filename,  # Pattern for segment filenames
        playlist_path                          # Path to the output playlist file
    ]

    # Run the FFmpeg command as a subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Video segmentation started from streaming input URL {stream_url}")

    # Wait for the FFmpeg process to complete and capture output/errors
    stdout, stderr = process.communicate()
    if process.returncode != 0:                 
        print(f"FFmpeg video segmentation error: {stderr.decode()}")
