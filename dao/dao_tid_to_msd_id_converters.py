from config import MONGO_CLIENT, MONGODB_DB_NAME
from dao.dao_base import DAOBase
from models.tid_to_msd_id_converter import TidToMsdIdConverter


class DAOTidToMsdIdConverter(DAOBase):

    def __init__(self):
        super().__init__(MONGO_CLIENT,
                         MONGODB_DB_NAME,
                         "tid_to_msd_id",
                         TidToMsdIdConverter,
                         TidToMsdIdConverter)