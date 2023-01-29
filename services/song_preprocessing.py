from typing import List, Optional

from dao.dao_mxm_labels import DAOMxmLabels
from models.mxm_label import MxmLabel
from models.mxm_object import MxmAttribute


def translate_mxm_attrs_to_lyrics(mxm_attrs: List[MxmAttribute], dict_of_translations: Optional[dict]) -> str:
    if not dict_of_translations:
        dao_mxm_labels = DAOMxmLabels()
        sentence = ''
        for mxm_attr in mxm_attrs:
            mxm_label: MxmLabel = dao_mxm_labels.find_one_by_query({"attr_id": mxm_attr.atrr_id})
            part_sentence = (mxm_label.attr_name + " ") * mxm_attr.atrr_value
            sentence += part_sentence
        return sentence
    else:
        sentence = ''
        for mxm_attr in mxm_attrs:
            part_sentence = (dict_of_translations[mxm_attr.atrr_id] + " ") * mxm_attr.atrr_value
            sentence += part_sentence
        return sentence