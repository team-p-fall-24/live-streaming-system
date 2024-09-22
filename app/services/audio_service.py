import subprocess

def process_audio(stream_url: str):
    try:
        command = [
            "ffmpeg",
            "-i", stream_url,
            "-vn",  # No video
            "-acodec", "pcm_s16le",  # WAV format
            "-ar", "44100",  # Sample rate
            "-ac", "2",  # Stereo
            "output_audio.wav"
        ]
        subprocess.run(command, check=True)
        print(f"Audio extracted from {stream_url}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing audio: {e}")
