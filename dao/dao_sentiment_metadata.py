from config import MONGO_CLIENT, MONGODB_DB_NAME
from dao.dao_base import DAOBase
from models.sentiment_metadata import SentimentMetadata


class DAOSentimentMetadata(DAOBase):

    def __init__(self):
        super().__init__(MONGO_CLIENT,
                         MONGODB_DB_NAME,
                         "sentiment_metadata",
                         SentimentMetadata,
                         SentimentMetadata)