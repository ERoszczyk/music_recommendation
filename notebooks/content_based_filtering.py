from typing import List
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd

pd.options.mode.chained_assignment = None
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import sigmoid_kernel, cosine_similarity

from dao.dao_msd_songs_with_lyrics import DAOMsdSongsWithLyrics
from models.msd_song import MsdSongWithLyrics


def database_data_to_dataframe(data):
    headers = data[0].dict().keys()
    data_values = [d.dict().values() for d in data]
    df = pd.DataFrame(data_values, columns=headers)
    return df


def get_songs_with_lyrics_df(songs_df):
    songs_df = songs_df.dropna(subset='lyrics', inplace=False)
    songs_df['lyrics'] = songs_df['lyrics'].str.replace(r'\n', ' ')
    return songs_df


def calculate_tfidf_matrix(songs_df, reduce_n=20000):
    final_stopwords_list = stopwords.words('english') + stopwords.words('french') + stopwords.words(
        'spanish') + stopwords.words('swedish')
    tfidf = TfidfVectorizer(analyzer='word', stop_words=final_stopwords_list)
    songs_df = songs_df[:reduce_n]
    tfidf_matrix = tfidf.fit_transform(songs_df['lyrics'])
    return tfidf_matrix


def calculate_sigmoid_kernel(tfidf_matrix):
    return sigmoid_kernel(tfidf_matrix, tfidf_matrix)


def calculate_cosi_similarity_matrix(tfidf_matrix):
    return cosine_similarity(tfidf_matrix)


def get_songs_indices(songs_df):
    return pd.Series(songs_df.index, index=songs_df['title'])


def get_recommended_songs_based_on_sigmoid_kernel(song_name, songs_df, n=10):
    indices = get_songs_indices(songs_df)
    idx = indices[song_name]
    tfid_matrix = calculate_tfidf_matrix(songs_df)
    songs_sig = calculate_sigmoid_kernel(tfid_matrix)
    sig_scores = list(enumerate(songs_sig[idx]))
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
    sig_scores = sig_scores[1:n + 1]
    return sig_scores


def get_recommended_songs_based_on_cosine_similarity(song_name, songs_df, n=10):
    indices = get_songs_indices(songs_df)
    idx = indices[song_name]
    tfidf_matrix = calculate_tfidf_matrix(songs_df)
    songs_cos = calculate_cosi_similarity_matrix(tfidf_matrix)
    return songs_cos[idx].argsort()[::-1][1:n + 1]


def print_recommendations_based_on_sigmoid_kernel(song_name, songs_df, n=10):
    sig_scores = get_recommended_songs_based_on_sigmoid_kernel(song_name, songs_df, n)
    print(f'Recommendations for {song_name}:')
    for song_score in sig_scores:
        print(songs_df['title'].iloc[song_score[0]], songs_df['artist_name'].iloc[song_score[0]])


def print_recommendations_based_on_cosine_similarity(song_name, songs_df, n=10):
    cos_scores = get_recommended_songs_based_on_cosine_similarity(song_name, songs_df, n)
    print(f'Recommendations for {song_name}:')
    for song_score in cos_scores:
        print(songs_df['title'].iloc[song_score], songs_df['artist_name'].iloc[song_score])


if __name__ == '__main__':
    dao_songs_with_lyrics: DAOMsdSongsWithLyrics = DAOMsdSongsWithLyrics()
    songs: List[MsdSongWithLyrics] = dao_songs_with_lyrics.find_all()
    songs_df = database_data_to_dataframe(songs)
    songs_df = get_songs_with_lyrics_df(songs_df)
    print_recommendations_based_on_cosine_similarity('Before He Kissed Me', songs_df, 10)
