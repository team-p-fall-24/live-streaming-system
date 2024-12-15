# Directories for storing video chunks and m3u8 files
AUDIO_OUTPUT = "app/media/audio"
VIDEO_OUTPUT = "app/media/chunks"
SUBTITLE_OUTPUT = "app/media/subtitles"
PLAYLIST_OUTPUT = "app/media/playlists"
PLAYLIST_FILE = f"{PLAYLIST_OUTPUT}/playlist.m3u8"
# Configurable chunk duration in seconds
CHUNK_DURATION = 10 # Currently use the 10-second chunk duration