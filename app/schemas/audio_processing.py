from pydantic import BaseModel, HttpUrl

class AudioProcessingRequest(BaseModel):
    stream_url: HttpUrl
