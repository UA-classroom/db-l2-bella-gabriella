import psycopg2
from psycopg2.extras import RealDictCursor

"""
This file is responsible for making database queries, which your fastapi endpoints/routes can use.
The reason we split them up is to avoid clutter in the endpoints, so that the endpoints might focus on other tasks 

- Try to return results with cursor.fetchall() or cursor.fetchone() when possible
- Make sure you always give the user response if something went right or wrong, sometimes 
you might need to use the RETURNING keyword to garantuee that something went right / wrong
e.g when making DELETE or UPDATE queries
- No need to use a class here
- Try to raise exceptions to make them more reusable and work a lot with returns
- You will need to decide which parameters each function should receive. All functions 
start with a connection parameter.
- Below, a few inspirational functions exist - feel free to completely ignore how they are structured
- E.g, if you decide to use psycopg3, you'd be able to directly use pydantic models with the cursor, these examples are however using psycopg2 and RealDictCursor
"""

# Categories
def get_all_categories(connection):
    with connection:
        # Creates a cursor to run SQL commands
        # RealDictCursor turns the results into dictionarys (easier to read)
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM categories;") # Run SQL ("Fetch everything from the table categories")
            categories = cursor.fetchall() # Fetch all the results and saves it in the varible categories
        return categories # Returns the result
    
# Listings
def get_all_listings(connection):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM listings;")
            listings = cursor.fetchall()
        return listings
    
def get_listing_by_id(connection, listing_id): # Parameter: listing_id
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM listings WHERE id = %s;", (listing_id,)) # %s: placeholder for listing_id
            listing = cursor.fetchone() # Fetch only one result (the first one)
        return listing
    
def create_listing(connection, user_id, category_id, title, listing_type, price, region, status, description, image_url=None):
    """ Creates a new listing in the database """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO listings 
                (user_id, category_id, title, listing_type, price, region, status, description, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;""",
                # Run SQL ("Insert a new listing with these values")
                # RETURNING *: return the new row that was created
                # %s: placeholder for each value
                (user_id, category_id, title, listing_type, price, region, status, description, image_url) # Sending all the values
            )
            new_listing = cursor.fetchone() # Fetch only one result (the first one)
        return new_listing
    
def update_listing(connection, listing_id, category_id=None, title=None, listing_type=None, price=None, region=None, status=None, description=None, image_url=None):
    """ Updates an existing listing with the values that the user choose """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                # COALESCE: if there is no new value, keep the old value
                # WHERE id = %s: only update this listing
                """UPDATE listings SET
                category_id = COALESCE(%s, category_id),
                title = COALESCE(%s, title),
                listing_type = COALESCE(%s, listing_type),
                price = COALESCE(%s, price),
                region = COALESCE(%s, region),
                status = COALESCE(%s, status),
                description = COALESCE(%s, description),
                image_url = COALESCE(%s, image_url)
                WHERE id = %s RETURNING *;""",
                (listing_id, category_id, title, listing_type, price, region, status, description, image_url)
            )
            updated_listing = cursor.fetchone()
        return updated_listing
    
def delete_listing(connection, listing_id):
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("DELETE FROM listings WHERE id = %s * RETURNING *;")
                deleted_listing = cursor.fetchone()
        return deleted_listing


### THIS IS JUST AN EXAMPLE OF A FUNCTION FOR INSPIRATION FOR A LIST-OPERATION (FETCHING MANY ENTRIES)
# def get_items(con):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("SELECT * FROM items;")
#             items = cursor.fetchall()
#     return items


### THIS IS JUST INSPIRATION FOR A DETAIL OPERATION (FETCHING ONE ENTRY)
# def get_item(con, item_id):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("""SELECT * FROM items WHERE id = %s""", (item_id,))
#             item = cursor.fetchone()
#             return item


### THIS IS JUST INSPIRATION FOR A CREATE-OPERATION
# def add_item(con, title, description):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute(
#                 "INSERT INTO items (title, description) VALUES (%s, %s) RETURNING id;",
#                 (title, description),
#             )
#             item_id = cursor.fetchone()["id"]
#     return item_id
