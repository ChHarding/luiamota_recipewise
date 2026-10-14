# 
# VERSION 1: THIS CODE WAS CREATED TO TEST THE FUNCTIONALITY OF THE SEARCH RECIPES FEATURE.
# NOW, SINCE THE PROJECT IS EVOLVING, THIS CODE WAS EDITED ON THE MAIN.PY FILE AND IS NO LONGER NEEDED.
# THE CODE BELOW IS KEPT HERE FOR REFERENCE PURPOSES ONLY.
# THE NEW CODE ON MAIN.PY FILE IS NOW CONNECTING FLASK WITH THE SEARCH RECIPES FEATURE.
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
        for meal in data['meals']:
            print(meal['strMeal'])

#search_recipes()