from fastapi import APIRouter, BackgroundTasks
from app.schemas.subtitle_sync import SubtitleSyncRequest
from app.services.subtitle_service import sync_subtitles

router = APIRouter()

@router.post("/sync")
async def sync_subtitles_endpoint(request: SubtitleSyncRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(sync_subtitles, request.stream_url, request.subtitle_file)
    return {"message": "Subtitle synchronization started in the background"}
