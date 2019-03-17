import pandas as pd
from scipy.linalg import svd as scipy_svd
import numpy as np
import math
from sklearn.metrics.pairwise import cosine_similarity
from heapq import heappush, heappop, nlargest, nsmallest

ratings_df = pd.read_csv('data/the-movies-dataset/ratings_small.csv')
movies = pd.read_csv('data/the-movies-dataset/movies_metadata.csv')


movies_df = movies[['original_title', 'id']]

movies_df = movies_df.assign(movieId=pd.to_numeric(movies_df.id, errors='coerce').fillna(-1).astype('int64'))


movies_df = ratings_df.merge(movies_df, on='movieId')

#Commented movies pivoted, because could not get column names as movie names
#movies_pivoted = movies_df.pivot(index='userId', columns='movieId', values='rating')
ratings_pivoted = ratings_df.pivot(index='userId', columns='movieId', values='rating')

#movie_df_pivoted = movies_pivoted.fillna(0)
ratings_df_pivoted = ratings_pivoted.fillna(0)


#U, Sigma, VT = scipy_svd(movie_df_pivoted)
U, Sigma, VT = scipy_svd(ratings_df_pivoted)

user1 = U[0]

user_v = user1.reshape(1,-1)
heap = []
for i, row in enumerate(U):
    v_row = row.reshape(1,-1)
    heappush(heap, (cosine_similarity(user_v, v_row)[0][0], i))

print(nsmallest(10, heap))

############################################################################

user_id = 236
user_seen_movies_df = ratings_df.groupby('userId').get_group(user_id)[['movieId']][0:10]
user_seen_movies = user_seen_movies_df['movieId']

[(movies_df[movies_df.movieId == movie]['original_title'].iloc[0]) for movie in user_seen_movies]