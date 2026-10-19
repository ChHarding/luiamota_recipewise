"""
SUPABASE

Purpose: 
This file creates and stores the connection between RecipeWise
and Supabase database.

"""
# Import create_client from Supabase to create a database connection.
from supabase import create_client

# URL of the RecipeWise Supabase project.
url = "https://abjgsrimmsyjgvjxezyy.supabase.co"

# Public API key used to connect the application to Supabase.
key = "sb_publishable_pKS7XPkqFelBFTbtlDX20w_0cPvVaj2"

# Creates a reusable client to interact with the database.
supabase = create_client (url, key)