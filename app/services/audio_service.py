import subprocess
import os
import openai
from app.services.stt_service import transcribe_audio_with_openai

def process_audio(stream_url: str):
    try:
        if not stream_url.endswith(".m3u8"):
            raise ValueError("Provided URL is not an HLS (.m3u8) stream.")

        print(f"Processing HLS stream from {stream_url}...")

        # 10-second blocks.
        output_pattern = "output_audio_segment_%03d.wav"
        
        # FFmpeg command to cut audio(10s)
        command = [
            "ffmpeg",
            "-i", stream_url,  # Input HLS stream (.m3u8)
            "-vn",  # No video, audio only
            "-acodec", "pcm_s16le",  # WAV format
            "-ar", "44100",  # Sample rate (44.1 kHz)
            "-ac", "2",  # Stereo audio
            "-f", "segment",  # Segment the audio
            "-segment_time", "10",  # Cut into 10-second segments
            "-reset_timestamps", "1",  # Reset timestamps for each segment
            output_pattern  # Output file pattern
        ]
        
        # Run FFmpeg command, create the audio segments
        subprocess.run(command, check=True)
        print(f"Audio segments saved as {output_pattern}")

        # Now we process each segment using stt of openai
        segment_index = 0
        while True:
            segment_file = f"output_audio_segment_{segment_index:03d}.wav"
            if not os.path.exists(segment_file):
                break  # No more segments to process
            
            print(f"Transcribing segment: {segment_file}")
            transcription = transcribe_audio_with_openai(segment_file)
            print(f"Transcription for {segment_file}: {transcription}")

            # Save transcriptions
            segment_index += 1

    except subprocess.CalledProcessError as e:
        print(f"Error processing audio: {e}")
    except ValueError as ve:
        print(ve)
