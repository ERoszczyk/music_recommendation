import statistics
from scipy import sparse
from typing import Tuple, List

import numpy as np
import pandas as pd
# from gensim.models import KeyedVectors
from gensim.parsing.preprocessing import remove_stopwords
from sklearn.metrics.pairwise import cosine_similarity

# from config import GOOGLE_WORD2VEC_MODEL_PATH

# model = KeyedVectors.load_word2vec_format(GOOGLE_WORD2VEC_MODEL_PATH, binary=True)
# Not to import the model every time
model = None


def get_similarity_between_words(word1, word2):
    word1 = word1.lower()
    word2 = word2.lower()
    try:
        return model.similarity(word1, word2)
    except:
        return -1


def _preprocess_sentence(sentence) -> List[str]:
    sentence = remove_stopwords(sentence).replace(',', "").replace('.', "").lower()
    sentence_split = sentence.split(' ')
    return sentence_split


def get_stats_of_vector_of_sentence(sentence: str) -> Tuple[np.array, np.array, np.array]:
    sentence_split = _preprocess_sentence(sentence)
    if len(sentence_split) == 0:
        return np.zeros(300), np.zeros(300), np.zeros(300)

    values = []
    for word in sentence_split:
        try:
            values.append(model[word])
        except:
            values.append(np.zeros(300))

    try:
        sentence_mean = np.mean(values, axis=0)
    except statistics.StatisticsError:
        sentence_mean = np.zeros(300)

    try:
        sentence_median = np.median(values, axis=0)
    except statistics.StatisticsError:
        sentence_median = np.zeros(300)

    try:
        sentence_variance = np.var(values, axis=0)
    except statistics.StatisticsError:
        sentence_variance = np.zeros(300)

    return sentence_mean, sentence_median, sentence_variance


def get_mean_of_vector_of_sentence(sentence: str, for_base_model: bool = False):
    sentence_split = _preprocess_sentence(sentence)
    if len(sentence_split) == 0:
        return np.zeros(300)

    values = []
    for word in sentence_split:
        try:
            values.append(model[word])
        except:
            values.append(np.zeros(300))

    try:
        sentence_mean = np.mean(values, axis=0)
    except statistics.StatisticsError:
        sentence_mean = np.zeros(300)
    if not for_base_model:
        return sentence_mean
    else:
        return sentence_mean.tolist()

def get_songs_indices(df, column_name):
    return pd.Series(df.index, index=df[column_name]).drop_duplicates()

def tuples_list_to_df(tuples_list, column_name):
    df = pd.DataFrame(tuples_list, columns=['song_idx', column_name])
    df = df.set_index('song_idx')
    return df

def get_similarity_between_vectors(vector1, vector2):
    array1 = np.array(vector1, dtype=np.float32)
    array2 = np.array(vector2, dtype=np.float32)
    return cosine_similarity([array1, array2])[0][1]
    # return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))


def get_songs_by_word2vec(msd_ids_df, mxm_objects_df, songs_with_lyrics_df, user_songs):
    # word2vec_sim_df = msd_ids_df
    mxm_objects_df = mxm_objects_df[:18000]
    lyrics_indices = get_songs_indices(songs_with_lyrics_df, 'song_id')
    mxm_indices = get_songs_indices(mxm_objects_df, 'msd_id_true')
    # word2vec_sim_df.drop(mxm_objects_df.loc[mxm_objects_df['msd_id_true'].isin(user_songs)].index, inplace=True)
    # word2vec_sim_df.drop(songs_with_lyrics_df.loc[songs_with_lyrics_df['song_id'].isin(user_songs)].index,
    #                      inplace=True)
    # word2vec_sim_df['word2vec_sim'] = np.nan
    # word2vec_sim_lyrics_df = songs_with_lyrics_df[['song_id']].copy()
    # # word2vec_sim_lyrics_df.drop(songs_with_lyrics_df.loc[songs_with_lyrics_df['song_id'].isin(user_songs)].index,
    # #                             inplace=True)
    # word2vec_sim_lyrics_df['word2vec_sim'] = np.nan
    word2vec_sim_lyrics_df = pd.DataFrame(columns=['song_idx', 'word2vec_sim_lyrics'])
    word2vec_sim_lyrics_df = word2vec_sim_lyrics_df.set_index('song_idx')
    word2vec_sim_mxm_df = pd.DataFrame(columns=['song_idx', 'word2vec_sim_mxm'])
    word2vec_sim_mxm_df = word2vec_sim_mxm_df.set_index('song_idx')
    # word2vec_sim_mxm_df = mxm_objects_df[['msd_id_true']].copy()
    # word2vec_sim_mxm_df.drop(mxm_objects_df.loc[mxm_objects_df['msd_id_true'].isin(user_songs)].index, inplace=True)
    # word2vec_sim_mxm_df['word2vec_sim'] = np.nan
    mxm_ids = mxm_objects_df['msd_id_true'].tolist()
    songs_with_lyrics_ids = songs_with_lyrics_df['song_id'].tolist()
    songs_with_lyrics_cosine_sim = cosine_similarity(np.vstack(songs_with_lyrics_df['representation_vector']))# cosine_similarity(np.array(songs_with_lyrics_df['representation_vector'], dtype=np.float32))
    # print(songs_with_lyrics_cosine_sim)
    songs_with_lyrics_cosine_sim = sparse.csr_matrix(songs_with_lyrics_cosine_sim)
    mxm_cosine_sim = cosine_similarity(np.vstack(mxm_objects_df['representation_vector']))
    mxm_cosine_sim = sparse.csr_matrix(mxm_cosine_sim)
    for song in user_songs:
        if song in songs_with_lyrics_ids:
            word2vec_sim_lyrics_df.fillna(0, inplace=True)
            # score = list(enumerate(lyrics_indices[song]))
            temp_df = pd.DataFrame((songs_with_lyrics_cosine_sim[lyrics_indices[song]]).data, columns=['word2vec_sim_lyrics'])

            word2vec_sim_lyrics_df = word2vec_sim_lyrics_df.add(temp_df, fill_value=0)

        elif song in mxm_ids:
            word2vec_sim_mxm_df.fillna(0, inplace=True)
            # print(mxm_cosine_sim)
            temp_df = pd.DataFrame(mxm_cosine_sim[mxm_indices[song]].data, columns=['word2vec_sim_mxm'])

            # print(temp_df)
            word2vec_sim_mxm_df = word2vec_sim_mxm_df.add(temp_df, fill_value=0)
            # song_word2vec_representation = songs_with_lyrics_df.loc[
            #     songs_with_lyrics_df['song_id'] == song, 'representation_vector']
            # for index, row in songs_with_lyrics_df.iterrows():
            #     word2vec_sim_df.loc[
            #         word2vec_sim_df['song_id'] == row['song_id'], 'word2vec_sim'] = get_similarity_between_vectors(
            #         row['representation_vector'],
            #         song_word2vec_representation.values[0])
            # word2vec_sim_df['word2vec_sim'] = word2vec_sim_df['word2vec_sim'].add(
            #     get_similarity_between_vectors(songs_with_lyrics_df['representation_vector'],
            #                                    song_word2vec_representation))
        # elif song in mxm_ids:
        #     word2vec_sim_mxm_df.fillna(0, inplace=True)
        #     print(type(mxm_cosine_sim))
        #     print(mxm_cosine_sim[mxm_indices[song]])
        #     print("DUUUUUUUUUUUUUUUUUUUUUpa")
        #     print(mxm_cosine_sim[mxm_indices[song]])
        #     score = list(enumerate(mxm_cosine_sim[mxm_indices[song]]))
        #     temp_df = tuples_list_to_df(score, 'word2vec_sim')
        #     # temp_df = pd.DataFrame(mxm_cosine_sim[mxm_indices[song]], columns=['word2vec_sim'])
        #     word2vec_sim_mxm_df = word2vec_sim_mxm_df.add(temp_df, fill_value=0)
            # song_word2vec_representation = mxm_objects_df.loc[
            #     mxm_objects_df['msd_id_true'] == song, 'representation_vector']
            # for index, row in mxm_objects_df.iterrows():
            #     word2vec_sim_df.loc[
            #         word2vec_sim_df['song_id'] == row['msd_id_true'], 'word2vec_sim'] = get_similarity_between_vectors(
            #         row['representation_vector'],
            #         song_word2vec_representation.values[0])
            # word2vec_sim_df['word2vec_sim'] = word2vec_sim_df['word2vec_sim'].add(
            # )
    word2vec_sim_lyrics_df['song_id'] = songs_with_lyrics_df['song_id']
    word2vec_sim_lyrics_df.set_index('song_id', inplace=True)
    word2vec_sim_mxm_df['song_id'] = mxm_objects_df['msd_id_true']
    word2vec_sim_mxm_df.set_index('song_id', inplace=True)
    return word2vec_sim_lyrics_df, word2vec_sim_mxm_df

# if __name__ == '__main__':
#     sen1 = get_mean_of_vector_of_sentence("I love you", for_base_model=True)
#     sen2 = get_mean_of_vector_of_sentence("I like yopu very much my friendo", for_base_model=True)
#     print(get_similarity_between_vectors(sen1, sen2))
