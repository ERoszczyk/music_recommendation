from typing import Optional

from pydantic import BaseModel


class MxmLabel(BaseModel):
    attr_id: int
    attr_name: str
    sentiment_score: Optional[int]  # -1 negative, 1 positive
