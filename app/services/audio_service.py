# audio_service.py

import os
import subprocess

AUDIO_OUTPUT = "app/media/audio"

def setup_audio_directory():
    os.makedirs(AUDIO_OUTPUT, exist_ok=True)

def segment_audio(stream_url: str, chunk_duration: int):
    setup_audio_directory()
    audio_segment_filename = os.path.join(AUDIO_OUTPUT, "audio_%d.wav")

    # FFmpeg command to segment the audio stream
    command = [
        "ffmpeg",
        "-i", stream_url,                 # Input URL of the audio stream
        "-map", "0:a",                    # Select only the audio stream (map the audio channel)
        "-c:a", "pcm_s16le",              # Set audio codec to uncompressed PCM (WAV format)
        "-ar", "44100",                   # Set audio sample rate to 44.1 kHz
        "-ac", "2",                       # Set audio channels to stereo (2 channels)
        "-f", "segment",                  # Use the segment format to split the audio into parts
        "-segment_time", str(chunk_duration),  # Duration of each audio segment
        "-reset_timestamps", "1",         # Reset timestamps for each new segment
        audio_segment_filename            # Output pattern for the segmented audio files
    ]

    # Execute the FFmpeg command to segment the audio stream
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Audio segmentation started.")

    # Wait for the FFmpeg process to complete and capture output/errors
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"FFmpeg audio segmentation error: {stderr.decode()}")
