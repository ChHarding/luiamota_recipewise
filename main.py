"""
RecipeWise - A Flask web application that allows users to search for recipes
and save favorite recipes for later viewing.
"""

# Importing Flask framework and render_template to render HTML templates (index.html, recipe_details.html, favorites.html)
from flask import Flask, render_template, request 
# Importing requests library to be able to call TheMealDB API and get recipe data 
import requests

# Creating a Flask application instance
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
    # Making a request to TheMealDB API to search for recipes based on the recipe_name provided by the user.
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={recipe_name}"
    # Sending a GET request to the API.
    response = requests.get(url)
    # Turning the response to JSON format.
    data = response.json()
    # Returning the list of matching recipes (meals) from the API response.
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
# - When a user clicks on a recipe from the search results, they are redirected to the recipe details page.
# - RecipeWise retrieves detailed recipe information from TheMealDB API using the selected meal_id.
# - The recipe details are displayed on the recipe_details.html page.
#   Information displayed includes:
#      - Recipe's name
#      - Recipe's ID
#      - Recipe's image
#      - Recipe's ingredients and measurements
#      - Recipe's instructions
#      - Button to add the recipe to favorites (functionality not yet implemented)
# ---------------------------------------------------
def get_recipe_details(meal_id):
    # Getting the recipe details from one recipe using the meal_id from TheMealDB API
    url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    # Sending a GET request to the API to retrieve the recipe details.
    response = requests.get(url)
    # Turning the response to JSON format
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

# ---------------------------------------------------
# HOME PAGE ROUTE (index.html)
# ---------------------------------------------------

# Create a route for the home page where users can search for recipes
@app.route("/", methods=["GET", "POST"])
def home():
    meals = []
    if request.method == "POST":
        recipe_name = request.form["recipe_name"]
        print(f"Searching for recipes matching: {recipe_name}")
        meals = search_recipes(recipe_name)
    return render_template("index.html", meals=meals)

# ---------------------------------------------------
# RECIPE DETAILS ROUTE (recipe_details.html)
# ---------------------------------------------------
# Create a route for the recipe details page where users can view the details of a selected recipe.
@app.route("/recipe/<int:meal_id>")
def recipe_details(meal_id):
    # Get the recipe details using the meal_id from TheMealDB API
    recipe = get_recipe_details(meal_id)
    
    # Split the instructions into a list of steps for better display in the template
    # ---------------------------------------------------------------------------------
    # Note: Each recipe has different formatting for each step in the instructions. 
    # So will need to handle that in the future. For now, we will just split by new lines.
    # ---------------------------------------------------------------------------------
    instructions = recipe["strInstructions"].split("\n")
    instructions = []
    for step in recipe["strInstructions"].split("\n"):
        if step.strip():  # Only add non-empty steps
            instructions.append(step)
            
    # Extract ingredients and their measurements from the recipe details
    ingredients = []
    #Loop through the possible ingredient and measurement fields
    # TheMealDB API has up to 20 ingredients (that's why we loop from 1 to 21. Needed help with this part from AI)
    for i in range(1, 21):
        ingredient = recipe.get(f"strIngredient{i}")
        measure = recipe.get(f"strMeasure{i}")
        # Only add the ingredient if it is not empty
        if ingredient and ingredient.strip():
            ingredients.append(f"{measure} {ingredient}")
    
    return render_template(
        "recipe_details.html", 
        recipe=recipe, 
        instructions=instructions,
        ingredients=ingredients
        )

# ---------------------------------------------------
# FAVORITES ROUTE (favorites.html)
# ---------------------------------------------------
# Create a route for favorite recipes page where users can view their saved recipes.
@app.route("/favorites/add/<int:meal_id>", methods=["POST"])
def add_favorites(meal_id):
    return f"Recipe with ID {meal_id} added to favorites!"
    #return render_template("favorites.html")

if __name__ == "__main__":
    app.run(debug=True,port=5001)