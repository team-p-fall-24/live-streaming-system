import subprocess

def process_audio(stream_url: str):
    try:
        # Ensure the URL ends with .m3u8 (HLS format)
        if not stream_url.endswith(".m3u8"):
            raise ValueError("Provided URL is not an HLS (.m3u8) stream.")

        print(f"Processing HLS stream from {stream_url}...")
        output_file = "output_hls_audio.wav"

        command = [
            "ffmpeg",
            "-i", stream_url,  # Input HLS stream (.m3u8)
            "-vn",  # No video, audio only
            "-acodec", "pcm_s16le",  # WAV format
            "-ar", "44100",  # Sample rate (44.1 kHz)
            "-ac", "2",  # Stereo audio
            output_file  # Output WAV file
        ]
        
        # Run the FFmpeg command
        subprocess.run(command, check=True)
        print(f"Audio extracted and saved as {output_file} from {stream_url}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error processing audio: {e}")
    except ValueError as ve:
        print(ve)