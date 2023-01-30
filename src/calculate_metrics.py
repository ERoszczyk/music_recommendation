from typing import List

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from dao.dao_msd_songs import DAOMsdSongs
from dao.dao_user_recommendation import DAOUserRecommendation
from models.user_recommendation import UserRecommendation

def database_data_to_dataframe(data):
    if not isinstance(data[0], dict):
        headers = data[0].dict().keys()
        data_values = [d.dict().values() for d in data]
    else:
        headers = data[0].keys()
        data_values = [d.values() for d in data]
    df = pd.DataFrame(data_values, columns=headers)
    return df

if __name__ == '__main__':
    dao_user_recommendation: DAOUserRecommendation = DAOUserRecommendation()
    user_recommendations: List[UserRecommendation] = dao_user_recommendation.find_all()

    dao_songs: DAOMsdSongs = DAOMsdSongs()
    songs_df = database_data_to_dataframe(dao_songs.find_all())
    songs_df = songs_df.drop_duplicates(subset=['song_id'])

    recommendation_list: List[List[str]] = [recommendation.recommendation_list for recommendation in
                                            user_recommendations]
    recommended_song_list: List[str] = []
    for user_recommendation in user_recommendations:
        recommended_song_list.extend(user_recommendation.recommendation_list)
    recommended_song_list = list(set(recommended_song_list))
    print(f'Percentage of songs recommended: {(len(recommended_song_list) / len(songs_df)) * 100}%')
    print(f'Maximal number of songs recommended: {len(user_recommendations) * 10}')
    print(f'Number of unique songs in songs_df: {len(songs_df)}')
    print(f'Number of unique songs recommended: {len(recommended_song_list)}')

    reccomendation_df = df = pd.DataFrame(recommendation_list)
    cos_sim = cosine_similarity(pd.get_dummies(reccomendation_df))
    ltri = np.tril(cos_sim, -1)
    print(ltri)
    ltri = ltri[np.nonzero(ltri)]
    print(f'Personalization: {1 - np.mean(ltri)}')

