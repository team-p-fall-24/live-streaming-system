from pydantic import BaseModel, HttpUrl

class SubtitleSyncRequest(BaseModel):
    stream_url: HttpUrl
    subtitle_file: str
