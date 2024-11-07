from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import Response, FileResponse
from app.services import live_stream_service
import os

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
    playlist_path = "app/media/playlists/playlist.m3u8"
    if os.path.isfile(playlist_path):
        headers = {
            "Content-Type": "application/vnd.apple.mpegurl",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        }
        with open(playlist_path, "rb") as f:
            return Response(content=f.read(), headers=headers, media_type="application/vnd.apple.mpegurl")
    else:
        raise HTTPException(status_code=404, detail="Playlist not found")

# Endpoint to serve individual .ts video chunks
@router.get("/chunks/{filename}")
async def get_chunk(filename: str):
    file_path = f"app/media/chunks/{filename}"
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
