from typing import Optional, List

from pydantic import BaseModel


class MsdSong(BaseModel):
    song_id: str
    title: str
    release: str
    artist_name: str
    year: int
    # ranking_score: Optional[float]


class MsdSongWithLyrics(MsdSong):
    tag: Optional[str]
    features: Optional[List[str]]
    lyrics: Optional[str]
