import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import random
from threading import local
import json

def get_recipes(conn):
    """
    Get recipes from database

    :param conn: database connection
    :return: recipes as a mapping from recipe id to list of ingredient ids
    """
    recipes = pd.read_sql_query("SELECT * FROM api_recipe", conn)
    recipe_to_ingridient = pd.read_sql_query("SELECT * FROM api_recipe_ingredients", conn)
    recipes = recipes.merge(recipe_to_ingridient, left_on='id', right_on='recipe_id')
    recipes = pd.DataFrame(recipes.groupby(['recipe_id', 'name'])['ingredient_id'].apply(list))
    recipes = recipes.reset_index().to_dict('records')


    ingredients = pd.read_sql_query("SELECT * FROM api_ingredient", conn)
    for recipe in recipes:
        recipe['ingredient_str'] = [ingredients[ingredients['id'] == ingredient_id]['name'].values[0] for ingredient_id in recipe['ingredient_id']]
        recipe['ingredient_str'] = ' '.join(recipe['ingredient_str'])
        recipe['feedback'] = random.randint(-1, 1) # TODO: get feedback from database
        
    # E.g.:
    # [{'recipe_id': 1, 'ingredient_id': [1, 2, 3], 'ingredient_str': 'ingredient1 ingredient2 ingredient3'}, ...]

      
    return recipes


def get_similarities(recipes, feedback_weight = 0.1):
    """
    Get cosine similarity matrix for recipes

    :param recipes: recipes as a mapping from recipe id to list of ingredient ids
    :param feedback_weight: weight factor for feedback
    :return: similarity matrix
    """

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([recipe['ingredient_str'] for recipe in recipes])

    # Iterate over recipes and adjust TF-IDF matrix
    # This results in a higher similarity score for recipes with positive feedback
    for i, recipe in enumerate(recipes):
        feedback = recipe['feedback']
        if feedback != 0:
            for term, term_index in vectorizer.vocabulary_.items():
                term_weight = tfidf_matrix[i, term_index]
                tfidf_matrix[i, term_index] = term_weight * (1 + feedback_weight * feedback)  # Adjust weight factor as needed

    # print(tfidf_matrix)

    return linear_kernel(tfidf_matrix, tfidf_matrix)

 

def get_recommendation(idx, recipes, similarities, random_top_n=0):
    """
    Get recommendations for a recipe

    :param recipe_id: id of recipe to get recommendations for
    :param recipes: recipes as a mapping from recipe id to list of ingredient ids
    :param similarities: similarity matrix
    :param random_top_n: number of top recommendations to randomly select from
    :return: list of recommended recipes
    """

    # Get the pairwsie similarity scores of all recipes with that recipe
    sim_scores = list(enumerate(similarities[idx]))

    # remove the recipe itself from the list
    sim_scores.pop(idx)

    # Sort the recipes based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)


    # Get the recipe indices
    recipe_indices = [i[0] for i in sim_scores]
    selected_recipes = [recipes[i] for i in recipe_indices]
    
    if random_top_n != 0 and len(selected_recipes) > random_top_n:
        selected_recipes = random.sample(selected_recipes[:random_top_n], random_top_n)

    return selected_recipes 


# Create a thread-local storage to hold SQLite connections
thread_local_storage = local()

def get_sqlite_connection():
    """
    Get a SQLite connection for the current thread

    :return: SQLite connection
    """

    # Check if the current thread already has a connection
    if not hasattr(thread_local_storage, "connection") or thread_local_storage.connection is None:
        # If not, create a new connection
        thread_local_storage.connection = sqlite3.connect("db.sqlite3")
    
    return thread_local_storage.connection


def get_next_recommendation(recipe_id):
    conn = get_sqlite_connection()
    recipes = get_recipes(conn)

    # We have translate the database id to the index in the recipes list
    print(recipe_id)
    recipes_idx = [recipe['recipe_id'] for recipe in recipes].index(recipe_id)

    similarities = get_similarities(recipes, feedback_weight=0.3)
    recommendations = get_recommendation(recipes_idx, recipes, similarities)
    

    # load from database based on recipe_id
    recommeded_id = recommendations[0]['recipe_id']
    selected_recipe = pd.read_sql_query("SELECT * FROM api_recipe WHERE id = " + str(recommeded_id), conn).to_dict('records')
    return json.dumps(selected_recipe)
