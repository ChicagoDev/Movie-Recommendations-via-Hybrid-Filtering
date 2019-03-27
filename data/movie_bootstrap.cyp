USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///all_actors_two_clms.csv" AS row
CREATE (:ACTOR {name: row.name, actor_id: toInteger(row.id)})

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///movies_metadata.csv" AS row
CREATE (:MOVIE {title: row.title, movie_id: toInteger(row.id)})

CREATE INDEX ON :MOVIE(movie_id);
CREATE INDEX ON :ACTOR(actor_id);
CREATE INDEX ON :MOVIE(title);
CREATE INDEX ON :ACTOR(name);

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///actors_and_movies.neo4j.csv" AS row
MATCH (movie:MOVIE {movie_id: toInt(row.id_movie)})
MATCH (actor:ACTOR {actor_id: toInt(row.id_actor)})
MERGE (actor)-[:APPEARED_IN]->(movie)


// QUERIES
MATCH (tom:ACTOR {name:"Tom Hanks"})-[:APPEARED_IN]->(:MOVIE)<-[:APPEARED_IN]-(coActor:ACTOR)
RETURN coActor.name


MATCH (x_men:MOVIE {title: "X-Men: First Class"})-[link:APPEARED_IN]-(actors:ACTOR) return x_men, actors

MATCH (tom:ACTOR {name:"Kevin Bacon"})-[:APPEARED_IN]->(movie:MOVIE)
RETURN tom, movie

MATCH (tom:ACTOR {name: 'Tom Hanks'})-[:APPEARED_IN]->(:MOVIE)<-[:APPEARED_IN]-(coActor:ACTOR)
RETURN coActor.name

MATCH (tom:ACTOR)-[:APPEARED_IN]->(movie1)<-[:APPEARED_IN]-(coActor:ACTOR),
         (coActor)-[:APPEARED_IN]->(movie2)<-[:APPEARED_IN]-(coCoActor:ACTOR)
WHERE tom.name = 'Tom Hanks'
AND   NOT    (tom)-[:APPEARED_IN]->()<-[:APPEARED_IN]-(coCoActor)
RETURN coCoActor.name, count(distinct coCoActor) as frequency
ORDER BY frequency DESC
LIMIT 30


MATCH (tom:ACTOR)-[:APPEARED_IN]->(movie1)<-[:APPEARED_IN]-(coActor:ACTOR),
         (coActor)-[:APPEARED_IN]->(movie2)<-[:APPEARED_IN]-(cruise:ACTOR)
WHERE tom.name = 'Tom Hanks' AND cruise.name = 'Tom Cruise'
AND   NOT    (tom)-[:APPEARED_IN]->(movie2)
RETURN tom, movie1, coActor, movie2, cruise
//////
MATCH (origin:MOVIE)-[:APPEARED_IN]-(actor)-[:APPEARED_IN]-(first_movie:MOVIE)
WHERE origin.title = 'Top Gun'

RETURN origin, actor, first_movie
//////
MATCH (origin:MOVIE)-[:APPEARED_IN]-(actor)-[:APPEARED_IN]-(first_movie:MOVIE)-[:APPEARED_IN]-(actor2)-[:APPEARED_IN]-(second_movie:MOVIE)
WHERE origin.title = 'Top Gun'

RETURN origin, actor, first_movie, actor2, second_movie
/////
MATCH (origin:MOVIE)-[:APPEARED_IN]-(actor)-[:APPEARED_IN]-(first_movie:MOVIE)
WHERE origin.title = 'Top Gun'

RETURN origin, actor, first_movie

//
MATCH (origin:MOVIE)-[:APPEARED_IN]-(actor)-[:APPEARED_IN]-(first_movie:MOVIE)-[:APPEARED_IN]-(actor2)-[:APPEARED_IN]-(movie2:MOVIE)-[:APPEARED_IN]-(actor3)-[:APPEARED_IN]-(movie3:MOVIE)
WHERE origin.title = 'Ferris Bueller\'s Day Off' AND actor.name = 'Matthew Broderick' and first_movie.title in ["Election", "You Can Count On Me", "The Cable Guy", "The Freshman" ]

RETURN origin, actor, first_movie, actor2, movie2, actor3, movie3 limit 300
//
MATCH (origin:MOVIE)-[:APPEARED_IN]-(actor)-[:APPEARED_IN]-(first_movie:MOVIE)-[:APPEARED_IN]-(actor2)-[:APPEARED_IN]-(movie2:MOVIE)-[:APPEARED_IN]-(actor3)-[:APPEARED_IN]-(movie3:MOVIE)
WHERE origin.title = 'Ferris Bueller\'s Day Off' AND actor.name = 'Matthew Broderick'

RETURN origin, actor, first_movie, actor2, movie2, actor3, movie3 limit 300
//

MATCH (origin:MOVIE)-[:APPEARED_IN]-(actor)-[:APPEARED_IN]-(first_movie:MOVIE)
WHERE origin.title = 'Ferris Bueller\'s Day Off'

RETURN origin, actor, first_movie