# raw data files downloaded from http://millionsongdataset.com/sites/default/files/AdditionalFiles/unique_tracks.txt

from typing import List

import pandas as pd

from dao.dao_mxm_labels import DAOMxmLabels
from dao.dao_mxm_objects import DAOMxmObjects
from dao.dao_sentiment_scores import DAOSentimentScores
from dao.dao_tid_to_msd_id_converters import DAOTidToMsdIdConverter
from models.mxm_label import MxmLabel
from models.mxm_object import MxmObject
from models.sentiment_score import SentimentScore
from models.tid_to_msd_id_converter import TidToMsdIdConverter


def read_data_from_database(dao_mxm_objects):
    # dao_mxm_objects: DAOMxmObjects = DAOMxmObjects("mxm_train")
    mxm_objects: List[MxmObject] = dao_mxm_objects.find_all()
    return mxm_objects

def database_data_to_dataframe(dao_mxm_objects):
    mxm_objects = read_data_from_database(dao_mxm_objects)
    headers = mxm_objects[0].dict().keys()
    mxm_values = [obj.dict().values() for obj in mxm_objects]
    mxm_objects_df = pd.DataFrame(mxm_values, columns=headers)
    return mxm_objects_df


if __name__ == '__main__':
    dao_mxm_objects: DAOMxmObjects = DAOMxmObjects("mxm_train")
    mxm_objects_df = database_data_to_dataframe(dao_mxm_objects)
    msd_ids = mxm_objects_df['msd_id'].to_list()

    updated = 0
    cos_znalazlem = False
    df = pd.read_csv("unique_tracks.txt", sep="<SEP>", names=["tid", "msd_id", "artist_name", "title"])
    df = df.loc[df['tid'].isin(msd_ids)]
    print(len(df))
    count = 0
    for index, row in df.iterrows():
        dao_mxm_objects.update_one(query={"msd_id": row['tid']},
                                   values={"$set": {"msd_id_true": row['msd_id']}})
        count += 1
        if count % 1000 == 0:
            print(count)
    # with open(
    #         ".\\unique_tracks.txt",
    #         'r', encoding='utf-8') as f:
    #     for line in f.readlines():
    #         split_line: List[str] = line.split('<SEP>')
    #         tid: str = split_line[0]
    #
    #         msd_id: str = split_line[1]
    #         result = dao_mxm_objects.update_one({"msd_id": tid}, {'$set': {"msd_id_true": msd_id}})
    #         updated+=1
    #         if updated%1000 == 0:
    #             print(updated)
    #         if result != 0:
    #             if not cos_znalazlem:
    #                 print("Znalazlem cos")
    #             cos_znalazlem = True
            # artist_name: str = split_line[2]
            # title: str = split_line[3]
            # tid_to_msd_id_converter: TidToMsdIdConverter = TidToMsdIdConverter(tid=tid, msd_id=msd_id,
            #                                                                    artist_name=artist_name, title=title)
            # dao_train.insert_one(tid_to_msd_id_converter)
