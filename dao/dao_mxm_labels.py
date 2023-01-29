from config import MONGO_CLIENT, MONGODB_DB_NAME
from dao.dao_base import DAOBase
from models.mxm_label import MxmLabel


class DAOMxmLabels(DAOBase):

    def __init__(self):
        super().__init__(MONGO_CLIENT,
                         MONGODB_DB_NAME,
                         "mxm_labels",
                         MxmLabel,
                         MxmLabel)

    def get_dict_of_translations(self) -> dict:
        return {mxm_label.attr_id: mxm_label.attr_name for mxm_label in self.find_all()}