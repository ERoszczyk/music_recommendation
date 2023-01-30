from typing import List

from pydantic import BaseModel


class UserRecommendation(BaseModel):
    user_id: str
    recommendation_list: List[str]


if __name__ == '__main__':

    user_rec = UserRecommendation(user_id='123', recommendation_list=['123', '456'])
    print(user_rec)
    print(user_rec.json())
    print(user_rec.dict())
    print(user_rec.dict(by_alias=True))
    print(user_rec.dict(by_alias=True, exclude_unset=True))
