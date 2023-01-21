# raw data files downloaded from https://www.kaggle.com/datasets/rtatman/sentiment-lexicons-for-81-languages

from typing import List
import csv
import os

from dao.dao_sentiment_scores import DAOSentimentScores
from dao.dao_sentiment_metadata import DAOSentimentMetadata
from models.sentiment_score import SentimentScore

if __name__ == '__main__':
    dao_sentiment_score: DAOSentimentScores = DAOSentimentScores()

    for filename in os.listdir('./sentiment-lexicons'):
        if filename.startswith('negative_words'):
            with open(os.path.join('./sentiment-lexicons', filename), 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    dao_sentiment_score.insert_one(SentimentScore(word=line.strip(), sentiment_score=-1))

        if filename.startswith('positive_words'):
            with open(os.path.join('./sentiment-lexicons', filename), 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    dao_sentiment_score.insert_one(SentimentScore(word=line.strip(), sentiment_score=1))

