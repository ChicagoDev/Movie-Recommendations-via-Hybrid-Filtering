#Python Imports
from utils.movieDatasetTools import *
from collections import defaultdict, namedtuple

from utils.movieDatasetTools import get_movie_name

UserFavoriteRating = namedtuple('UserFavoriteRating', ['title', 'rating'])


def get_top_n(predictions, n=200):
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


def print_user_prediction(userId, predictions_dict, meta_df, movies_df):
    users_viewed_movies = movies_df[movies_df['userId'] == userId][
        ['rating', 'original_title']]
    print(f'User {userId} has viewed the following movies:\n')

    for row in users_viewed_movies.itertuples():
        rating = row[1]
        original_title = row[2]
        print(f'\t{original_title}, Rating: {rating}')

    print(f'\nThe following movies are recommended for User {userId}\n')
    recommended_movies = [get_movie_name(mov_id[0], meta_df) for mov_id in predictions_dict[userId]]

    for movie in recommended_movies:
        print(f'\t{movie}')


def users_favorite_movies(n, userId, predictions_dict, meta_df, movies_df):
    users_viewed_movies = movies_df[movies_df['userId'] == userId][
        ['rating', 'original_title']]

    viewed_movies = []

    for row in users_viewed_movies.itertuples():
        rating = row[1]
        original_title = row[2]
        film = UserFavoriteRating(original_title, rating)
        viewed_movies.append(film)

    sorted(viewed_movies, key=lambda film: film[1])

    return viewed_movies[0:n]


def collab_filter_recommendations(user, top_ns, movie_meta_df):
    predictions = top_ns[user]

    return [UserFavoriteRating(get_movie_name(pred[0], movie_meta_df), pred[1]) for pred in predictions]