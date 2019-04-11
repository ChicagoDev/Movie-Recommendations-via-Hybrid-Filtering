# Machine Learning and Graph Database Hybrid Movie Recommendation Model 

This is a hybrid model for creating a personalized list of movie recommendations. The hybrid model builds a person's movie taste-profile and generates lists of similar movies to develop the recommendations. These are created using collaborative filtering and content filtering. What makes this recommendation system unique is the use of its third model: a graph filter, implemented in [neo4j](https://neo4j.com/). The graph filter eliminates movies from being recommended if they don't fit a network criterion. 

Data to create this model was sourced from the [Kaggle's The Movies Dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset). This dataset contains information about 45,000 movies and 25,000,000+ movie ratings.

Three different models to construct the hybrid are:

- Content Filter
  - Overview: A Content Filter determines movies that are similar to each other. For example, *There Will Be Blood* is similar to *No Country for Old Men* because they have similar plot themes, release years, and budgets. If someone likes *There Will be Blood*, *No Country for Old Men* is recommended by the Content Filter. In contrast, a movie like *Girls Just Wanna Have Fun* would not be recommended in the same context. 
  - Implementation: [Scikit-Learn Python API](https://scikit-learn.org/stable/)
  - Code: [Modeling/content_filtering.py](https://github.com/ChicagoDev/MovieRecommender_AI/blob/master/Modeling/content_filtering.py)
- Collaborative Filter
  - Overview: A collaborative filter is used to create an estimated personal-rating for a movie based on other people who have seen the movie. I used a collaborative filter based on Singular Value Decomposition. In other words, the personal-rating is determined by creating an average of people who have the most similar taste to you, who have already seen the movie to recommend.  
  - Implementation: [Surprise Python API](http://surpriselib.com/)
  - Code: [Modeling/collaborative_filtering.py](https://github.com/ChicagoDev/MovieRecommender_AI/blob/master/Modeling/collaborative_filtering.py)
- Graph Filter
  - Overview: I utilized a [graph](https://en.wikipedia.org/wiki/Graph_(abstract_data_type)) and created a network of all 45,000 films connected by the 500,000+ actors in the database. Before I create a recommendation, I chose a user's top three rated films. Then, once I have a set of recommendations from the Collaborative Filter and Content Filter (CF_recs1, CF_recs2), I utilize the Graph FIlter: 
    - check to verify that CF_recs1 is connected on the graph to the top-3 films by a degree of two. 
    - check to verify that CF_recs2 is connected on the graph to the top-3 films by a degree of two. 
      - Films that are connected on the graph are recommended
  - Implementation: Python [neo4j]([https://neo4j.com](https://neo4j.com/)) API, and neo4j [Cypher GraphQL](https://neo4j.com/developer/cypher-query-language/)
  - Code: [Modeling/graphing.py](https://github.com/ChicagoDev/MovieRecommender_AI/blob/master/Modeling/graphing.py)

To see a more in-depth explanation of the features of this hybrid move recommender, you can [watch the presentation I delivered](https://livestream.com/metis/events/8591480). Skip to the 11:45 mark.

Model Architecture Diagrams:

<blockquote class="imgur-embed-pub" lang="en" data-id="VpVO3Ju" data-context="false"><a href="//imgur.com/VpVO3Ju"></a></blockquote><script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>

To run the application, you must download the dataset from Kaggle, and place it in the *data/* folder. Additionally, 
you must insert the movie data into a neo4j database. The neo4j cypher code to 
perform the insertion is located in:

- data/movie_bootstrap.cyp 

To run the model, use the Jupyter Notebook:

- notebooks/Hybridization4.ipynb
