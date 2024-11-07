# audio_service.py

import os
import subprocess

AUDIO_OUTPUT = "app/media/audio"

def setup_audio_directory():
    os.makedirs(AUDIO_OUTPUT, exist_ok=True)

def segment_audio(stream_url: str, chunk_duration: int):
    setup_audio_directory()
    audio_segment_filename = os.path.join(AUDIO_OUTPUT, "audio_%d.wav")

    command = [
        "ffmpeg",
        "-i", stream_url,
        "-map", "0:a",
        "-c:a", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        "-f", "segment",
        "-segment_time", str(chunk_duration),
        "-reset_timestamps", "1",
        audio_segment_filename
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Audio segmentation started.")

    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"FFmpeg audio segmentation error: {stderr.decode()}")
