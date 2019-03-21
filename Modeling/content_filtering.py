#Python Imports
from collections import namedtuple

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from Modeling.collaborative_filtering import users_favorite_movies
from utils.movieDatasetTools import *

ContentFilterRecommendation = namedtuple('ContentFilterRecommendation', ['id_origin', 'title'
                                 ,'id_2', 'title_2'
                                ,'similarity'])

def top_n_closest_content_filtered(n, movie_id, content_filter_df):
    similarity_arr = cosine_similarity(np.array(content_filter_df.loc[movie_id]).reshape(1, -1), content_filter_df)[0].tolist()
    tups = [(similarity_arr.index(value), value) for value in similarity_arr]
    tups = sorted(tups, key=lambda x: x[1], reverse=True)
    return tups[0:n]


def top_filtered_to_movie_rec_tuples(content_filtered_rec_list, origin_movie_id, movie_meta_data_df):
    failed = 0
    recs = []
    origin_film_name = get_movie_name(origin_movie_id, movie_meta_data_df)

    for rec in content_filtered_rec_list:
        try:

            film_2_id = rec[0]
            film_2_name = get_movie_name(rec[0], movie_meta_data_df)
            sim_score = rec[1]

            recs.append(ContentFilterRecommendation(origin_movie_id, origin_film_name
                                                    , film_2_id, film_2_name
                                                    , sim_score))
        except:
            failed += 1

            pass
    print(f'lookup failed {failed} times.')
    return recs


def get_top_three_favs(user_id, prediction_dict, movie_meta_df):
    favorite_seen_movie_array = users_favorite_movies(200, user_id, prediction_dict, movie_meta_df)
    sorted_seen_movies = sorted(favorite_seen_movie_array, key=lambda k: k[1], reverse=True)
    return sorted_seen_movies[0:3]