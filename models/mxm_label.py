from pydantic import BaseModel


class MxmLabel(BaseModel):
    attr_id: int
    attr_name: str
