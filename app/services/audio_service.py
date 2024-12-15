# audio_service.py

import os
import subprocess

AUDIO_OUTPUT = "app/media/audio"

# Ensure the audio output directory exists
def setup_audio_directory():
    os.makedirs(AUDIO_OUTPUT, exist_ok=True)

def segment_audio(stream_url: str, chunk_duration: int):
    setup_audio_directory()
    audio_segment_filename = os.path.join(AUDIO_OUTPUT, "audio_%d.wav")

    # FFmpeg command to segment the audio stream
    command = [
        "ffmpeg",
        "-i", stream_url,
         "-map", "0:0",                       # Select only the first audio stream (Stream #0:0)
        "-c:a", "pcm_s16le",                 # Set audio codec to uncompressed PCM (WAV format)
        "-ar", "16000",                       # Set audio sample rate to 16 kHz (common for STT)
        "-ac", "1",                           # Set audio channels to mono (single channel for STT)
        "-f", "segment",                      # Use the segment muxer to split the audio
        "-segment_time", str(chunk_duration),  # Duration of each audio segment in seconds
        "-reset_timestamps", "1",             # Reset timestamps for each new segment
        audio_segment_filename
    ]

    # Execute the FFmpeg command to segment the audio stream
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Audio segmentation started.")

    # Wait for the FFmpeg process to complete and capture output/errors
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"FFmpeg audio segmentation error: {stderr.decode()}")
