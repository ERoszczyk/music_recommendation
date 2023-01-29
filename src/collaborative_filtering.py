from typing import List

import pandas as pd

from dao.dao_msd_songs import DAOMsdSongs
from dao.dao_msd_triplets import DAOMsdTriplets
from models.msd_song import MsdSong
from models.msd_triplet import MsdTriplet


def database_data_to_dataframe(data):
    headers = data[0].dict().keys()
    data_values = [d.dict().values() for d in data]
    df = pd.DataFrame(data_values, columns=headers)
    return df


def get_rating_from_listen_count(df, num1, num2, num3):
    ratings = []
    for count in list(df.listen_count):
        if count == num1:
            ratings.append(0)
        elif num1 < count <= num2:
            ratings.append(1)
        elif num2 < count <= num3:
            ratings.append(2)
        elif count > num3:
            ratings.append(3)
        else:
            raise ValueError()
    df['rating'] = ratings
    return df


def get_songs_rated_by_more_than_n_users(df, n):
    sort_df = df.sort_values(by=['ratings_amount'], inplace=False, ascending=False)
    return sort_df[sort_df['ratings_amount'] >= n]


def get_triplets_by_song_ids(triplets_df, song_df, num1=1, num2=7, num3=20):
    songs_ids = list(song_df['song_id'])
    ratings_df = get_rating_from_listen_count(triplets_df, num1, num2, num3)
    return ratings_df[(ratings_df['song_id'].isin(songs_ids))]


def get_matrix(triplets_df):
    return triplets_df.pivot_table(index='user_id', columns='song_id', values='rating')


def calculate_user_similarity(triplets_df, user_id, user_similarity_threshold=0.3):
    matrix = get_matrix(triplets_df)
    user_similarity = matrix.T.corr()
    similar_users_matrix = user_similarity.drop(index=user_id, inplace=False)
    similar_users = similar_users_matrix[similar_users_matrix[user_id] > user_similarity_threshold][
        user_id].sort_values(ascending=False)
    return similar_users


def get_recommended_song_info_df(songs_to_recommend, songs_df, n):
    songs_to_recommend_info = pd.DataFrame(columns=songs_df.columns.values)
    for song in songs_to_recommend[:n]:
        songs_to_recommend_info = songs_to_recommend_info.append(songs_df.loc[songs_df['song_id'] == song])
    return songs_to_recommend_info


def get_songs_to_recommend_for_user(triplets_df, user_id, songs_df, n=10):
    similar_users = calculate_user_similarity(triplets_df, user_id)
    users_songs_df = pd.DataFrame(columns=triplets_df.columns.values)
    for i in range(len(similar_users)):
        temp = triplets_df.loc[triplets_df['user_id'] == similar_users.index[i]]
        users_songs_df = users_songs_df.append(temp)
    songs_to_recommend = users_songs_df.sort_values('listen_count', ascending=False)['song_id']
    songs_to_recommend = songs_to_recommend.unique()
    return get_recommended_song_info_df(songs_to_recommend, songs_df, n)


def get_similar_users_songs(triplets_df, user_id, similar_users):
    matrix = get_matrix(triplets_df)
    target_user_songs = matrix[matrix.index == user_id].dropna(axis=1, how='all')
    similar_user_songs = matrix[matrix.index.isin(similar_users.index)].dropna(axis=1, how='all')
    similar_user_songs.drop(target_user_songs.columns, axis=1, inplace=True, errors='ignore')
    return similar_user_songs


def calculate_song_score(similar_user_songs, similar_users):
    song_scores = pd.DataFrame(columns=['song_id', 'total_score'])
    for song in similar_user_songs.columns:
        song_rating = similar_user_songs[song]
        total_rating = 0
        ratings_num = 0
        for user in similar_users.index:
            song_rating_by_user = song_rating[user]
            if not pd.isna(song_rating[user]):
                total_rating += similar_users[user] * song_rating_by_user
                ratings_num += 1
        song_scores = song_scores.append({"song_id": song, "total_score": total_rating / ratings_num},
                                         ignore_index=True)
    return song_scores


def get_songs_to_recommend_for_user_considering_user_similarity(triplets_df, user_id, songs_df, n=10):
    similar_users = calculate_user_similarity(triplets_df, user_id)
    similar_user_songs = get_similar_users_songs(triplets_df, user_id, similar_users)
    song_scores = calculate_song_score(similar_user_songs, similar_users)
    # songs_to_recommend = song_scores.sort_values('total_score', ascending=False)['song_id']
    # recommended_songs = get_recommended_song_info_df(songs_to_recommend, songs_df, n)
    # # Add score column
    # for song in recommended_songs['song_id']:
    #     recommended_songs.loc[recommended_songs['song_id'] == song, 'score'] = song_scores[
    #         song_scores['song_id'] == song]['total_score'].values[0]
    # recommended_songs['score'] = song_scores.sort_values('total_score', ascending=False)['total_score']
    return song_scores


if __name__ == '__main__':
    dao_triplets: DAOMsdTriplets = DAOMsdTriplets()
    dao_songs: DAOMsdSongs = DAOMsdSongs()

    triplets: List[MsdTriplet] = dao_triplets.find_all()
    triplets_df = database_data_to_dataframe(triplets)
    songs: List[MsdSong] = dao_songs.find_all()
    songs_df = database_data_to_dataframe(songs)

    ratings_amount = 100
    songs_100_ratings = get_songs_rated_by_more_than_n_users(songs_df, ratings_amount)
    triplets_df = get_triplets_by_song_ids(triplets_df, songs_100_ratings)

    # reduce df due to 43GiB memory allocation
    reduced_triplets_df = triplets_df[:100000]

    # get user_ids
    user_ids = list(reduced_triplets_df['user_id'].unique())
    # print(user_ids)

    user_id = '1260cde60645ca85f03991fdc60c217e7f4e5156'
    print("Recommendation for user: " + user_id)
    # similar_users = calculate_user_similarity(reduced_triplets_df, user_id)
    #
    # songs_to_recommend = get_songs_to_recommend_for_user(reduced_triplets_df, user_id)
    # print(f'The similar users for user {user_id} are', similar_users)
    # print(f'Songs recommended for user {user_id} are:')
    # index = 1
    # for i, song_info in songs_to_recommend.iterrows():
    #     print(f"{index}. {song_info['title']} by {song_info['artist_name']}")
    #     index += 1

    songs_to_recommend_considering_us = get_songs_to_recommend_for_user_considering_user_similarity(reduced_triplets_df,
                                                                                                    user_id, songs_df)
    print(f'Songs recommended for user {user_id} are:')
    index = 1
    for i, song_info in songs_to_recommend_considering_us.iterrows():
        print(f"{index}. {song_info['title']} by {song_info['artist_name']}")
        # print(
        #     f"{index}. {song_info['title']} by {song_info['artist_name']} with score: {songs_to_recommend_considering_us.loc[songs_to_recommend_considering_us['song_id'] == song_info['song_id']].iloc[0]['score']}")
        index += 1
