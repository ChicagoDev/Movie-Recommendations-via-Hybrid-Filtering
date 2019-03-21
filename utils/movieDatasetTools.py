import json
import re

import pandas as pd


def convert_ids(ids_in_csv):
    return pd.to_numeric(ids_in_csv, errors='coerce').astype('int64')


def convert_to_float(ids_in_csv):
    return pd.to_numeric(ids_in_csv, errors='coerce').astype('float64')


def to_json(csv_entry):
    return json.loads(re.sub('\'', '"', csv_entry))


def get_movie_name(movie_id, movie_meta_df):
    return movie_meta_df[movie_meta_df.id == movie_id]['title'].iloc[0]

def get_movie_id(title, movie_meta_df):
    return movie_meta_df[movie_meta_df.title == title]['id'].iloc[0]