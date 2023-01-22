# raw data files downloaded from http://millionsongdataset.com/musixmatch/

from typing import List

import pandas as pd

from dao.dao_mxm_labels import DAOMxmLabels
from dao.dao_sentiment_scores import DAOSentimentScores
from models.mxm_label import MxmLabel
from models.sentiment_score import SentimentScore


def read_data_from_database():
    dao_sentiment_scores: DAOSentimentScores = DAOSentimentScores()
    sentiment_scores: List[SentimentScore] = dao_sentiment_scores.find_all()
    return sentiment_scores


def database_data_to_dataframe():
    sentiment_scores = read_data_from_database()
    headers = sentiment_scores[0].dict().keys()
    sentiment_values = [score.dict().values() for score in sentiment_scores]
    sentiment_df = pd.DataFrame(sentiment_values, columns=headers)
    return sentiment_df


if __name__ == '__main__':
    dao_labels: DAOMxmLabels = DAOMxmLabels()
    sentiment_df = database_data_to_dataframe()
    labels = dao_labels.find_all()

    for label in labels:
        sentiment_score = sentiment_df[sentiment_df['word'] == label.attr_name]
        if len(sentiment_score) > 0:
            label.sentiment_score = sentiment_score.iloc[0]['sentiment_score']
            dao_labels.update_one(query={"attr_name": label.attr_name},
                                  values={"$set": {"sentiment_score": int(label.sentiment_score)}})
        else:
            dao_labels.update_one(query={"attr_name": label.attr_name}, values={"$set": {"sentiment_score": 0}})
