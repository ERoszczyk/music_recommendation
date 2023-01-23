from typing import List

import pandas as pd
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne

from dao.dao_msd_songs import DAOMsdSongs
from models.msd_song import MsdSong

if __name__ == "__main__":
    dao_songs: DAOMsdSongs = DAOMsdSongs()
    songs: List[MsdSong] = dao_songs.find_all()
    song_ratings_amount = pd.read_csv('../../1_interim/song_ratings_amount.csv', sep=",")
    print(song_ratings_amount.head())

    # count = 0
    # for song in songs:
    #     count += 1
    #     if song.ratings_amount is None:
    #         ratings_amount = song_ratings_amount[song_ratings_amount['song_id'] == song.song_id]['ratings_amount'].values[0]
    #         # song.ratings_amount = ratings_amount
    #         dao_songs.update_one({'song_id': song.song_id}, {'$set': {'ratings_amount': int(ratings_amount)}})
    # get all songs ids from df
    # song_ids = song_ratings_amount['song_id'].tolist()
    # for song_rating in song_ratings_amount.itertuples():
    #     song_id = song_rating[2]
    #     ratings_amount = song_rating[3]
    #     dao_songs.update_one({'song_id': song_id}, {'$set': {'ratings_amount': int(ratings_amount)}})
    list_of_updates: List[UpdateOne] = []
    for index, row in song_ratings_amount.iterrows():
        song_id = row['song_id']
        ratings_amount = row['ratings_amount']
        update_one: UpdateOne = UpdateOne({'song_id': song_id}, {'$set': {'ratings_amount': int(ratings_amount)}})
        list_of_updates.append(update_one)
    result = dao_songs.collection.bulk_write(list_of_updates)

    # for song_id in song_ids:
    #     # get ratings amount for song
    #     ratings_amount = song_ratings_amount.loc[song_ratings_amount['song_id'] == song_id, 'ratings_amount'].iloc[0]
    #     # update song ratings amount
    #     dao_songs.update_one({'song_id': song_id}, {'$set': {'ratings_amount': int(ratings_amount)}})
