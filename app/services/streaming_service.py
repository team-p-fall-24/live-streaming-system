# app/services/streaming_service.py

import httpx
from fastapi.responses import StreamingResponse

async def stream_m3u8(url: str) -> StreamingResponse:
    async with httpx.AsyncClient() as client:
        # Fetch the response without using the stream argument
        response = await client.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the m3u8 file. Status code: {response.status_code}")
        
        # Use an iterator to stream the response content
        async def iter_content():
            async with client.stream("GET", url) as streamed_response:
                async for chunk in streamed_response.aiter_bytes():
                    yield chunk
        
        return StreamingResponse(
            iter_content(),
            media_type="application/vnd.apple.mpegurl"
        )
