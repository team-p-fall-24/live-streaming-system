import subprocess
import threading
import glob
import time
import librosa

AUDIO_OUTPUT = "app/output"

# Processes an individual audio file: transcribes, writes subtitles, and deletes the file once donee processing
def process_audio_file(file):
    print(f"Processing file {file}")
    return

# Continuously monitors and processes new audio files
def process_audio_files():
    processed_files = set()
    while True:
        files = glob.glob(f"{AUDIO_OUTPUT}/audio_*.wav")
        for file in files:
            if file not in processed_files:
                duration = librosa.get_duration(path=file)
                # Only process audio files whose length is over 9 seconds
                if duration > 9:
                    print(f"File {file} has duration {duration}")
                    processed_files.add(file)
                    process_audio_file(file)
        time.sleep(1)


# Extracts audio from the stream and segments it for processing
def process_audio(stream_url: str):
    try:
        # FFmpeg command to segment the audio every 10 seconds
        command = [
            "ffmpeg",
            "-i", stream_url,
            "-vn",  # No video
            "-acodec", "pcm_s16le",  # WAV format
            "-ar", "44100",  # Sample rate
            "-ac", "2",  # Stereo
            "-f", "segment", # Segment
            "-segment_time", "10",
            "-strftime", "1",
            "-reset_timestamps", "1",
            f"{AUDIO_OUTPUT}/audio_%Y%m%d%H%M%S.wav"
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Audio extracted from {stream_url}")

        # Start the background thread to process audio files
        print("Start processing audio files...")
        threading.Thread(target=process_audio_files, daemon=True).start()
        
        # Wait for the FFmpeg process to complete
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"FFmpeg error: {stderr.decode()}")

    except subprocess.CalledProcessError as e:
        print(f"Error processing audio: {e}")
