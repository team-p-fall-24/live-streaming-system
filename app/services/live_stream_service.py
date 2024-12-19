# service/live_stream_service.py
import os
import shutil
import glob
import time
from concurrent.futures import ThreadPoolExecutor
from app.services.stt_service import transcribe_audio
from app.services.video_service import segment_video  # Import video segmentation
from app.services.audio_service import segment_audio
from app.services.translation_service import translate_file  # Import translation function
from app.variables import AUDIO_OUTPUT, LIVESTREAM_OUTPUT, MEDIA_DIR, THAI_WEBVTT_FILE, VIDEO_OUTPUT, PLAYLIST_OUTPUT, PLAYLIST_FILE, CHUNK_DURATION, SUBTITLE_OUTPUT, TRANSLATION_OUTPUT, VIET_WEBVTT_FILE

# Set up an executor for background tasks
executor = ThreadPoolExecutor(max_workers=5)  # Allow both video and audio tasks

# Automatically create the media directories if they don't exist
def setup_media_directories():
    os.makedirs(VIDEO_OUTPUT, exist_ok=True)
    os.makedirs(PLAYLIST_OUTPUT, exist_ok=True)
    os.makedirs(AUDIO_OUTPUT, exist_ok=True)
    os.makedirs(SUBTITLE_OUTPUT, exist_ok=True)
    os.makedirs(TRANSLATION_OUTPUT, exist_ok=True)

    
# Create index files and translation file
def setup_output_files():
    # index output
    langs = {"vi": "Vietnamese", "th": "Thai"}
    with open(LIVESTREAM_OUTPUT, "w") as f:
        m3u8_content = "#EXTM3U\n"
        m3u8_content += "#EXT-X-VERSION:3\n"
        
        for key in langs:
            m3u8_content += f'#EXT-X-MEDIA:TYPE=SUBTITLES,GROUP-ID="subs",NAME="{langs[key]}",FORCED=NO,AUTOSELECT=YES,URI="/api/v1/streaming/subtitles/{key}",LANGUAGE="{key}"\n'
        
        m3u8_content += '\n#EXT-X-STREAM-INF:SUBTITLES="subs"\n/api/v1/streaming/playlist.m3u8'
        f.write(m3u8_content)
    
    print("Finished writing the master output file.")

    # create two blank translation file
    with open(THAI_WEBVTT_FILE, 'w') as f:
        pass
    with open(VIET_WEBVTT_FILE, 'w') as f:
        pass

# Function to update the m3u8 playlist file dynamically
def update_m3u8_playlist():
    try:
        chunk_files = sorted(glob.glob(f"{VIDEO_OUTPUT}/video_*.ts"), key=os.path.getctime)
        if not chunk_files:
            print("No video chunks found to create m3u8 file.")
            return

        media_sequence = int(os.path.splitext(os.path.basename(chunk_files[0]))[0].split('_')[1])

        m3u8_content = "#EXTM3U\n"
        m3u8_content += "#EXT-X-PLAYLIST-TYPE:LIVE\n"
        m3u8_content += f"#EXT-X-TARGETDURATION:{CHUNK_DURATION}\n"
        m3u8_content += f"#EXT-X-MEDIA-SEQUENCE:{media_sequence}\n\n"

        for chunk_file in chunk_files:
            chunk_filename = os.path.basename(chunk_file)
            m3u8_content += f'#EXTINF:{CHUNK_DURATION}\n/api/v1/streaming/chunks/{chunk_filename}\n'

        with open(PLAYLIST_FILE, "w") as f:
            f.write(m3u8_content)
        print(f"Updated m3u8 file with {len(chunk_files)} chunks.")
        

    except Exception as e:
        print(f"Error updating m3u8 file: {e}")

# Continuously monitors and processes new video files, updating the .m3u8 file
def process_video_files():
    processed_files = set()
    while True:
        files = sorted(glob.glob(f"{VIDEO_OUTPUT}/video_*.ts"), key=os.path.getctime)
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

# Monitors and processes subtitle files, call the translation service, and update the translation .m3u8 file
def process_translation_files():
    def is_file_stable(file_path, wait_time=4):
        initial_size = os.path.getsize(file_path)
        time.sleep(wait_time)
        final_size = os.path.getsize(file_path)
        return initial_size == final_size and initial_size > 0

    processed_files = set()
    while True:
        files = sorted(glob.glob(f"{SUBTITLE_OUTPUT}/audio_*.txt"), key=os.path.getctime)
        new_files = [file for file in files if file not in processed_files]
        if new_files:
            for file in new_files:
                if is_file_stable(file):
                    processed_files.add(file)
                    print(f"New subtitle file detected: {file}")
                    translate_file(file)
                else:
                    # Wait additional 2 seconds and check again
                    time.sleep(1)
                    if is_file_stable(file, wait_time=2):
                        processed_files.add(file)
                        print(f"New subtitle file detected after additional wait: {file}")
                        translate_file(file)
                    else:
                        print(f"Skipping empty subtitle file: {file}")
        time.sleep(1)

# Main function to start processing the video and audio streams
def process_stream(stream_url: str):
    # remove the media file before proceeding with other steps
    if os.path.exists(MEDIA_DIR):
        shutil.rmtree(MEDIA_DIR)

    # setup
    setup_media_directories()   
    # set up file & translation files
    setup_output_files()

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
