from notebooks.collaborative_filtering import get_songs_rated_by_more_than_n_users, get_triplets_by_song_ids, \
    get_songs_to_recommend_for_user_considering_user_similarity
from notebooks.content_based_filtering import print_recommendations_based_on_cosine_similarity, \
    print_recommendations_based_on_sigmoid_kernel


class RecommendationSystem:
    def __init__(self, user_id, triplets_df, songs_df, reduce_songs_df=True, reduce_songs_by_ratings_amount=100,
                 reduce_triplets_df=True, reduce_triplets_by_rows=500000, n_recommendations=10):
        self.user_id = user_id
        self.triplets_df = triplets_df
        self.song_df = songs_df
        self.n_recommendations = n_recommendations

        self.collaborative_filtering = True
        self.content_based_filtering = True
        self.data = None
        self.user_id = None
        self.user_items = None
        self.similarity_matrix = None
        self.item_similarity_recommendations = None

        if self.collaborative_filtering:
            if reduce_songs_df:
                self.song_df = get_songs_rated_by_more_than_n_users(self.song_df, reduce_songs_by_ratings_amount)
                self.triplets_df = get_triplets_by_song_ids(self.triplets_df, self.song_df)
            if reduce_triplets_df:
                self.triplets_df = self.triplets_df[:reduce_triplets_by_rows]
            songs_to_recommend = get_songs_to_recommend_for_user_considering_user_similarity(self.triplets_df,
                                                                                             self.user_id,
                                                                                             self.n_recommendations)
            self.print_recommendations(songs_to_recommend)

        if self.content_based_filtering:
            print_recommendations_based_on_cosine_similarity(['SOBDLRM12A8C13A0AC', 'SODVOFJ12AB0181EE6'], songs_df, 10)
            print_recommendations_based_on_sigmoid_kernel(['SOBDLRM12A8C13A0AC', 'SODVOFJ12AB0181EE6'], songs_df, 10)

    def print_recommendations(self, songs_to_recommend):
        print(f'Songs recommended for user {self.user_id} are:')
        index = 1
        for i, song_info in songs_to_recommend.iterrows():
            print(f"{index}. {song_info['title']} by {song_info['artist_name']}")
            index += 1
