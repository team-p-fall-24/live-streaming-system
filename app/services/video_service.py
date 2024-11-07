# video_service.py

import os
import subprocess

VIDEO_OUTPUT = "app/media/chunks"
PLAYLIST_OUTPUT = "app/media/playlists"

def setup_video_directory():
    os.makedirs(VIDEO_OUTPUT, exist_ok=True)
    os.makedirs(PLAYLIST_OUTPUT, exist_ok=True)

def segment_video(stream_url: str, chunk_duration: int):
    setup_video_directory()

    playlist_path = os.path.join(PLAYLIST_OUTPUT, "playlist.m3u8")
    segment_filename = os.path.join(VIDEO_OUTPUT, "video_%d.ts")

    command = [
        "ffmpeg",
        "-i", stream_url,
        "-c:v", "copy",
        "-c:a", "copy",
        "-f", "hls",
        "-hls_time", str(chunk_duration),
        "-hls_list_size", "0",
        "-hls_segment_filename", segment_filename,
        playlist_path
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Video segmentation started from streaming input URL {stream_url}")

    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"FFmpeg video segmentation error: {stderr.decode()}")
