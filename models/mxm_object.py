from typing import List, Optional
from pydantic import BaseModel


class MxmAttribute(BaseModel):
    atrr_id: int
    atrr_value: int


class MxmObject(BaseModel):
    msd_id: str
    msd_id_true: Optional[str] = None
    mxm_id: str
    attr_list: List[MxmAttribute]
    sentiment: Optional[float] = None
