import numpy as np
import pandas as pd
from typing import List

from matplotlib import pyplot as plt

from dao.dao_mxm_labels import DAOMxmLabels
from dao.dao_mxm_objects import DAOMxmObjects
from dao.dao_sentiment_scores import DAOSentimentScores
from models.mxm_label import MxmLabel
from models.mxm_object import MxmObject
from models.sentiment_score import SentimentScore


def sig(x):
    return (1 / (1 + np.exp(-(1 / 8) * x))) * 2 - 1


def generate_sig_graph():
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    x = np.linspace(-50, 50, 1000)
    plt.plot(x, sig(x), color='red')
    plt.savefig('sigmoid.png')
    plt.show()


def create_dict_from_mxm_labels():
    dao_mxm_labels: DAOMxmLabels = DAOMxmLabels()
    mxm_labels: List[MxmLabel] = dao_mxm_labels.find_all()
    mxm_labels_dict = {}
    for mxm_label in mxm_labels:
        mxm_labels_dict[mxm_label.attr_id] = mxm_label.attr_name
    return mxm_labels_dict


def get_scores_from_mxm_label():
    dao_mxm_labels: DAOMxmLabels = DAOMxmLabels()
    mxm_labels: List[MxmLabel] = dao_mxm_labels.find_all()
    mxm_labels_dict = {}
    for mxm_label in mxm_labels:
        mxm_labels_dict[mxm_label.attr_id] = mxm_label.sentiment_score
    return mxm_labels_dict


def database_data_to_dataframe(data):
    headers = data[0].dict().keys()
    sentiment_values = [score.dict().values() for score in data]
    sentiment_df = pd.DataFrame(sentiment_values, columns=headers)
    return sentiment_df


def predict_all_songs():
    dao_mxm_objects: DAOMxmObjects = DAOMxmObjects("mxm_train")
    attr_translation_dict: dict = create_dict_from_mxm_labels()
    sentiment_scores_dict: dict = get_scores_from_mxm_label()
    dao_sentiment_scores: DAOSentimentScores = DAOSentimentScores()
    sentiment_score_from_db: List[SentimentScore] = dao_sentiment_scores.find_all()
    sentiment_df = database_data_to_dataframe(sentiment_score_from_db)

    mxm_objects: List[MxmObject] = dao_mxm_objects.find_all()
    count = 0
    for mxm_object in mxm_objects:
        count += 1
        if mxm_object.sentiment is None:
            sentiment = 0
            for mxm_label in mxm_object.attr_list:
                # word = attr_translation_dict[mxm_label.atrr_id]
                sentiment += sentiment_scores_dict[mxm_label.atrr_id] * mxm_label.atrr_value
                # try:
                #     sentiment_score = sentiment_df.loc[sentiment_df['word'] == word, 'sentiment_score']
                #     # sentiment_score: SentimentScore = dao_sentiment_scores.find_one_by_query({"word": word})
                #     if len(sentiment_score) > 0:
                #         sentiment += sentiment_score.iloc[0] * mxm_label.atrr_value
                #         # sentiment += sentiment_score. * mxm_label.atrr_value
                # except TypeError as e:
                #     pass
            # print(f'Song: {mxm_object.msd_id}, sentiment: {sentiment}')
            dao_mxm_objects.update_one(query={"msd_id": mxm_object.msd_id},
                                       values={"$set": {"sentiment": sig(sentiment)}})
        if count % 1000 == 0:
            print(f'Processed {count} songs')


if __name__ == '__main__':
    # dao_mxm_objects: DAOMxmObjects = DAOMxmObjects("mxm_train")
    predict_all_songs()
    # print(sig(-11))
    # print(sig(15))
    # print(sig(10000000))
