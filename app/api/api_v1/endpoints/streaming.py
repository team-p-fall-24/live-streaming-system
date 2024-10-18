from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from app.services.streaming_service import stream_m3u8

router = APIRouter()

@router.get("/stream/")
async def stream_m3u8_endpoint(url: str = Query(..., description="URL of the .m3u8 file")):
    try:
        return await stream_m3u8(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 