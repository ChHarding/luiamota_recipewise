"""
SUPABASE CONNECTION TEST

Note:
This file is for testing purposes only and is not part of the
main application functionality.
"""


from supabase_client import supabase

response = (
    supabase.table("favorites")
    .insert({
        "meal_id": "123",
        "meal_name": "Test Recipe",
        "meal_image": "test.jpg",
        "meal_area": "Mexican"
    })
    .execute()
)


print (response.data)

