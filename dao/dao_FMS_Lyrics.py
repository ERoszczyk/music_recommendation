from music_recommendation.config import MONGO_CLIENT, MONGODB_DB_NAME
from music_recommendation.dao.dao_base import DAOBase
from music_recommendation.models.fms_lyrics import FMSLyrics


class DAOFMSLyrics(DAOBase):

    def __init__(self):
        super().__init__(MONGO_CLIENT,
                         MONGODB_DB_NAME,
                         "FMS_Lyrics",
                         FMSLyrics,
                         FMSLyrics)