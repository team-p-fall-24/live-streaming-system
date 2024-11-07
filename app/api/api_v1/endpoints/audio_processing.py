from fastapi import APIRouter, BackgroundTasks
from app.schemas.audio_processing import AudioProcessingRequest
from app.services.audio_service import segment_audio

router = APIRouter()

@router.post("/segment-audio/")
async def process_audio_endpoint(request: AudioProcessingRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(segment_audio, request.stream_url)
    return {"message": "Audio processing started in the background"}
