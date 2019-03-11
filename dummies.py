import pandas as pd
import json
import re
import pprint as pp
from pymongo import MongoClient
import seaborn as sns
from pandas.io.json import json_normalize
from sklearn.preprocessing import MultiLabelBinarizer
from sqlalchemy import create_engine


client = MongoClient('localhost', 27017)
db = client.MovieRecommender
mbl = MultiLabelBinarizer()

keywords = db['keywords']
keywords_df = pd.DataFrame(list((keywords).find({})))
del keywords

metadata = db['movies_metadata']
metadata_df = pd.DataFrame(list((metadata).find({})))
del metadata

"""Create Dummy column and variables for Keywords and Genres"""

keywords_df['keyword_names_list'] = keywords_df['keywords'].apply(lambda z: [x['name'] for x in z])
mbl.fit(keywords_df['keyword_names_list'])
keyword_dummies = pd.DataFrame(mbl.transform(keywords_df['keyword_names_list']), columns=mbl.classes_)
keywords_df_long = keywords_df.merge(keyword_dummies, left_index=True, right_index=True)
del keyword_dummies

metadata_df['genres_list'] = metadata_df['genres'].apply(lambda z: [x['name'] for x in z])
mbl.fit(metadata_df['genres_list'])
genres_binary_df = pd.DataFrame(mbl.transform(metadata_df['genres_list']), columns=mbl.classes_)
metadata_df_long = metadata_df.merge(genres_binary_df, left_index=True, right_index=True)
del genres_binary_df