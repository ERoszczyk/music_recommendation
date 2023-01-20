from config import MONGO_CLIENT, MONGODB_DB_NAME
from dao.dao_base import DAOBase
from models.mxm_object import MxmObject


class DAOMxmObjects(DAOBase):

    def __init__(self, train_or_test: str):
        super().__init__(MONGO_CLIENT,
                         MONGODB_DB_NAME,
                         train_or_test,
                         MxmObject,
                         MxmObject)