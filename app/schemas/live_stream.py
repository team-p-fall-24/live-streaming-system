from pydantic import BaseModel, HttpUrl

class LiveStreamRequest(BaseModel):
    stream_url: HttpUrl
