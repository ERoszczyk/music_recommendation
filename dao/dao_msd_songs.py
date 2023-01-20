from config import MONGO_CLIENT, MONGODB_DB_NAME
from dao.dao_base import DAOBase
from models.msd_song import MsdSong


class DAOMsdSongs(DAOBase):

    def __init__(self):
        super().__init__(MONGO_CLIENT,
                         MONGODB_DB_NAME,
                         "msd_songs",
                         MsdSong,
                         MsdSong)