# raw data files downloaded from http://millionsongdataset.com/musixmatch/

from typing import List

from music_recommendation.dao.dao_mxm_objects import DAOMxmObjects
from music_recommendation.models.mxm_object import MxmObject, MxmAttribute

if __name__ == '__main__':
    dao_train: DAOMxmObjects = DAOMxmObjects('mxm_train')
    dao_test: DAOMxmObjects = DAOMxmObjects('mxm_test')

    # with open(
    #         ".\mxm_dataset_train.txt",
    #         'r') as f:
    #     for line in f.readlines():
    #         split_line: List[str] = line.split(',')
    #         msd_id: str = split_line[0]
    #         mxm_id: str = split_line[1]
    #         attr_list: List[MxmAttribute] = []
    #         for val in split_line[2:]:
    #             split_val: List[str] = val.split(':')
    #             attr_id: int = int(split_val[0])
    #             attr_value: int = int(split_val[1])
    #             attr: MxmAttribute = MxmAttribute(atrr_id=attr_id, atrr_value=attr_value)
    #             attr_list.append(attr)
    #         mxm_object: MxmObject = MxmObject(msd_id=msd_id, mxm_id=mxm_id, attr_list=attr_list)
    #         dao_train.insert_one(mxm_object)
    #
    # with open(
    #         ".\mxm_dataset_test.txt",
    #         'r') as f:
    #     for line in f.readlines():
    #         split_line: List[str] = line.split(',')
    #         msd_id: str = split_line[0]
    #         mxm_id: str = split_line[1]
    #         attr_list: List[MxmAttribute] = []
    #         for val in split_line[2:]:
    #             split_val: List[str] = val.split(':')
    #             attr_id: int = int(split_val[0])
    #             attr_value: int = int(split_val[1])
    #             attr: MxmAttribute = MxmAttribute(atrr_id=attr_id, atrr_value=attr_value)
    #             attr_list.append(attr)
    #         mxm_object: MxmObject = MxmObject(msd_id=msd_id, mxm_id=mxm_id, attr_list=attr_list)
    #         dao_test.insert_one(mxm_object)
