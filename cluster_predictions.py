from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics

from sklearn.cluster import KMeans, MiniBatchKMeans

import logging
from optparse import OptionParser
import sys
from time import time

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
import pickle


class nlp_preprocessor:

    def __init__(self, vectorizer=CountVectorizer(), tokenizer=None, cleaning_function=None,
                 stemmer=None, model=None):
        """
        A class for pipelining our data in NLP problems. The user provides a series of
        tools, and this class manages all of the training, transforming, and modification
        of the text data.
        ---
        Inputs:
        vectorizer: the model to use for vectorization of text data
        tokenizer: The tokenizer to use, if none defaults to split on spaces
        cleaning_function: how to clean the data, if None, defaults to the in built class
        """
        if not tokenizer:
            tokenizer = self.splitter
        if not cleaning_function:
            cleaning_function = self.clean_text
        self.stemmer = stemmer
        self.tokenizer = tokenizer
        self.model = model
        self.cleaning_function = cleaning_function
        self.vectorizer = vectorizer
        self._is_fit = False

    def splitter(self, text):
        """
        Default tokenizer that splits on spaces naively
        """
        return text.split(' ')

    def clean_text(self, text, tokenizer, stemmer):
        """
        A naive function to lowercase all works can clean them quickly.
        This is the default behavior if no other cleaning function is specified
        """
        cleaned_text = []
        for post in text:
            cleaned_words = []
            for word in tokenizer(post):
                low_word = word.lower()
                if stemmer:
                    low_word = stemmer.stem(low_word)
                cleaned_words.append(low_word)
            cleaned_text.append(' '.join(cleaned_words))
        return cleaned_text

    def fit(self, text):
        """
        Cleans the data and then fits the vectorizer with
        the user provided text
        """
        clean_text = self.cleaning_function(text, self.tokenizer, self.stemmer)
        self.vectorizer.fit(clean_text)
        self._is_fit = True

    def transform(self, text):
        """
        Cleans any provided data and then transforms the data into
        a vectorized format based on the fit function. Returns the
        vectorized form of the data.
        """
        if not self._is_fit:
            raise ValueError("Must fit the models before transforming!")
        clean_text = self.cleaning_function(text, self.tokenizer, self.stemmer)
        return self.vectorizer.transform(clean_text)

    def save_pipe(self, filename):
        """
        Writes the attributes of the pipeline to a file
        allowing a pipeline to be loaded later with the
        pre-trained pieces in place.
        """
        if type(filename) != str:
            raise TypeError("filename must be a string")
        pickle.dump(self.__dict__, open(filename + ".mdl", 'wb'))

    def load_pipe(self, filename):
        """
        Writes the attributes of the pipeline to a file
        allowing a pipeline to be loaded later with the
        pre-trained pieces in place.
        """
        if type(filename) != str:
            raise TypeError("filename must be a string")
        if filename[-4:] != '.mdl':
            filename += '.mdl'
        self.__dict__ = pickle.load(open(filename, 'rb'))


import pandas as pd


def convert_ids(ids_in_csv):
    return pd.to_numeric(ids_in_csv, errors='coerce').astype('int64')


movies_metadata_df = pd.read_csv('data/the-movies-dataset/movies_metadata.csv'
                                 , converters={ 'id': lambda x: convert_ids(x), 'imdb_id': lambda x: convert_ids(x) }
                                 , usecols=['id', 'original_title'
        , 'genres', 'homepage'
        , 'overview', 'popularity', 'poster_path'
        , 'release_date', 'revenue', 'runtime'
        , 'spoken_languages', 'tagline', 'title'
        , 'vote_average', 'vote_count'])

import re


def clean(text, tokenizer, stemmer):
    """
    Cleans Text with Regexes
    :param text:
    :return: text:
    """
    doc = ''.join(text).lower()
    doc = re.sub(r'[<>\{}/;|\[\]-]', ' ', doc)
    doc = re.sub(r'[0-9]', ' ', doc)
    doc = re.sub(r'\'', ' ', doc)
    doc = re.sub(r'=', ' ', doc)
    doc = re.sub(r':', ' ', doc)
    doc = re.sub(r'"', ' ', doc)
    doc = re.sub(r'\s+', ' ', doc)
    doc = re.sub(r'\(', ' ', doc)
    doc = re.sub(r'\)', ' ', doc)
    doc = re.sub(r'\s{2,}', ' ', doc)
    doc = re.sub(r'\.', '', doc)
    doc = re.sub(r',', '', doc)

    return doc


from sklearn.feature_extraction.text import TfidfVectorizer

nlp_pp = nlp_preprocessor(TfidfVectorizer(stop_words='english'), cleaning_function=clean)

corpus = ' '
sentences = [str(sentence) for sentence in movies_metadata_df.overview.tolist()]

cv_tfidf = TfidfVectorizer(min_df=5, stop_words='english')  # ngram_range=(1,2)

X_tfidf = cv_tfidf.fit_transform(sentences).toarray()

# tfidf_model_df = pd.DataFrame(X_tfidf, columns=cv_tfidf.get_feature_names())

from sklearn.decomposition import TruncatedSVD

svd = TruncatedSVD(n_components=20)

tfidf_model_df = pd.DataFrame(X_tfidf, columns=cv_tfidf.get_feature_names())

X = svd.fit_transform(tfidf_model_df)

# print(svd.explained_variance_ratio_.sum())

km = KMeans(n_clusters=60, init='k-means++', max_iter=100, n_init=1, verbose=True)
km.fit(X)

clustered = zip(km.labels_, movies_metadata_df['id'])  # zip(tfidf_model_df.index.values, km.labels_)

#### Needs Functionalization/Abstraction
from collections import defaultdict

movie_summaries_clustered = defaultdict(list)

for cluster, movie_id in clustered:
    movie_summaries_clustered[cluster].append(movie_id)


####

# cluster_distribution = [len(movies) for (clust, movies) in movie_summaries_clustered.items()]

def get_cluster_number(movie, cluster_zip):
    for cluster, movie_id in cluster_zip:

        if movie_id == movie:
            return cluster

    raise Exception('Movie not found in cluster')


#### Find the cluster of a movie by movie id
clustered = zip(km.labels_, movies_metadata_df['id'])  # zip(tfidf_model_df.index.values, km.labels_)
print(get_cluster_number(862, clustered))


####

def get_movie_name(movie_id):
    return movies_metadata_df[movies_metadata_df.id == movie_id]['original_title'].iloc[0]


def get_all_movies_in_cluster(cluster_number, cluster_dict):
    movies = cluster_dict[cluster_number]
    return [get_movie_name(mov) for mov in movies]


#### List all the movies in a cluster
print(get_all_movies_in_cluster(20, movie_summaries_clustered))
####