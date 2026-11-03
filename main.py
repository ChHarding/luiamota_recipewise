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
# - Added clicklable recipe cards to edirect users to the Recipes Detail Page. 
# - Added a Favorites button to allow users to save recipes directly from the search results page. 
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
#      - Button to add the recipe to favorites
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
# BLOCK 3: FAVORITES
# ==================================================
# Functionality:
# - Save selected recipes.
# - Store recipe information in Supabase.
# - Prevent duplicate saves.
# - Manage favorite recipes.
#
#  What's new in this version:
# - Connected the Save Recipe button to the Favorites workflow.
# - Displayed saved recipes on the Favorites page. Each recipe mantains the same style
#   as the search result list (recipe name, image and country of origin).
# - Connected Supabase to store recipe information in a database table. 
# - Added clickable recipe cards that redirect users to the Recipe Details page
# - Added success and duplicate-save feedback messages
# ---------------------------------------------------
#  3.1 SUPABASE INTEGRATION
# ---------------------------------------------------
# - Recipe data is stored in Supabase favorites table. 
# - Before saving a recipe, the system checks wether the recipe already exists.
# ---------------------------------------------------
# Importing Supabase client
from supabase_client import supabase
def save_recipe(meal_id):

    # Retrieve recipe details from TheMealDB API.
    recipe = get_recipe_details(meal_id)
    
    # Check the Supabase favorites table to determine whether the recipe has already been saved. 
    existing_recipe = (
        supabase.table("favorites")
        .select("*")
        .eq("idMeal", recipe["idMeal"])
        .execute()
    )

    # If matching meal ID is found in the database, a duplicated 
    # favorite entry will not be created. 
    # The system will display warning message. 
    if existing_recipe.data:
        return ( 
                "Recipe is already in your favorites.",
                "warning")
    
    # If the recipe has not been saved before,
    # its information is stored in the Supabase favorites table.
    supabase.table("favorites").insert ({
        "idMeal": recipe["idMeal"],
        "strMeal": recipe["strMeal"],
        "strMealThumb": recipe["strMealThumb"],
        "strArea": recipe ["strArea"]
    }) .execute()
    
    # A successful message will be displayed after the recipe is saved.
    return (
        "Recipe saved successfully.",
        "success"
    )



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
#
#
# ---------------------------------------------------
# 1 HOME PAGE ROUTE (index.html)
# ---------------------------------------------------
# Create a route for the home page where users can search for recipes
@app.route("/", methods=["GET", "POST"])
def home():
    # Initialize default values before the search: 
    meals = [] # Stores matching results from the API
    recipe_count = 0 # Recipe's counter
    recipe_name = "" # Stores user's search query. 
    
    if request.method == "POST":
        # Get the recipe name from the search form submitted by the user
        recipe_name = request.form["recipe_name"] 
        # Call the search_recipes function to get matching recipes from TheMealDB API
        meals = search_recipes(recipe_name) 
        # Count the number of matching recipes found to display on the home page.
        recipe_count = len(meals) 
    
    # Retrieve the list of favorite recipes from Supabase to display on the home page.
    favorites_recipes = (
        supabase.table ("favorites")
        .select("idMeal")
        .execute ()
    )
    # Create a set of favorite recipe IDs to idenrify
    # which recipes have already been saved as favorites. 
    favorites_ids = {
        recipe ["idMeal"]
        for recipe in favorites_recipes.data
    }
    # Pass the data to the index.html template to be rendered on the home page.
    return render_template(
        "index.html", 
        meals=meals,
        recipe_count=recipe_count,
        recipe_name=recipe_name,
        favorites_ids=favorites_ids
    )

# ---------------------------------------------------
# 2 RECIPE DETAILS ROUTE (recipe_details.html)
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
    # Loop through the possible ingredient and measurement fields
    # TheMealDB API has up to 20 ingredients (that's why we loop from 1 to 21. 
    # Needed help with this part from AI)
    for i in range(1, 21):
        ingredient = recipe.get(f"strIngredient{i}")
        measure = recipe.get(f"strMeasure{i}")
        # Only add the ingredient if it is not empty
        if ingredient and ingredient.strip():
            ingredients.append(f"{measure} {ingredient}")
    # Retrieve the list of favorite recipes from Supabase to display on the recipe details page.
    favorite_recipes = (
        supabase.table("favorites")
        .select ("idMeal")
        .execute()
    )
    # Create a set of favorite recipe IDs to identify 
    # which recipes have already been saved as favorites.
    favorite_ids = {
        str(recipe["idMeal"])
        for recipe in favorite_recipes.data
    }
    # Pass the data to the recipe_details.html template to be rendered on the recipe details page.
    return render_template(
        "recipe_details.html", 
        recipe=recipe, 
        instructions=instructions,
        ingredients=ingredients,
        favorite_ids=favorite_ids
        )

# ---------------------------------------------------
# 3 FAVORITES ROUTE (favorites.html)
# Create a route for favorite recipes page where users can view their saved recipes.
# ---------------------------------------------------
#
# ////////////////////////////////////////////////////
# 3.1 ROUTE: to the Favorites Page from the Navigation Top Nav Bar. 
@app.route("/favorites")
def favorites_page():
    response = (
            supabase.table("favorites")
            .select("*")
            .execute()
        )
    # Retrieve the list of favorite recipes from Supabase to display on the favorites page.
    favorites = response.data
    # Count the number of favorite recipes to display on the favorites page.
    favorites_count = len(favorites)
    
    # Pass the data to the favorites.html template to be rendered on the favorites page.
    return render_template(
        "favorites.html", 
        favorites=favorites,
        favorites_count=favorites_count
        )

# //////////////////////////////////////////////////
# 3.2 ROUTE: Adding a new recipe to the Supabase Favorites Table.
@app.route("/favorites/add/<int:meal_id>", methods=["POST"])
def add_favorites(meal_id):
    # Message and message_type are returned from the save_recipe function to provide feedback to the user.
    # In this case a success message will be displayed if the recipe is saved successfully,
    # or a warning message will be displayed if the recipe is already in the favorites.
    message, message_type = save_recipe(meal_id)
    response = (
        supabase.table("favorites")
        .select("*")
        .execute()
    )
    # Retrieve the list of favorite recipes from Supabase to display on the favorites page.
    favorites = response.data
    # Count the number of favorite recipes to display on the favorites page.
    favorites_count = len(favorites)
    
    # Pass the data to the favorites.html template to be rendered on the favorites page.
    return render_template(
        "favorites.html", 
        favorites=favorites, 
        message=message,
        favorites_count=favorites_count,
        message_type=message_type
        )
    
# /////////////////////////////////////////////////////// 
# 3.3 ROUTE: Removing a recipe from the Supabase Favorites Table.
@app.route("/favorites/remove/<int:meal_id>", methods=["POST"])
def remove_favorites(meal_id):
    # Message and message_type are returned to provide feedback to the user.
    # In this case a success message will be displayed if the recipe is removed successfully.
    message = "Recipe removed successfully."
    message_type = "success"
    # Removing the recipe from Supabase fav table
    response = (
        supabase.table("favorites")
        .delete()
        .eq("idMeal", str(meal_id))
        .execute()
        )
    response = (
            supabase.table("favorites")
            .select("*")
            .execute()
        )
    # Retrieve the list of favorite recipes from Supabase to display on the favorites page.
    favorites = response.data
    # Count the number of favorite recipes to display on the favorites page.
    favorites_count = len(favorites)
   
    # Pass the data to the favorites.html template to be rendered on the favorites page.
    return render_template (
        "favorites.html",
        favorites=favorites, 
        message=message,
        message_type=message_type,
        favorites_count=favorites_count
    )

if __name__ == "__main__":
    app.run(debug=True,port=5001)