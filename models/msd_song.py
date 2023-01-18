from typing import List, Optional

from pydantic import BaseModel


class MsdSong(BaseModel):
    song_id: str
    title: str
    release: str
    artist_name: str
    year: int
    # ranking_score: Optional[float]
