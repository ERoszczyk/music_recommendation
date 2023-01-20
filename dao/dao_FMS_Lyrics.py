from config import MONGO_CLIENT, MONGODB_DB_NAME
from dao.dao_base import DAOBase
from models.fms_lyrics import FMSLyrics


class DAOFMSLyrics(DAOBase):

    def __init__(self):
        super().__init__(MONGO_CLIENT,
                         MONGODB_DB_NAME,
                         "FMS_Lyrics",
                         FMSLyrics,
                         FMSLyrics)