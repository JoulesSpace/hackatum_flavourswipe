import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import random

def get_recipes(conn):
    """
    Get recipes from database

    :param conn: database connection
    :return: recipes as a mapping from recipe id to list of ingredient ids
    """
    recipes = pd.read_sql_query("SELECT * FROM api_recipe", conn)
    recipe_to_ingridient = pd.read_sql_query("SELECT * FROM api_recipe_ingredients", conn)
    recipes = recipes.merge(recipe_to_ingridient, left_on='id', right_on='recipe_id')
    # recipes = pd.DataFrame(recipes.groupby('recipe_id')['ingredient_id'].apply(list))
    # group by recipe_id and name
    recipes = pd.DataFrame(recipes.groupby(['recipe_id', 'name'])['ingredient_id'].apply(list))
    recipes = recipes.reset_index().to_dict('records')


    ingredients = pd.read_sql_query("SELECT * FROM api_ingredient", conn)
    for recipe in recipes:
        recipe['ingredient_str'] = [ingredients[ingredients['id'] == ingredient_id]['name'].values[0] for ingredient_id in recipe['ingredient_id']]
        recipe['ingredient_str'] = ' '.join(recipe['ingredient_str'])
        # random feedback -1, 0, 1
        recipe['feedback'] = random.randint(-1, 1)
        
    # E.g.:
    # [{'recipe_id': 1, 'ingredient_id': [1, 2, 3], 'ingredient_str': 'flour sugar salt'},
    #  {'recipe_id': 2, 'ingredient_id': [2, 3, 4], 'ingredient_str': 'sugar salt butter'}]

      
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

 

def get_recommendation(recipe_id, recipes, similarities, random_top_n=0):
    """
    Get recommendations for a recipe

    :param recipe_id: id of recipe to get recommendations for
    :param recipes: recipes as a mapping from recipe id to list of ingredient ids
    :param similarities: similarity matrix
    :param random_top_n: number of top recommendations to randomly select from
    :return: list of recommended recipes
    """
    # Get the index of the recipe that matches the id
    idx = [recipe['recipe_id'] for recipe in recipes].index(recipe_id)

    # Get the pairwsie similarity scores of all recipes with that recipe
    sim_scores = list(enumerate(similarities[idx]))

    print(sim_scores)

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



def main():
    conn = sqlite3.connect("db.sqlite3")
    recipes = get_recipes(conn)
    similarities = get_similarities(recipes, feedback_weight=0.3)
    idx = [recipe['recipe_id'] for recipe in recipes].index(1)

    selected_recipe = recipes[idx]
    recommendations = get_recommendation(1, recipes, similarities)
    feedback = [recipe['feedback'] for recipe in recipes]
    recipe_names = [recipe['name'] for recipe in recipes]

    # print what the initial recipe was, what feedback the user had and what the recommendations are
    print("Recipe:", selected_recipe)
    print("Names:", recipe_names)
    print("Feedback:", feedback)
    print("Recommendations:", [recipe['name'] for recipe in recommendations])