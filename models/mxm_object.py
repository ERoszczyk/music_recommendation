from typing import List, Optional

from pydantic import BaseModel


class MxmAttribute(BaseModel):
    atrr_id: int
    atrr_value: int


class MxmObject(BaseModel):
    msd_id: str
    mxm_id: str
    attr_list: List[MxmAttribute]
    # ranking_score: Optional[float]
