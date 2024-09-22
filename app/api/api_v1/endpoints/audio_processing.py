from fastapi import APIRouter, BackgroundTasks
from app.schemas.audio_processing import AudioProcessingRequest
from app.services.audio_service import process_audio

router = APIRouter()

@router.post("/extract")
async def process_audio_endpoint(request: AudioProcessingRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_audio, request.stream_url)
    return {"message": "Audio processing started in the background"}
