# MovieRecommender_AI

The move recommender uses three seperate models to suggest a movie for a user to view based on the [Kaggle](https://www.kaggle.com/rounakbanik/the-movies-dataset#movies_metadata.csv) dataset.  

Three different methods are used:

* Content Filter

* Collaborative Filter

* Graph Filter

The basic code for these models is in the *Modeling* folder.

* Modeling/collaborative_filtering.py
* Modeling/content_filtering.py
* Modeling/graphing.py

To run the model, use a Jupyter Notebook:

* notebooks/Hybridization4.ipynb

To run the application, you must download the dataset from Kaggle, and place it in the *data/* folder. Additionally, 
you must insert the movie data into a neo4j database. The neo4j cypher code to 
perform the insertion is located in:

* data/movie_bootstrap.cyp 

   