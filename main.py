"""
RecipeWise - A Flask web application that allows users to search for recipes
and save favorite recipes for later viewing.
"""
# Version 1 focuses on project setup and application structure.

# Import Flask framework 
from flask import Flask

app = Flask(__name__)


# ==================================================
# BLOCK 1: SEARCH RECIPES
# ==================================================
# Functionality:
# - Receive user's search input
# - Send request to TheMealDB API
# - Return matching recipes
# ---------------------------------------------------

# Importing requests library to be able to call TheMealDB API and get recipe data
import requests
def search_recipes():
    #Asking user for recipe name to search
    recipe_name = input("Enter recipe name to search: ")
    print(f"Searching for recipes matching: {recipe_name}")
    
    # Making a request to TheMealDB API to search for recipes
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={recipe_name}"
    response = requests.get(url)
    # Turn the response to JSON format
    data = response.json()
    
    # This if statement aims to check if the search input exists in the API response. 
    # If it doesn't, it will print a message to the user telling no recipes were found.
    if data['meals'] is None:
        print("No recipes found for your search.")
    # Else, if the search input exists in the API response, it will print the names 
    # of the recipes found.
    else:
        # The for loop will look for the key 'meals' in the data and print only the 
        # value of 'strMeal' for each meal found.
        for meals in data['meals']:
            print(meals['strMeal'])

search_recipes()

# ==================================================
# BLOCK 2: RECIPE DETAILS
# ==================================================
# Functionality:
# - Display selected recipe
# - Show ingredients
# - Show instructions
# - Show recipe image
def display_recipe_details():
    pass

# ==================================================
# BLOCK 3: SAVE RECIPES
# ==================================================
# Functionality:
# - Save selected recipe
# - Store recipe information
# - Manage favorite recipes
def save_recipe():
    pass

# ==================================================
# BLOCK 4: VIEW SAVED RECIPES
# ==================================================
# Functionality:
# - Retrieve saved recipes
# - Display saved recipes
# - Refresh recipe information if needed
def get_saved_recipes():
    pass

@app.route("/")
def home():
    return "RecipeWise: Work in Progress Part 1!"

if __name__ == "__main__":
    app.run(debug=True)