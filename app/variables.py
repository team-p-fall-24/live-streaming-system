from dotenv import load_dotenv
import os

load_dotenv()

# Directories for storing video chunks and m3u8 files
AUDIO_OUTPUT = os.getenv("AUDIO_OUTPUT")
VIDEO_OUTPUT = os.getenv("VIDEO_OUTPUT")
SUBTITLE_OUTPUT = os.getenv("SUBTITLE_OUTPUT")
TRANSLATION_OUTPUT = os.getenv("TRANSLATION_OUTPUT")
PLAYLIST_OUTPUT = os.getenv("PLAYLIST_OUTPUT")
PLAYLIST_FILE = f"{PLAYLIST_OUTPUT}/playlist.m3u8"
MEDIA_DIR = os.getenv("MEDIA_DIR")
LIVESTREAM_OUTPUT = f"{MEDIA_DIR}/index.m3u8"

VIET_WEBVTT_FILE = os.path.join(TRANSLATION_OUTPUT, "viet_sub.m3u8")
THAI_WEBVTT_FILE = os.path.join(TRANSLATION_OUTPUT, "thai_sub.m3u8")

# Configurable chunk duration in seconds
CHUNK_DURATION = int(os.getenv("CHUNK_DURATION"))
