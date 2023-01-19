from pydantic import BaseModel


class MsdTriplet(BaseModel):
    user_id: str
    song_id: str
    listen_count: int
