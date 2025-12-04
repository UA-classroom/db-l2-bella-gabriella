import os
import psycopg2
import db
from db_setup import get_connection
from fastapi import FastAPI, HTTPException

app = FastAPI()

"""
ADD ENDPOINTS FOR FASTAPI HERE
Make sure to do the following:
- Use the correct HTTP method (e.g get, post, put, delete)
- Use correct STATUS CODES, e.g 200, 400, 401 etc. when returning a result to the user
- Use pydantic models whenever you receive user data and need to validate the structure and data types (VG)
This means you need some error handling that determine what should be returned to the user
Read more: https://www.geeksforgeeks.org/10-most-common-http-status-codes/
- Use correct URL paths the resource, e.g some endpoints should be located at the exact same URL, 
but will have different HTTP-verbs.
"""


# INSPIRATION FOR A LIST-ENDPOINT - Not necessary to use pydantic models, but we could to ascertain that we return the correct values
# @app.get("/items/")
# def read_items():
#     con = get_connection()
#     items = get_items(con)
#     return {"items": items}


# INSPIRATION FOR A POST-ENDPOINT, uses a pydantic model to validate
# @app.post("/validation_items/")
# def create_item_validation(item: ItemCreate):
#     con = get_connection()
#     item_id = add_item_validation(con, item)
#     return {"item_id": item_id}

# Categories

# Listings

# Messages

# Listings_watch_list

# Payments

# Bids
@app.post("/bids", status_code=201)
def create_bid(user_id: int, listing_id: int, bid_amount: float):
    try:
        connection = get_connection() # Get database connection
        new_bid = db.create_bid(connection, user_id, listing_id, bid_amount) # Call the function from the database
        return new_bid
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")

@app.get("/bids")
def get_all_bids():
    try:
        connection = get_connection() 
        bids = db.get_all_bids(connection)
        return {"bids": bids}
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")

@app.get("/bids/{bid_id}")
def get_bid_by_id(bid_id: int):
    try:
        connection = get_connection()
        bid_by_id = db.get_bid_by_id(connection, bid_id)
        if bid_by_id is None:
            raise HTTPException(status_code=404, detail="Bid not found.")
        return bid_by_id
    except HTTPException: # Catch the 404-HTTPException
        raise
    except Exception as error: # Catch unexpected errors
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")

@app.get("/listings/{listing_id}/bids")
def get_bids_for_listing(listing_id: int):
    try:
        connection = get_connection()
        bids_for_listing = db.get_bids_for_listing(connection, listing_id)
        return {"bids": bids_for_listing} # If a listing has no bids it returns an empty list
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")

@app.delete("/bids/{bid_id}")
def delete_bid(bid_id: int):
    try:
        connection = get_connection()
        deleted_bid = db.delete_bid(connection, bid_id)
        if deleted_bid is None:
            raise HTTPException(status_code=404, detail="Bid not found.")
        return deleted_bid
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")

# User_ratings
@app.post("/user-ratings", status_code=201)
def create_user_rating(
    user_id: int, total_ratings: int = 0, average_rating: float = 0.00):
    try:
        connection = get_connection()
        new_rating = db.create_user_rating(
            connection, user_id, total_ratings, average_rating
        )
        return new_rating
    except Exception as error:
        raise HTTPException(status_code=500, detail="Error, could not create rating.")

@app.get("/user-ratings")
def get_all_user_ratings():
    try:
        connection = get_connection()
        all_ratings = db.get_all_user_ratings(connection)
        return {"ratings": all_ratings}
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")

@app.get("/users/{user_id}/rating")
def get_user_rating(user_id: int):
    try:
        connection = get_connection()
        user_rating = db.get_user_rating_by_user_id(connection, user_id)
        return user_rating
    except Exception as error:
        raise HTTPException(status_code=500, detail="Something went wrong.")

@app.put("/users/{user_id}/rating")
def update_user_rating(
    user_id: int, total_ratings: int = None, average_rating: float = None):
    try:
        connection = get_connection()
        updated_rating = db.update_user_rating(
            connection, user_id, total_ratings, average_rating
        )
        return updated_rating
    except Exception as error:
        raise HTTPException(status_code=500, detail="Error, could not update rating.")

@app.delete("/users/{user_id}/rating")
def delete_user_rating(user_id: int):
    try:
        connection = get_connection()
        result = db.delete_user_rating(connection, user_id)
        return result
    except Exception as error:
        raise HTTPException(status_code=500, detail="Something went wrong.")

# Reviews
@app.post("/reviews", status_code=201)
def create_review(
    reviewer_id: int,
    reviewed_user_id: int,
    listing_id: int,
    rating: int,
    review_text: str = None,
):
    try:
        connection = get_connection()
        new_review = db.create_review(
            connection, reviewer_id, reviewed_user_id, listing_id, rating, review_text
        )
        return new_review
    except Exception as error:
        raise HTTPException(status_code=500, detail="Error, could not create review.")

@app.get("/reviews")
def get_all_reviews():
    try:
        connection = get_connection()
        all_reviews = db.get_all_reviews(connection)
        return {"reviews": all_reviews}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Something went wrong.")

@app.get("/reviews/{review_id}")
def get_review(review_id: int):
    try:
        connection = get_connection()
        review = db.get_review_by_id(connection, review_id)
        return review
    except Exception as error:
        raise HTTPException(status_code=500, detail="Something went wrong.")

@app.get("/users/{user_id}/reviews")
def get_reviews_for_user(user_id: int):
    try:
        connection = get_connection()
        reviews_for_user = db.get_reviews_for_user(connection, user_id)
        return {"reviews": reviews_for_user}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Something went wrong.")

@app.delete("/reviews/{review_id}")
def delete_review(review_id: int):
    try:
        connection = get_connection()
        deleted_review = db.delete_review(connection, review_id)
        return deleted_review
    except Exception as error:
        raise HTTPException(status_code=500, detail="Something went wrong.")

# Images
@app.post("/images", status_code=201)
def create_image(user_id: int, listing_id: int, image_url: str):
    try:
        connection = get_connection()
        new_image = db.create_image(connection, user_id, listing_id, image_url)
        return new_image
    except Exception as error:
        raise HTTPException(status_code=500, detail="Error, could not create image.")

@app.get("/images")
def get_all_images():
    """Hämtar alla bilder"""
    try:
        connection = get_connection()
        all_images = db.get_all_images(connection)
        return {"images": all_images}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Something went wrong.")

@app.get("/images/{image_id}")
def get_image(image_id: int):
    try:
        connection = get_connection()
        image = db.get_image_by_id(connection, image_id)
        return image
    except Exception as error:
        raise HTTPException(status_code=500, detail="Something went wrong.")

@app.get("/listings/{listing_id}/images")
def get_images_for_listing(listing_id: int):
    try:
        connection = get_connection()
        images_for_listing = db.get_images_for_listing(connection, listing_id)
        return {"images": images_for_listing}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Something went wrong.")

@app.delete("/images/{image_id}")
def delete_image(image_id: int):
    try:
        connection = get_connection()
        deleted_image = db.delete_image(connection, image_id)
        return deleted_image
    except Exception as error:
        raise HTTPException(status_code=500, detail="Something went wrong.")

# Reports
@app.post("/reports", status_code=201)
def create_report(user_id: int, listing_id: int, report_reason: str):
    try:
        connection = get_connection()
        new_report = db.create_report(connection, user_id, listing_id, report_reason)
        return new_report
    except Exception as error:
        raise HTTPException(status_code=500, detail="Error, could not create report.")

@app.get("/reports")
def get_all_reports():
    try:
        connection = get_connection()
        all_reports = db.get_all_reports(connection)
        return {"reports": all_reports}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Something went wrong.")

@app.get("/reports/{report_id}")
def get_report(report_id: int):
    try:
        connection = get_connection()
        report = db.get_report_by_id(connection, report_id)
        return report
    except Exception as error:
        raise HTTPException(status_code=500, detail="Something went wrong.")

@app.get("/listings/{listing_id}/reports")
def get_reports_for_listing(listing_id: int):
    try:
        connection = get_connection()
        reports_for_listing = db.get_reports_for_listing(connection, listing_id)
        return {"reports": reports_for_listing}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Something went wrong.")

@app.delete("/reports/{report_id}")
def delete_report(report_id: int):
    try:
        connection = get_connection()
        deleted_report = db.delete_report(connection, report_id)
        return deleted_report
    except Exception as error:
        raise HTTPException(status_code=500, detail="Something went wrong.")
