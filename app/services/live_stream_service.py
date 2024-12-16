# service/live_stream_service.py
import os
import glob
import time
from concurrent.futures import ThreadPoolExecutor
from app.services.stt_service import transcribe_audio
from app.services.video_service import segment_video  # Import video segmentation
from app.services.audio_service import segment_audio
from app.services.translation_service import translate_file  # Import translation function
from app.variables import AUDIO_OUTPUT, VIDEO_OUTPUT, PLAYLIST_OUTPUT, PLAYLIST_FILE, CHUNK_DURATION, SUBTITLE_OUTPUT, TRANSLATION_OUTPUT

# Set up an executor for background tasks
executor = ThreadPoolExecutor(max_workers=5)  # Allow both video and audio tasks

# Sets up the directory structure if it doesn't exist
def setup_media_directories():
    os.makedirs(VIDEO_OUTPUT, exist_ok=True)
    os.makedirs(PLAYLIST_OUTPUT, exist_ok=True)
    os.makedirs(AUDIO_OUTPUT, exist_ok=True)
    os.makedirs(SUBTITLE_OUTPUT, exist_ok=True)
    os.makedirs(TRANSLATION_OUTPUT, exist_ok=True)

# Function to update the m3u8 playlist file dynamically
def update_m3u8_playlist():
    try:
        chunk_files = sorted(glob.glob(f"{VIDEO_OUTPUT}/video_*.ts"))
        if not chunk_files:
            print("No video chunks found to create m3u8 file.")
            return

        media_sequence = int(os.path.splitext(os.path.basename(chunk_files[0]))[0].split('_')[1])

        m3u8_content = "#EXTM3U\n"
        m3u8_content += "#EXT-X-VERSION:3\n"
        m3u8_content += "#EXT-X-PLAYLIST-TYPE:LIVE\n"
        m3u8_content += f"#EXT-X-TARGETDURATION:{CHUNK_DURATION}\n"
        m3u8_content += f"#EXT-X-MEDIA-SEQUENCE:{media_sequence}\n\n"

        for chunk_file in chunk_files:
            chunk_filename = os.path.basename(chunk_file)
            m3u8_content += f"#EXTINF:{CHUNK_DURATION},\n/api/v1/live/chunks/{chunk_filename}\n"

        with open(PLAYLIST_FILE, "w") as f:
            f.write(m3u8_content)
        print(f"Updated m3u8 file with {len(chunk_files)} chunks.")

    except Exception as e:
        print(f"Error updating m3u8 file: {e}")

# Continuously monitors and processes new video files, updating the .m3u8 file
def process_video_files():
    processed_files = set()
    while True:
        files = sorted(glob.glob(f"{VIDEO_OUTPUT}/video_*.ts"))
        new_files = [file for file in files if file not in processed_files]
        if new_files:
            for file in new_files:
                processed_files.add(file)
                print(f"New chunk detected: {file}")
            update_m3u8_playlist()
        time.sleep(1)


# Monitors and processes audio files, call the translation and update the .m3u8 file
def process_audio_files():
    def is_file_stable(file_path, wait_time=6):
        initial_size = os.path.getsize(file_path)
        time.sleep(wait_time)
        final_size = os.path.getsize(file_path)
        return initial_size == final_size
    
    processed_files = set()
  
    while True:
        files = sorted(glob.glob(f"{AUDIO_OUTPUT}/audio_*.wav"), key=os.path.getctime) # make sure they should order the videos by time
        new_files = [file for file in files if file not in processed_files]
        if new_files:
            for file in new_files:
                if is_file_stable(file):
                    processed_files.add(file)
                    print(f"New audio file detected: {file}")
                    # transcribe something
                    transcribe_audio(file)

        time.sleep(1)

# Monitors and processes subtitle files, call the translation service
def process_translation_files():
    processed_files = set()
    while True:
        files = sorted(glob.glob(f"{SUBTITLE_OUTPUT}/audio_*.txt"), key=os.path.getctime)
        new_files = [file for file in files if file not in processed_files]
        if new_files:
            for file in new_files:
                processed_files.add(file)
                print(f"New subtitle file detected: {file}")
                translate_file(file)
        time.sleep(1)

# Main function to start processing the video and audio streams
def process_stream(stream_url: str):
    try:
        # Submit tasks for video and audio segmentation to the executor
        executor.submit(segment_video, stream_url, CHUNK_DURATION)
        executor.submit(segment_audio, stream_url, CHUNK_DURATION)
        
        # Start background thread to process video files, audio files, subtitle files, and translation files
        executor.submit(process_video_files)
        executor.submit(process_audio_files)
        executor.submit(process_translation_files)
        
        print(f"Processing started for {stream_url}")
    except Exception as e:
        print(f"Error processing video: {e}")
