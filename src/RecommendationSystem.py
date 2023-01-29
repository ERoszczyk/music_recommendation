import time
import streamlit as st
from src.word2vec import get_songs_by_word2vec
from src.collaborative_filtering import get_songs_rated_by_more_than_n_users, get_triplets_by_song_ids, \
    get_songs_to_recommend_for_user_considering_user_similarity
from src.content_based_filtering import get_recommended_songs_based_on_cosine_similarity, \
    get_recommended_songs_based_on_sigmoid_kernel
from src.recommend_songs_based_on_sentiment import calculate_sentiment_similarity


class RecommendationSystem:
    def __init__(self, user_id, triplets_df, songs_df, mxm_objects_df, songs_with_lyrics_df, reduce_songs_df=True,
                 reduce_songs_by_ratings_amount=100,
                 reduce_triplets_df=True, reduce_triplets_by_rows=500000, n_recommendations=10):
        self.user_id = user_id
        self.triplets_df = triplets_df
        self.song_df = songs_df
        self.mxm_objects_df = mxm_objects_df
        self.songs_with_lyrics_df = songs_with_lyrics_df
        self.n_recommendations = n_recommendations

        self.collaborative_filtering = True
        self.tfidf_algorithm = True
        self.sentiment_recommendation = True
        self.word2vec = True
        self.show_time = True

        self.reduce_songs_df = reduce_songs_df
        self.reduce_songs_by_ratings_amount = reduce_songs_by_ratings_amount
        self.reduce_triplets_df = reduce_triplets_df
        self.reduce_triplets_by_rows = reduce_triplets_by_rows

    def set_collaborative_filtering(self, if_collaborative_filtering):
        self.collaborative_filtering = if_collaborative_filtering

    def set_tfidf_algorithm(self, if_content_based_filtering):
        self.tfidf_algorithm = if_content_based_filtering

    def set_sentiment_recommendation(self, if_sentiment_recommendation):
        self.sentiment_recommendation = if_sentiment_recommendation

    def set_word2vec(self, if_word2vec):
        self.word2vec = if_word2vec

    def set_show_time(self, if_show_time):
        self.show_time = if_show_time

    def get_songs_user_has_listened_to(self):
        return self.triplets_df.loc[self.triplets_df['user_id'] == self.user_id, 'song_id']

    def add_recommendation_values(self, recommendation_df1, recommendation_df2):
        recommendation_df1.sort_values(by=['song_id'], inplace=True, ascending=False)
        recommendation_df2.sort_values(by=['song_id'], inplace=True, ascending=False)
        recommendation_df1['total_score'] = recommendation_df1['total_score'] + \
                                            recommendation_df2['total_score']
        recommendation_df1['total_score'] /= 2
        return recommendation_df1

    def get_recommendations(self):
        combined_songs = self.song_df[['song_id']].copy()
        if self.collaborative_filtering:
            if self.reduce_songs_df:
                # self.song_df = get_songs_rated_by_more_than_n_users(self.song_df, self.reduce_songs_by_ratings_amount)
                self.triplets_df = get_triplets_by_song_ids(self.triplets_df,
                                                            get_songs_rated_by_more_than_n_users(self.song_df,
                                                                                                 self.reduce_songs_by_ratings_amount))
            if self.reduce_triplets_df:
                self.triplets_df = self.triplets_df[:self.reduce_triplets_by_rows]
            start_time = time.time()
            songs_to_recommend = get_songs_to_recommend_for_user_considering_user_similarity(self.triplets_df,
                                                                                             self.user_id,
                                                                                             self.song_df,
                                                                                             self.n_recommendations)
            # self.print_recommendations(songs_to_recommend)
            end_time = time.time()
            print(f'Collaborative filtering took {"{:.2f}".format(end_time - start_time)} seconds')
            if self.show_time:

                st.write(f'Filtrowanie oparte na współpracy zajęło {"{:.2f}".format(end_time - start_time)} sekund.')
            songs_to_recommend.rename(columns={'total_score': 'collaborative_filtering_score'}, inplace=True)
            combined_songs = combined_songs.merge(songs_to_recommend, on='song_id', how='outer')

        if self.tfidf_algorithm:
            user_songs = self.get_songs_user_has_listened_to()
            start_time = time.time()
            cos_sim = get_recommended_songs_based_on_cosine_similarity(user_songs.to_list(), self.songs_with_lyrics_df,
                                                                       self.n_recommendations)
            end_time = time.time()
            print(f'Cosine similarity took {"{:.2f}".format(end_time - start_time)} seconds')
            if self.show_time:
                st.write(f'Wygenerowanie rekomendacji na bazie podobieństwa cosinusowego zajęło {"{:.2f}".format(end_time - start_time)} sekund.')
            if cos_sim.empty:
                print("No recommendations based on cosine similarity")
            else:
                cos_sim.rename(columns={'total_score': 'cosine_similarity_score'}, inplace=True)
                combined_songs = combined_songs.merge(cos_sim, on='song_id', how='outer')
            start_time = time.time()
            sig_kernel = get_recommended_songs_based_on_sigmoid_kernel(user_songs.to_list(), self.songs_with_lyrics_df,
                                                                       self.n_recommendations)
            end_time = time.time()
            print(f'Sigmoid kernel took {"{:.2f}".format(end_time - start_time)} seconds')
            if self.show_time:
                st.write(f'Wygenerowanie rekomendacji na bazie jądra sigmoidalnego zajęło {"{:.2f}".format(end_time - start_time)} sekund.')
            if sig_kernel.empty:
                print("No recommendations based on sigmoid kernel")
            else:
                sig_kernel.rename(columns={'total_score': 'sigmoid_kernel_score'}, inplace=True)
                combined_songs = combined_songs.merge(sig_kernel, on='song_id', how='outer')

        if self.sentiment_recommendation:
            user_songs = self.get_songs_user_has_listened_to()
            start_time = time.time()
            recommendation_df = calculate_sentiment_similarity(self.mxm_objects_df, user_songs.to_list())
            end_time = time.time()
            print(f'Sentiment similarity took {"{:.2f}".format(end_time - start_time)} seconds')
            if self.show_time:
                st.write(f'Wygenerowanie rekomendacji na bazie wydźwięku emocjonalnego zajęło {"{:.2f}".format(end_time - start_time)} sekund.')
            combined_songs = combined_songs.merge(recommendation_df, on='song_id', how='outer')

        if self.word2vec:
            user_songs = self.get_songs_user_has_listened_to()
            start_time = time.time()
            recommendation_df1, recommendation_df2 = get_songs_by_word2vec(self.song_df[['song_id']].copy(),
                                                                           self.mxm_objects_df,
                                                                           self.songs_with_lyrics_df,
                                                                           user_songs.to_list())
            end_time = time.time()
            print(f'Word2vec took {"{:.2f}".format(end_time - start_time)} seconds')
            if self.show_time:
                st.write(f'Wygenerowanie rekomendacji na bazie word2vec zajęło {"{:.2f}".format(end_time - start_time)} sekund.')
            combined_songs = combined_songs.merge(recommendation_df1, on='song_id', how='outer')
            combined_songs = combined_songs.merge(recommendation_df2, on='song_id', how='outer')
        return combined_songs

    def print_recommendations(self, songs_to_recommend):
        print(f'Songs recommended for user {self.user_id} are:')
        index = 1
        for i, song_info in songs_to_recommend.iterrows():
            print(f"{index}. {song_info['title']} by {song_info['artist_name']}")
            index += 1
