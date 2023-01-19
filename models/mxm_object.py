from typing import List
from pydantic import BaseModel


class MxmAttribute(BaseModel):
    atrr_id: int
    atrr_value: int


class MxmObject(BaseModel):
    msd_id: str
    mxm_id: str
    attr_list: List[MxmAttribute]
