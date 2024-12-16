from fastapi import APIRouter, BackgroundTasks
from app.schemas.subtitle_sync import SubtitleSyncRequest
from app.services.stt_service import transcribe_audio

router = APIRouter()

@router.post("/transcribe")
async def transcribe_audio_endpoint(request: SubtitleSyncRequest, background_tasks: BackgroundTasks):
    """
    Endpoint to transcribe an audio file asynchronously.

    Args:
        request (SubtitleSyncRequest): The request body containing the audio file path.
        background_tasks (BackgroundTasks): FastAPI's background task manager.

    Returns:
        dict: A message indicating that the transcription task has started.
    """
    audio_file_path = request.audio_file_path

    # Add the transcription task to run in the background
    background_tasks.add_task(transcribe_audio, audio_file_path)
    
    return {"message": f"Transcription started in the background for {audio_file_path}"}
