from config import MONGO_CLIENT, MONGODB_DB_NAME
from dao.dao_base import DAOBase
from models.user_recommendation import UserRecommendation


class DAOUserRecommendation(DAOBase):

    def __init__(self):
        super().__init__(MONGO_CLIENT,
                         MONGODB_DB_NAME,
                         "user_recommendation",
                         UserRecommendation,
                         UserRecommendation)