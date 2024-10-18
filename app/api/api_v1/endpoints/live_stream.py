from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from app.services import live_stream_service
import os

router = APIRouter()

# Endpoint to start processing the video stream
@router.post("/process-video/")
async def process_video_endpoint(background_tasks: BackgroundTasks, stream_url: str):
    try:    
        # Add the process_video function as a background task
        background_tasks.add_task(live_stream_service.process_video, stream_url)
        return {"message": "Video stream processing started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to serve the .m3u8 playlist file
@router.get("/playlist.m3u8")
async def get_m3u8():
    playlist_path = "app/media/playlists/playlist.m3u8"
    if os.path.isfile(playlist_path):
        # Use FileResponse to directly serve the latest version of the .m3u8 file
        return FileResponse(
            playlist_path, 
            media_type="application/vnd.apple.mpegurl", 
            headers={"Cache-Control": "no-store"}
        )
    else:
        raise HTTPException(status_code=404, detail="Playlist not found")

# Endpoint to serve individual .ts video chunks
@router.get("/chunks/{filename}")
async def get_chunk(filename: str):
    file_path = f"app/media/chunks/{filename}"
    if os.path.isfile(file_path):
        return FileResponse(file_path, media_type="video/MP2T")
    else:
        raise HTTPException(status_code=404, detail="Chunk file not found")
    