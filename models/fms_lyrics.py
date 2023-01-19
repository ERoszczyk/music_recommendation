from typing import List, Optional

from pydantic import BaseModel


class FMSLyrics(BaseModel):
    title: str
    tag: str
    artist: str
    year: int
    views: int
    features: List[str]
    lyrics: str
    song_id: int
