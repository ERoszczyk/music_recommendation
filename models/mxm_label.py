from typing import List, Optional

from pydantic import BaseModel

class MxmLabel(BaseModel):
    attr_id: int
    attr_name: str
    # ranking_score: Optional[float]
