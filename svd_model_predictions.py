import pandas as pd
import numpy as np
from surprise import SVD
from surprise.model_selection import cross_validate, train_test_split
from surprise import Dataset
from surprise import Reader
from surprise.prediction_algorithms.knns import KNNWithZScore, KNNBaseline
from surprise.prediction_algorithms.matrix_factorization import NMF
from pandas.io.json import json_normalize
from pymongo import MongoClient

def convert_ids(ids_in_csv):
    return pd.to_numeric(ids_in_csv, errors='coerce').astype('int64')

from collections import defaultdict
def get_top_n(predictions, n=10):
    '''COPIED FROM SUPRISE API
    Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

def get_movie_name(movie_id):
    return ratings_with_movie_names[ratings_with_movie_names.id == movie_id]['original_title'].iloc[0]


def print_user_prediction(userId, predictions_dict):
    users_viewed_movies = ratings_with_movie_names[ratings_with_movie_names['userId'] == userId][
        ['rating', 'original_title']]
    print(f'User {userId} has viewed the following movies:\n')

    for row in users_viewed_movies.itertuples():
        rating = row[1]
        original_title = row[2]
        print(f'\t{original_title}, Rating: {rating}')

    print(f'\nThe following movies are recommended for User {userId}\n')
    recommended_movies = [get_movie_name(mov_id[0]) for mov_id in predictions_dict[userId]]

    for movie in recommended_movies:
        print(f'\t{movie}')


ratings_df = pd.read_csv('data/the-movies-dataset/ratings_small.csv')
movies_df = pd.read_csv('data/the-movies-dataset/movies_metadata.csv'
                        , converters={'id': lambda x: convert_ids(x), 'imdb_id': lambda x: convert_ids(x)}
                       ,usecols=['id', 'original_title', 'belongs_to_collection'
                                 , 'budget', 'genres', 'homepage'
                                 ,'imdb_id', 'overview', 'popularity', 'poster_path'
                                 , 'production_companies','release_date', 'revenue', 'runtime',
                                 'spoken_languages', 'status', 'tagline', 'title', 'video',
                                 'vote_average', 'vote_count'])

###May need Fuzzy matching, but for now:
movies_df = movies_df[movies_df.spoken_languages == """[{'iso_639_1': 'en', 'name': 'English'}]"""]


ratings_with_movie_names = ratings_df.merge(movies_df[['id', 'original_title']], how='left', left_on='movieId', right_on='id')
ratings_with_movie_names = ratings_with_movie_names[ratings_with_movie_names.original_title.isnull() == False]

algo = SVD(verbose=True)
reader = Reader(rating_scale=(0, 5))
data = Dataset.load_from_df(ratings_with_movie_names[['userId', 'movieId', 'rating']], reader)
trainset = data.build_full_trainset()

algo.fit(trainset)

cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, n_jobs=-1, verbose=True)

testset = trainset.build_anti_testset()

predictions = algo.test(testset)

top_n = get_top_n(predictions)

predicted_movies_by_name = defaultdict(list)

for key, value in top_n.items():
    predicted_movies_by_name[key] = [get_movie_name(mov_id[0]) for mov_id in value]

print_user_prediction(321, top_n)