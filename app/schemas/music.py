from pydantic import BaseModel

class MusicMetadata(BaseModel):
    artist: str
    title: str
    score: int
    MUSICBRAINZ_RECORDINGID: str

