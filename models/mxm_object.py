from typing import List, Optional

import numpy as np
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
    representation_vector: Optional[List[float]] = None

    def to_readable_form(self, dict_of_mxm_labels: dict):
        words_list = []
        for attr in self.attr_list:
            words_list.append([dict_of_mxm_labels[attr.atrr_id], attr.atrr_value])

        return {
            'msd_id': self.msd_id,
            'msd_id_true': self.msd_id_true,
            'mxm_id': self.mxm_id,
            'sentiment': self.sentiment,
            'representation_vector': self.representation_vector,
            'words_list': words_list
        }

