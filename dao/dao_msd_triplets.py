from music_recommendation.config import MONGO_CLIENT, MONGODB_DB_NAME
from music_recommendation.dao.dao_base import DAOBase
from music_recommendation.models.msd_song import MsdSong
from music_recommendation.models.msd_triplet import MsdTriplet


class DAOMsdTriplets(DAOBase):

    def __init__(self):
        super().__init__(MONGO_CLIENT,
                         MONGODB_DB_NAME,
                         "msd_triplets",
                         MsdTriplet,
                         MsdTriplet)