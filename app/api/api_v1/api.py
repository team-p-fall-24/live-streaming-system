from fastapi import APIRouter
from app.api.api_v1.endpoints import live_stream, audio_processing, live_stream

api_router = APIRouter()

api_router.include_router(audio_processing.router, prefix="/audio", tags=["audio_processing"])

api_router.include_router(live_stream.router, prefix="/streaming", tags=["streaming"])
