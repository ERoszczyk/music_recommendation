# python -m streamlit run ./src/main.py
import numpy as np
import streamlit as st
from typing import List

import pandas as pd
import time

from sklearn.preprocessing import MinMaxScaler

from dao.dao_msd_songs import DAOMsdSongs
from dao.dao_msd_songs_with_lyrics import DAOMsdSongsWithLyrics
from dao.dao_msd_triplets import DAOMsdTriplets
from dao.dao_mxm_objects import DAOMxmObjects
from models.msd_song import MsdSong, MsdSongWithLyrics
from models.msd_triplet import MsdTriplet
from models.mxm_object import MxmObject
from services.sentiment_prediction import create_dict_from_mxm_labels
from src.RecommendationSystem import RecommendationSystem
from src.content_based_filtering import get_songs_with_lyrics_df


def database_data_to_dataframe(data):
    if not isinstance(data[0], dict):
        headers = data[0].dict().keys()
        data_values = [d.dict().values() for d in data]
    else:
        headers = data[0].keys()
        data_values = [d.values() for d in data]
    df = pd.DataFrame(data_values, columns=headers)
    return df


@st.cache(allow_output_mutation=True)
def load_data():
    start = time.time()
    dao_triplets: DAOMsdTriplets = DAOMsdTriplets()
    triplets_df = database_data_to_dataframe(dao_triplets.find_all())

    dao_songs: DAOMsdSongs = DAOMsdSongs()
    songs_df = database_data_to_dataframe(dao_songs.find_all())

    dao_songs_with_lyrics: DAOMsdSongsWithLyrics = DAOMsdSongsWithLyrics()
    # songs_with_lyrics: List[MsdSongWithLyrics] = dao_songs_with_lyrics.find_all()
    songs_with_lyrics_df = database_data_to_dataframe(dao_songs_with_lyrics.find_all()[:1000])
    songs_with_lyrics_df = get_songs_with_lyrics_df(songs_with_lyrics_df)

    dao_mxm_objects: DAOMxmObjects = DAOMxmObjects("mxm")
    mxm_objects_df = database_data_to_dataframe(dao_mxm_objects.find_all())
    mxm_labels_dict = create_dict_from_mxm_labels()
    mxm_readable = dao_mxm_objects.get_all_readable_form(mxm_labels_dict)
    mxm_objects_readable_df = database_data_to_dataframe(mxm_readable)
    end = time.time()
    print("Czas wczytania danych: ", end - start)

    return triplets_df, songs_df, songs_with_lyrics_df, mxm_objects_df, mxm_objects_readable_df


def st_show_datasets(triplets_df, songs_df, songs_with_lyrics_df, mxm_objects_df):
    st.write("""
    ## Zbiory danych wykorzystane do projektu:
    Zbiór danych sesji użytkowników:""")
    st.write(triplets_df[:1000])
    st.write("""
    Zbiór danych utworów (Million Song Dataset):""")
    st.write(songs_df.drop('ratings_amount', axis=1)[:1000])
    st.write("""
    Zbiór danych utworów (Million Song Dataset) z tekstem piosenki:""")
    # reduced_songs_with_lyrics_df = songs_with_lyrics_df[:100000]
    songs_with_lyrics_df = songs_with_lyrics_df.drop('ratings_amount', axis=1)
    st.write(songs_with_lyrics_df[:1000])
    st.write("""
    Zbiór danych utworów z tzw. workami słów:""")
    st.write(mxm_objects_df[:1000])


def get_songs_user_listened_to(triplets_df, user_id):
    user_triplets_df = triplets_df[triplets_df['user_id'] == user_id]
    return user_triplets_df


def st_selectbox_user_id_where_songs_in_songs_with_lyrics_df(triplets_df, songs_with_lyrics_df):
    user_id = st.selectbox(
        'Wybierz użytkownika:',
        triplets_df.loc[triplets_df['song_id'].isin(songs_with_lyrics_df['song_id'])]['user_id'].unique())
    st.write('Wybrany użytkownik:', user_id)
    st.write('Sesje użytkownika:', get_songs_user_listened_to(triplets_df, user_id))
    # st.write('Teksty piosenek użytkownika:', songs_with_lyrics_df.loc[songs_with_lyrics_df['song_id'].isin(
    #     get_songs_user_listened_to(triplets_df, user_id)['song_id'])])
    return user_id


def st_selectbox_user_id(triplets_df):
    user_id = st.selectbox(
        'Wybierz użytkownika:',
        triplets_df['user_id'].unique())
    st.write('Wybrany użytkownik:', user_id)
    st.write('Sesje użytkownika:', get_songs_user_listened_to(triplets_df, user_id))
    return user_id


def st_recommendation_system_methods_checkbox(recommendation_system):
    st.write('Wybierz metody rekomendacji:')
    recommendation_system.set_collaborative_filtering(st.checkbox('Filtrowanie oparte na współpracy', value=True))
    recommendation_system.set_tfidf_algorithm(st.checkbox('Algorytm TF-IDF', value=True))
    recommendation_system.set_sentiment_recommendation(
        st.checkbox('Wydźwięk emocjonalny', value=False))
    recommendation_system.set_word2vec(st.checkbox('Word2vec', value=False))
    st.write('Opcje rekomendacji:')
    recommendation_system.set_show_time(st.checkbox('Pokaż czas generowania rekomendacji', value=False))
    if_show_datasets = st.checkbox('Pokaż zbiory danych użyte do wygenerowania rekomendacji', value=False)
    return if_show_datasets


def get_recommended_song_info_df(songs_to_recommend, songs_df, n):
    songs_to_recommend_info = pd.DataFrame(columns=songs_df.columns.values)
    songs_to_recommend.sort_values(by=['score'], ascending=False, inplace=True)
    for song in songs_to_recommend['song_id'].tolist()[:n]:
        songs_to_recommend_info = songs_to_recommend_info.append(songs_df.loc[songs_df['song_id'] == song])
    return songs_to_recommend_info


def show_songs_user_listened_to(triplets_df, user_id, songs_df):
    st.write('Użytkownik', user_id, 'posłuchał następujących utworów:')
    songs_df = songs_df.drop('ratings_amount', axis=1)
    st.write(songs_df.loc[songs_df['song_id'].isin(get_songs_user_listened_to(triplets_df, user_id)['song_id'])])


def show_datasets(songs_with_lyrics_df, mxm_objects_df, user_songs):
    if if_show_datasets:
        st.write("""
        Zbiór danych przesłuchanych przez użytkownika utworów (Million Song Dataset) z tekstem piosenki:""")
        songs_with_lyrics_df = songs_with_lyrics_df.drop('ratings_amount', axis=1)
        st.write(songs_with_lyrics_df.loc[songs_with_lyrics_df['song_id'].isin(user_songs)])
        st.write("""
        Zbiór danych przesłuchanych przez użytkownika utworów z tzw. workami słów:""")
        st.write(mxm_objects_df.loc[mxm_objects_df['msd_id_true'].isin(user_songs)])


def show_recommendations(recommendation_system, songs_df, triplets_df, user_id, n):
    st.write('Rekomendacje dla użytkownika:', user_id)
    songs_to_recommend = recommendation_system.get_recommendations()
    thresh = len(songs_to_recommend) - (len(songs_to_recommend) - 2)
    songs_to_recommend = songs_to_recommend.dropna(thresh=thresh)
    for column in songs_to_recommend.columns:
        if column != 'song_id':
            songs_to_recommend[column] = MinMaxScaler().fit_transform(
                np.array(songs_to_recommend[column]).reshape(-1, 1))
    songs_to_recommend.drop(songs_to_recommend.loc[songs_to_recommend['song_id'].isin(
        get_songs_user_listened_to(triplets_df, user_id)['song_id'])].index, inplace=True)
    # sentiment_diff_df.drop(mxm_objects_df.loc[mxm_objects_df['msd_id_true'].isin(user_songs)].index, inplace=True)
    songs_to_recommend['score'] = songs_to_recommend.mean(axis=1, skipna=True)
    index = 1
    songs_to_recommend = get_recommended_song_info_df(songs_to_recommend, songs_df, n)
    for i, song_info in songs_to_recommend.iterrows():
        st.write(index, song_info['title'], song_info['artist_name'])
        # print(f"{index}. {song_info['title']} by {song_info['artist_name']}")
        index += 1


if __name__ == '__main__':
    triplets_df, songs_df, songs_with_lyrics_df, mxm_objects_df, mxm_objects_readable_df = load_data()

    st.write("""
    # Rekomendacje muzyki za pomocą metod sztucznej inteligencji
    """)
    st_show_datasets(triplets_df, songs_df, songs_with_lyrics_df, mxm_objects_readable_df)
    reduce_triplets_by_rows = 100000
    user_id = st_selectbox_user_id_where_songs_in_songs_with_lyrics_df(triplets_df[:reduce_triplets_by_rows],
                                                                       songs_with_lyrics_df)
    recommendation_system = RecommendationSystem(user_id, triplets_df, songs_df, mxm_objects_df, songs_with_lyrics_df,
                                                 reduce_songs_by_ratings_amount=100,
                                                 reduce_triplets_by_rows=reduce_triplets_by_rows)
    if_show_datasets = st_recommendation_system_methods_checkbox(recommendation_system)
    is_submit = st.button('Wygeneruj rekomendacje')
    if is_submit:
        if if_show_datasets:
            user_songs = get_songs_user_listened_to(triplets_df, user_id)['song_id']
            show_songs_user_listened_to(triplets_df, user_id, songs_df)
            show_datasets(songs_with_lyrics_df, mxm_objects_readable_df, user_songs.tolist())
        show_recommendations(recommendation_system, songs_df, triplets_df, user_id, 10)
