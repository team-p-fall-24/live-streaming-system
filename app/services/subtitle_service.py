import subprocess

def sync_subtitles(stream_url: str, subtitle_file: str):
    try:
        command = [
            "ffmpeg",
            "-i", stream_url,
            "-vf", f"subtitles={subtitle_file}",
            "-c:v", "libx264",
            "-c:a", "copy",
            "output_video_with_subtitles.mp4"
        ]
        subprocess.run(command, check=True)
        print(f"Subtitles synchronized for {stream_url}")
    except subprocess.CalledProcessError as e:
        print(f"Error syncing subtitles: {e}")
