from music_recommendation.config import MONGO_CLIENT, MONGODB_DB_NAME
from music_recommendation.dao.dao_base import DAOBase
from music_recommendation.models.msd_song import MsdSongWithLyrics


class DAOMsdSongsWithLyrics(DAOBase):

    def __init__(self):
        super().__init__(MONGO_CLIENT,
                         MONGODB_DB_NAME,
                         "msd_songs_with_lyrics",
                         MsdSongWithLyrics,
                         MsdSongWithLyrics)