from config import MONGO_CLIENT, MONGODB_DB_NAME
from dao.dao_base import DAOBase
from models.sentiment_score import SentimentScore


class DAOSentimentScores(DAOBase):

    def __init__(self):
        super().__init__(MONGO_CLIENT,
                         MONGODB_DB_NAME,
                         "sentiment_score",
                         SentimentScore,
                         SentimentScore)