from pydantic import BaseModel


class TidToMsdIdConverter(BaseModel):
    tid: str
    msd_id: str
    artist_name: str
    title: str
