from typing import List, Optional

from pydantic import BaseModel


class MsdTriplet(BaseModel):
    user_id: str
    song_id: str
    listen_count: int
    # ranking_score: Optional[float]
