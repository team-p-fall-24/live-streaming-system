from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import Response, FileResponse
from app.services import live_stream_service
import os

from app.variables import LIVESTREAM_OUTPUT, PLAYLIST_FILE, PLAYLIST_OUTPUT, TRANSLATION_OUTPUT, VIDEO_OUTPUT

router = APIRouter()

# Endpoint to start processing the video stream
@router.post("/process-stream/")
async def process_video_endpoint(background_tasks: BackgroundTasks, stream_url: str):
    try:    
        # Add the process_video function as a background task
        background_tasks.add_task(live_stream_service.process_stream, stream_url)
        return {"message": "Video stream processing started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to serve the .m3u8 playlist file
@router.get("/playlist.m3u8")
async def get_m3u8():
    if os.path.isfile(PLAYLIST_FILE):
        headers = {
            "Content-Type": "application/vnd.apple.mpegurl",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        }
        with open(PLAYLIST_FILE, "rb") as f:
            return Response(content=f.read(), headers=headers, media_type="application/vnd.apple.mpegurl")
    else:
        raise HTTPException(status_code=404, detail="Playlist not found")


# Endpoint to serve the index .m3u8 master file
@router.get("/index.m3u8")
async def get_m3u8():
    if os.path.isfile(LIVESTREAM_OUTPUT):
        headers = {
            "Content-Type": "application/vnd.apple.mpegurl",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        }
        with open(LIVESTREAM_OUTPUT, "rb") as f:
            return Response(content=f.read(), headers=headers, media_type="application/vnd.apple.mpegurl")
    else:
        raise HTTPException(status_code=404, detail="Playlist not found")


# Endpoint to serve individual .ts video chunks
@router.get("/chunks/{filename}")
async def get_chunk(filename: str):
    file_path = f"{VIDEO_OUTPUT}/{filename}"
    if os.path.isfile(file_path):
        headers = {
            "Content-Type": "video/MP2T",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        }
        return FileResponse(file_path, headers=headers, media_type="video/MP2T")
    else:
        raise HTTPException(status_code=404, detail="Chunk file not found")

        
# Endpoint to serve subtitle files
@router.get("/subtitles/{language}")
async def get_subtitle(language: str):
    subtitle_path = f"{PLAYLIST_OUTPUT}/{language}_sub.m3u8"
    if os.path.isfile(subtitle_path):
        headers = {
            "Content-Type": "application/vnd.apple.mpegurl",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        }
        with open(subtitle_path, "rb") as f:
            return Response(content=f.read(), headers=headers, media_type="application/vnd.apple.mpegurl")
    else:
        raise HTTPException(status_code=404, detail=f"{language.capitalize()} subtitle playlist is not found")


        
# Endpoint to serve individual translation chunks
@router.get("/{language}/{filename}")
async def get_translation_audio(language: str, filename: str):
    subtitle_path = f"{TRANSLATION_OUTPUT}/{language}/{filename}"
    if os.path.isfile(subtitle_path):
        headers = {
            "Content-Type": "text/vtt",  # Correct MIME type for WebVTT
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        }
        return FileResponse(subtitle_path, headers=headers, media_type="text/vtt")
    else:
        raise HTTPException(status_code=404, detail="Subtitle file not found")
