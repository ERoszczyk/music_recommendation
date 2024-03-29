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


def get_songs_with_lyrics_df(songs_with_lyrics_df):
    songs_with_lyrics_df = songs_with_lyrics_df.dropna(subset='lyrics', inplace=False)
    songs_with_lyrics_df['lyrics'] = songs_with_lyrics_df['lyrics'].str.replace(r'\n', ' ')
    return songs_with_lyrics_df


def calculate_tfidf_matrix(songs_with_lyrics_df, reduce_n=20000):
    final_stopwords_list = stopwords.words('english') + stopwords.words('french') + stopwords.words(
        'spanish') + stopwords.words('swedish')
    tfidf = TfidfVectorizer(analyzer='word', stop_words=final_stopwords_list)
    tfidf_matrix = tfidf.fit_transform(songs_with_lyrics_df['lyrics'])
    return tfidf_matrix


def calculate_sigmoid_kernel(tfidf_matrix):
    return sigmoid_kernel(tfidf_matrix)


def calculate_cosi_similarity_matrix(tfidf_matrix):
    return cosine_similarity(tfidf_matrix)


def get_songs_indices(songs_with_lyrics_df):
    return pd.Series(songs_with_lyrics_df.index, index=songs_with_lyrics_df['song_id']).drop_duplicates()


def tuples_list_to_df(tuples_list):
    df = pd.DataFrame(tuples_list, columns=['song_idx', 'total_score'])
    df = df.set_index('song_idx')
    return df


def get_recommended_songs_based_on_sigmoid_kernel(songs_ids, songs_with_lyrics_df, n=10):
    indices = get_songs_indices(songs_with_lyrics_df)
    tfid_matrix = calculate_tfidf_matrix(songs_with_lyrics_df)
    songs_sig = calculate_sigmoid_kernel(tfid_matrix)
    sig_scores_df = pd.DataFrame(columns=['song_idx', 'total_score'])
    sig_scores_df = sig_scores_df.set_index('song_idx')

    for song_id in songs_ids:
        if song_id in indices.index:
            idx = indices[song_id]
            temp_df = pd.DataFrame(songs_sig[idx], columns=['total_score'])
            sig_scores_df = sig_scores_df.add(temp_df, fill_value=0)
            # sig_scores = list(enumerate(songs_sig[idx]))
            # temp_df = tuples_list_to_df(sig_scores)
            # sig_scores_df = sig_scores_df.add(temp_df, fill_value=0)
    sig_scores_df['song_id'] = songs_with_lyrics_df['song_id']
    # sig_scores_df = sig_scores_df.sort_values(by='score', ascending=False)
    # sig_scores_df = sig_scores_df[1:n + 1]
    sig_scores_df.set_index('song_id', inplace=True)
    return sig_scores_df


def get_recommended_songs_based_on_cosine_similarity(songs_ids, songs_with_lyrics_df, n=10):
    indices = get_songs_indices(songs_with_lyrics_df)
    tfidf_matrix = calculate_tfidf_matrix(songs_with_lyrics_df)
    songs_cos = calculate_cosi_similarity_matrix(tfidf_matrix)
    cos_scores_df = pd.DataFrame(columns=['total_score'])
    for song_id in songs_ids:
        if song_id in indices.index:
            idx = indices[song_id]
            temp_df = pd.DataFrame(songs_cos[idx], columns=['total_score'])
            cos_scores_df = cos_scores_df.add(temp_df, fill_value=0)
    cos_scores_df['song_id'] = songs_with_lyrics_df['song_id']
    cos_scores_df.set_index('song_id', inplace=True)
    # cos_scores_df = cos_scores_df.sort_values(by='score', ascending=False)
    # cos_scores_df = cos_scores_df[1:n + 1]
    return cos_scores_df


def print_recommendations_based_on_sigmoid_kernel(songs_ids, songs_with_lyrics_df, n=10):
    sig_scores_df = get_recommended_songs_based_on_sigmoid_kernel(songs_ids, songs_with_lyrics_df, n)
    print(f'Recommendations for {songs_ids}:')
    for index, song_score in sig_scores_df.iterrows():
        print(songs_with_lyrics_df['title'].iloc[index], songs_with_lyrics_df['artist_name'].iloc[index])


def print_recommendations_based_on_cosine_similarity(songs_ids, songs_with_lyrics_df, n=10):
    cos_scores_df = get_recommended_songs_based_on_cosine_similarity(songs_ids, songs_with_lyrics_df, n)
    print(f'Recommendations for {songs_ids}:')
    for index, song_score in cos_scores_df.iterrows():
        print(songs_with_lyrics_df['title'].iloc[index], songs_with_lyrics_df['artist_name'].iloc[index])


if __name__ == '__main__':
    dao_songs_with_lyrics: DAOMsdSongsWithLyrics = DAOMsdSongsWithLyrics()
    songs: List[MsdSongWithLyrics] = dao_songs_with_lyrics.find_all()
    songs_with_lyrics_df = database_data_to_dataframe(songs)
    songs_with_lyrics_df = get_songs_with_lyrics_df(songs_with_lyrics_df)
    print_recommendations_based_on_cosine_similarity(['SOBDLRM12A8C13A0AC', 'SODVOFJ12AB0181EE6'], songs_with_lyrics_df,
                                                     10)
