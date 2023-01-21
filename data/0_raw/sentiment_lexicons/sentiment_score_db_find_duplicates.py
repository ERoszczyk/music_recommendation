# raw data files downloaded from https://www.kaggle.com/datasets/rtatman/sentiment-lexicons-for-81-languages

from typing import List
import csv
import os
import pandas as pd

from dao.dao_sentiment_scores import DAOSentimentScores
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


def drop_collection():
    dao_sentiment_scores: DAOSentimentScores = DAOSentimentScores()
    dao_sentiment_scores.collection.drop()


def insert_data_to_database_from_dataframe(df):
    dao_sentiment_scores: DAOSentimentScores = DAOSentimentScores()
    for index, row in df.iterrows():
        dao_sentiment_scores.insert_one(SentimentScore(word=row['word'], sentiment_score=row['sentiment_score']))


def get_words_list(df):
    words_list = []
    for index, row in df.iterrows():
        words_list.append(row['word'])
    return words_list


def get_duplicates(df):
    return df[df.word.duplicated() == True]


def get_unique_duplicated_values(df):
    return df.word.unique().tolist()


if __name__ == '__main__':
    sentiment_df = database_data_to_dataframe()
    # Drop duplicated rows
    sentiment_df_without_duplicates = sentiment_df.drop_duplicates(keep='first')
    duplicated_df = get_duplicates(sentiment_df_without_duplicates)
    unique_duplicates_values = get_unique_duplicated_values(duplicated_df)
    sentiment_df_without_duplicates = sentiment_df_without_duplicates.drop_duplicates(subset=['word'], keep=False)
    drop_collection()
    insert_data_to_database_from_dataframe(sentiment_df_without_duplicates)
