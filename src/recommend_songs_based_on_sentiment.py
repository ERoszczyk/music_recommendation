from typing import List

import pandas as pd

from dao.dao_msd_songs import DAOMsdSongs
from dao.dao_msd_songs_with_lyrics import DAOMsdSongsWithLyrics
from dao.dao_msd_triplets import DAOMsdTriplets
from dao.dao_mxm_objects import DAOMxmObjects
from models.msd_song import MsdSong
from models.msd_triplet import MsdTriplet
from models.mxm_object import MxmObject


def database_data_to_dataframe(data):
    headers = data[0].dict().keys()
    data_values = [d.dict().values() for d in data]
    df = pd.DataFrame(data_values, columns=headers)
    return df


def get_songs_user_has_listened_to(triplets_df, user_id):
    return triplets_df.loc[triplets_df['user_id'] == user_id, 'song_id']


def calculate_sentiment_difference(mxm_objects_df, user_songs):
    sentiment_diff_df = mxm_objects_df.copy()
    sentiment_diff_df.drop(mxm_objects_df.loc[mxm_objects_df['msd_id_true'].isin(user_songs)].index, inplace=True)
    sentiment_diff_df['sentiment_diff'] = 0
    for song in user_songs:
        song_sentiment = mxm_objects_df.loc[mxm_objects_df['msd_id_true'] == song, 'sentiment']
        # df[df['line_race']==0].index
        sentiment_diff_df['sentiment_diff'] = sentiment_diff_df['sentiment_diff'].add(
            (mxm_objects_df['sentiment'] - song_sentiment.values[0]).abs())
    return sentiment_diff_df


def get_songs_to_recommend(user_songs, mxm_objects_df, n=10):
    sentiment_diff_df = calculate_sentiment_difference(mxm_objects_df, user_songs)
    return sentiment_diff_df.sort_values(by=['sentiment_diff'], inplace=False, ascending=True).head(n)


def print_recommendation(recommendation_df, songs_df):
    for msd_id in recommendation_df['msd_id_true']:
        print(songs_df.loc[songs_df['song_id'] == msd_id, 'title'].values[0], 'by',
              songs_df.loc[songs_df['song_id'] == msd_id, 'artist_name'].values[0])


if __name__ == '__main__':
    dao_mxm_objects: DAOMxmObjects = DAOMxmObjects("mxm_train")
    mxm_objects: List[MxmObject] = dao_mxm_objects.find_all()
    mxm_objects_df = database_data_to_dataframe(mxm_objects)

    dao_songs: DAOMsdSongs = DAOMsdSongs()
    songs: List[MsdSong] = dao_songs.find_all()
    songs_df = database_data_to_dataframe(songs)

    # As there are none songs from mxm, I'll create list of user_song manually
    user_songs = mxm_objects_df.sample(n=25)
    user_songs = user_songs['msd_id_true'].to_list()
    recommendation_df = get_songs_to_recommend(user_songs, mxm_objects_df)
    print_recommendation(recommendation_df, songs_df)
