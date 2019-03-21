from collections import namedtuple
from neo4j import GraphDatabase

GraphMember = namedtuple('GraphMember', ['title', 'movie_id'])

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=('neo4j', ''))


def get_count_first_degree_films_of(tx, title):
    for record in tx.run("MATCH (origin:MOVIE)-[:APPEARED_IN]-(actor)-[:APPEARED_IN]-(first_movie:MOVIE)"
                         "WHERE origin.title = {title} "
                         "RETURN count(*)", title=title):
        print(record[0])


def get_first_degree_films_of(tx, title):
    nodes = []

    for record in tx.run("MATCH (origin:MOVIE)-[:APPEARED_IN]-(actor)-[:APPEARED_IN]-(first_movie:MOVIE)"
                         "WHERE origin.title = {title} "
                         "RETURN first_movie", title=title):
        nodes.append(record.data())

    return nodes



def neo4j_results_to_tuples(results):
    return [GraphMember(node['first_movie'].get('title'), node['first_movie'].get('movie_id')) for node in results]


def get_connected_movies(list_favorite_movies, driver):
    list_connected_movies = []

    with driver.session() as session:
        for movie in list_favorite_movies:
            first_degree_away_films = session.read_transaction(get_first_degree_films_of, movie)
            film_tups = neo4j_results_to_tuples(first_degree_away_films)
            list_connected_movies.extend(film_tups)

    return list_connected_movies