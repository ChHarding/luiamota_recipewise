"""
RecipeWise - A Flask web application that allows users to search for recipes
and save favorite recipes for later viewing.
"""
# Version 1 focuses on project setup and application structure.

# Import Flask framework
from flask import Flask, render_template, request 
# Importing requests library to be able to call TheMealDB API and get recipe data 
import requests

app = Flask(__name__)


# ==================================================
# BLOCK 1: SEARCH RECIPES
# ==================================================
# Functionality:
# - Receive user's search input
# - Send request to TheMealDB API
# - Return matching recipes
# 
#  What's new in this version:
# - The user enters a recipe name in the search bar on the home page, located in index.html.
# - Flask receives the search input and send a request to TheMealDB API.
# - Matching recipes are returned and displayed on the home page.
#   - Recipe name
#   - Recipe image
#   - Recipe country of origin
# ---------------------------------------------------

def search_recipes(recipe_name):
    # Making a request to TheMealDB API to search for recipes
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={recipe_name}"
    response = requests.get(url)
    # Turn the response to JSON format
    data = response.json()
    return data ["meals"]

# ==================================================
# BLOCK 2: RECIPE DETAILS PAGE
# ==================================================
# Functionality:
# - Display selected recipe
# - Show ingredients
# - Show instructions
# - Show recipe image
#
#  What's new in this version:
# ---------------------------------------------------
def get_recipe_details(meal_id):
    # Getting the recipe details from one recipe using the meal_id from TheMealDB API
    url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    response = requests.get(url)
    
    # Turn the response to JSON format
    data = response.json()
    # Returning the recipe details from the API 
    return data["meals"][0]

# ==================================================
# BLOCK 3: SAVE RECIPES
# ==================================================
# Functionality:
# - Save selected recipe
# - Store recipe information
# - Manage favorite recipes
#
#  What's new in this version:
# ---------------------------------------------------
def save_recipe():
    pass

# ==================================================
# BLOCK 4: VIEW SAVED RECIPES
# ==================================================
# Functionality:
# - Retrieve saved recipes
# - Display saved recipes
# - Refresh recipe information if needed
#
#  What's new in this version:
# ---------------------------------------------------

def get_saved_recipes():
    pass

# ==================================================
# FLASK ROUTES
# ==================================================
# Purpose: 
# - Connect the Flask application with the HTML templates
# Pages: 
# - Home page (index.html)
# - Recipe details page (recipe_details.html)
# - Favorite recipes page (favorites.html)
# ---------------------------------------------------

# Create a route for the home page (index.html) where users can search for recipes
@app.route("/", methods=["GET", "POST"])
def home():
    meals = []
    if request.method == "POST":
        recipe_name = request.form["recipe_name"]
        print(f"Searching for recipes matching: {recipe_name}")
        meals = search_recipes(recipe_name)
    return render_template("index.html", meals=meals)

# Create a route for the recipe details page (recipe_details.html) where users can view the details of a selected recipe.
@app.route("/recipe/<int:meal_id>")
def recipe_details(meal_id):
   # return f"You selected recipe with ID: {meal_id}"
    return render_template("recipe_details.html", recipe=get_recipe_details(meal_id))

# Future: Create a route for favorite recipes page (favorites.html) where users can view their saved recipes.
@app.route("/favorites")
def favorites():
    return render_template("favorites.html")

if __name__ == "__main__":
    app.run(debug=True,port=5001)