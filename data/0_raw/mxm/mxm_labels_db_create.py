# raw data files downloaded from http://millionsongdataset.com/musixmatch/

from typing import List

from music_recommendation.dao.dao_mxm_labels import DAOMxmLabels
from music_recommendation.models.mxm_label import MxmLabel

if __name__ == '__main__':
    dao_labels: DAOMxmLabels = DAOMxmLabels()

    with open(
            ".\mxm_labels.txt",
            'r', encoding='utf-8') as f:
        data = f.read()
        attr_list = data.split(',')
        for i, attr in enumerate(attr_list):
            dao_labels.insert_one(MxmLabel(attr_id=i+1, attr_name=attr))
