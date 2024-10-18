from fastapi import APIRouter, HTTPException
from app.services import live_stream_service

router = APIRouter()

@router.post("/process-video/")
async def process_video_endpoint(stream_url: str):
    try:
        live_stream_service.process_video(stream_url)
        return {"message": "Video stream processing started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
