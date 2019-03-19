test = True
import time
import pprint
import numpy as np
import pandas as pd
import networkx as nx
import pickle
import matplotlib.pyplot as plt
from multiprocessing import Pool

cast_df = None
with open('data/the-movies-dataset/cast_for_network.pkl', 'rb') as fl:
    cast_df = pickle.load(fl)
def convert_ids(ids_in_csv):
    return pd.to_numeric(ids_in_csv, errors='coerce').astype('int64')

names_for_movies_df = pd.read_csv('data/the-movies-dataset/movies_metadata.csv'
                                  , converters={ 'id': lambda x: convert_ids(x), 'imdb_id': lambda x: convert_ids(x) }
                                  , usecols=['id', 'original_title'
        , 'popularity', 'overview', 'genres'
        , 'revenue', 'vote_average'
        , 'runtime', 'tagline'
        , 'homepage', 'poster_path'
        , 'release_date'
        , 'title', 'spoken_languages'
                                             ])

cast_df = cast_df.drop_duplicates()
names_for_movies_df = names_for_movies_df.drop_duplicates()

actors_and_movie_info_df = cast_df.merge(names_for_movies_df
                                         , how='inner'
                                         , left_on='movie'
                                         , right_on='id')

actors_and_movie_info_df = actors_and_movie_info_df.rename(columns={ 'id_x': 'id_actor', 'id_y': 'id_movie' })
actors_filmography_group = actors_and_movie_info_df.groupby('name')

##### Test Data
test_df = actors_and_movie_info_df[
    (actors_and_movie_info_df.original_title == 'Toy Story') | (actors_and_movie_info_df.original_title == 'Big')]
test_group = test_df.groupby('name')
if test == True:
    actors_filmography_group = test_group
####

master_graph = nx.MultiGraph()

#########Working .... But Slow
# for filmography in actors_filmography_group:
#     # for filmography in test_group:
#     #     print('@@@@@@@@@@@@@@@@@@@@@@@BEGIN@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
#     #     print('This is the Graph creation for %s :' % (actor_edge['name']))
#
#     name = filmography[0]
#     films_df = filmography[1]
#
#     ## Need to store attribuetes of actors in a list, not dictionary based on constraints of NetworkX
#     ## When accessing an edge, index 0 is Name, 1 is Actor_id, 2 is profile_path
#     actor_edge_attrs = [name, films_df['id_actor'].iloc[0], films_df['profile_path'].iloc[0]]
#
#     films = films_df[['id_movie', 'original_title', 'profile_path', 'popularity', 'genres', 'vote_average'
#         , 'overview', 'poster_path', 'release_date', 'revenue'
#         , 'runtime', 'spoken_languages', 'tagline', 'title']].to_dict(orient='records')
#
#     nodes_for_stargraph = [film['title'] for film in films]
#     node_attributes = { film['title']: film for film in films }
#
#     # pprint.pprint(node_attributes)
#
#     actor_stargraph = nx.star_graph(nodes_for_stargraph, nx.MultiGraph)
#
#     nx.set_node_attributes(actor_stargraph, node_attributes)
#     nx.set_edge_attributes(actor_stargraph, actor_edge_attrs, 'actor')
#
#     master_graph = nx.compose(master_graph, actor_stargraph)


def create_actors_stargraph(filmography_grpby):

    name = filmography_grpby[0]
    films_df = filmography_grpby[1]

    actor_edge_attrs = [name, films_df['id_actor'].iloc[0], films_df['profile_path'].iloc[0]]

    films = films_df[['id_movie', 'original_title', 'profile_path', 'popularity', 'genres', 'vote_average'
        , 'overview', 'poster_path', 'release_date', 'revenue'
        , 'runtime', 'spoken_languages', 'tagline', 'title']].to_dict(orient='records')

    nodes_for_stargraph = [film['title'] for film in films]
    node_attributes = { film['title']: film for film in films }

    actor_stargraph = nx.star_graph(nodes_for_stargraph, nx.MultiGraph)
    nx.set_node_attributes(actor_stargraph, node_attributes)
    nx.set_edge_attributes(actor_stargraph, actor_edge_attrs, 'actor')

    return actor_stargraph


#### Attempting to rewrite code with function-call for parellelization
# for filmography in actors_filmography_group:
#     actors_graph = create_actors_stargraph(filmography)
#
#     master_graph = nx.compose(master_graph, actors_graph)
#
# pprint.pprint(master_graph.nodes)
# pprint.pprint(nx.get_edge_attributes(master_graph, 'actor'))

if __name__ == '__main__':
    pool = Pool(processes=24)
    actor_graphs = pool.imap(create_actors_stargraph, actors_filmography_group)
    master_graph = nx.compose_all(actor_graphs)
    try:
        nx.write_gpickle(master_graph, 'movie_graph.pkl')
    except:
        print('Failed to write Pickle')
    try:
        nx.write_gexf(master_graph, 'movie_graph.gexf')
    except:
        print('Failed to write GEXF')


    #pprint.pprint(master_graph.nodes)
    #pprint.pprint(nx.get_edge_attributes(master_graph, 'actor'))