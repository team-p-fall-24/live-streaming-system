from fastapi import APIRouter, BackgroundTasks
from app.schemas.live_stream import LiveStreamRequest
from app.services.live_stream_service import start_live_stream, stop_live_stream

router = APIRouter()

@router.post("/start")
async def start_live_stream_endpoint(request: LiveStreamRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(start_live_stream, request.stream_url)
    return {"message": "Live streaming started"}

@router.post("/stop")
async def stop_live_stream_endpoint(request: LiveStreamRequest):
    stop_live_stream(request.stream_url)
    return {"message": "Live streaming stopped"}
