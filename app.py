import os

import psycopg2
from fastapi import FastAPI, HTTPException

import db
from db_setup import get_connection

app = FastAPI()

"""
Endpoints for FastAPI
"""

# Users
@app.post("/users", status_code=201)
def create_user(
    username: str,
    email: str,
    password: str,
    date_of_birth: str,
    phone_number: str,
):
    try:
        connection = get_connection()
        # Call db function to insert user and return the ID
        new_user = db.create_user(
            connection,
            username,
            email,
            password,
            date_of_birth,
            phone_number,
        )
        return new_user
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong:{error}")


@app.get("/users/email")
def get_user_by_email(email: str):
    try:
        connection = get_connection()
        user_by_email = db.get_user_by_email(connection, email)
        # Returns dictionary with user data (not password)
        return user_by_email
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong {error}")


@app.get("/users/username")
def get_user_by_username(username: str):
    try:
        connection = get_connection()
        user_by_username = db.get_user_by_username(connection, username)
        # Returns dictionary with user data (not password)
        return user_by_username
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong {error}")


@app.get("/users")
def get_all_users():
    try:
        connection = get_connection()
        all_users = db.get_all_users(connection)
        # Returns a list of user dictionaries
        return all_users
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong {error}")


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    try:
        connection = get_connection()
        user_by_id = db.get_user_by_id(connection, user_id)
        # Returns dictionary with all user data
        return user_by_id
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong {error}")


@app.put("/users/{user_id}")
def update_user(user_id: int, email: str = None, phone_number: str = None):
    try:
        connection = get_connection()
        updated_user = db.update_user(connection, user_id, email, phone_number)
        # Returns dictionary with updated user data
        return updated_user
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong {error}")


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    try:
        connection = get_connection()
        deleted_user = db.delete_user(connection, user_id)
        # Returns dictionary with deleted user's data, returns None if user doesn't exist
        return deleted_user
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong {error}")


# Transactions
@app.post("/transactions", status_code=201)
def create_transaction(
    user_id: int, listing_id: int, amount: int, status: str, bid_id: int = None
):
    try:
        connection = get_connection()
        new_transaction = db.create_transaction(
            connection, user_id, listing_id, amount, status, bid_id
        )
        return new_transaction
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/transactions")
def get_all_transactions():
    try:
        connection = get_connection()
        all_transactions = db.get_all_transactions(connection)
        return all_transactions
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong {error}")


@app.get("/transactions/{transaction_id}")
def get_transaction_by_id(transaction_id: int):
    try:
        connection = get_connection()
        transaction_by_id = db.get_transaction_by_id(connection, transaction_id)
        return transaction_by_id
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong {error}")


@app.get("/transactions/users/{user_id}")
def get_transactions_by_user_id(user_id: int):
    try:
        connection = get_connection()
        transaction_by_user_id = db.get_transactions_by_user_id(connection, user_id)
        return transaction_by_user_id
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong {error}")


@app.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int, new_status: str):
    try:
        connection = get_connection()
        updated_transaction = db.update_transaction(
            connection, transaction_id, new_status
        )
        return updated_transaction
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong {error}")


# Notifications
@app.post("/notifications", status_code=201)
def create_notification(
    user_id: int, listing_id: int, notification_type: str, notification_message: str
):
    try:
        connection = get_connection()
        new_notification = db.create_notification(
            connection, user_id, listing_id, notification_type, notification_message
        )
        return new_notification
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/notifications/{user_id}")
def get_notifications_by_user_id(user_id: int):
    try:
        connection = get_connection()
        notifications = db.get_notifications_by_user_id(connection, user_id)
        return notifications
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/notifications/unread")
def get_unread_notifications(user_id: int):
    try:
        connection = get_connection()
        user_unread_notifications = db.get_unread_notifications(connection, user_id)
        return user_unread_notifications
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.put("/notifications/mark-read")
def mark_notifications_as_read(user_id: int):
    try:
        connection = get_connection()
        marked_notifications = db.mark_all_notifications_as_read(connection, user_id)
        return marked_notifications
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.delete("/notifications/delete")
def delete_notification(notification_id: int):
    try:
        connection = get_connection()
        deleted_notification = db.delete_notification(connection, notification_id)
        return deleted_notification
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


# Shipping_details
@app.post("/shipping-details", status_code=201)
def create_shipping_details(
    user_id: int,
    listing_id: int,
    shipping_method: str,
    shipping_cost: float,
    estimated_delivery_days: int = None,
    tracking_number: str = None,
    status: str = None,
    shipped_at: str = None,
):
    try:
        connection = get_connection()
        shipping_detail = db.create_shipping_details(
            connection,
            user_id,
            listing_id,
            shipping_method,
            shipping_cost,
            estimated_delivery_days,
            tracking_number,
            status,
            shipped_at,
        )
        return shipping_detail
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/shipping-details/{listing_id}")
def get_shipping_details_by_listing_id(listing_id: int):
    try:
        connection = get_connection()
        shipping_by_listing_id = db.get_shipping_by_listing_id(connection, listing_id)
        return shipping_by_listing_id
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.put("/shipping-details/update")
def update_shipping(
    tracking_number: str, shipping_id: int, status: str, shipped_at: str = None
):
    try:
        connection = get_connection()
        new_shipping = db.update_shipping_tracking(
            connection, tracking_number, shipping_id, status, shipped_at
        )
        return new_shipping
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


# Listing_comments
@app.post("/listing_comments", status_code=201)
def create_listing_comment(user_id: int, listing_id: int, comment_text: str):
    try:
        connection = get_connection()
        new_listing_comment = db.create_listing_comment(
            connection, user_id, listing_id, comment_text
        )
        return new_listing_comment
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/listing_comments/{listing_id}")
def get_comments_by_listing_id(listing_id: int):
    try:
        connection = get_connection()
        comment_by_listing = db.get_comments_by_listing_id(connection, listing_id)
        return comment_by_listing
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/listing_comments/user/{user_id}")
def get_comments_by_user_id(user_id: int):
    try:
        connection = get_connection()
        comment_by_user = db.get_comments_by_user_id(connection, user_id)
        return comment_by_user
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.put("/listing_comments/answer")
def answer_comment(answer_text: str, comment_id: int):
    try:
        connection = get_connection()
        answer_to_comment = db.answer_comment(connection, answer_text, comment_id)
        return answer_to_comment
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.delete("/listing_comments/delete")
def delete_listing_comment(comment_id: int):
    try:
        connection = get_connection()
        deleted_comment = db.delete_listing_comment(connection, comment_id)
        return deleted_comment
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


# Categories
@app.get("/categories")
def get_all_categories():
    try:
        connection = get_connection()
        categories = db.get_all_categories(connection)
        return categories
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/categories/{category_id}")
def get_category_by_id(category_id: int):
    try:
        connection = get_connection()
        category_by_id = db.get_category_by_id(connection, category_id)
        if category_by_id is None:
            raise HTTPException(status_code=404, detail="Category not found.")
        return category_by_id
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


# Listings
@app.post("/listings", status_code=201)
def create_listing(
    user_id: int,
    category_id: int,
    title: str,
    listing_type: str,
    price: float,
    region: str,
    description: str,
    image_url: str = None
):
    try:
        connection = get_connection()
        new_listing = db.create_listing(
            connection,
            user_id,
            category_id,
            title,
            listing_type,
            price,
            region,
            description,
            image_url
        )
        return new_listing
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/listings")
def get_all_listings():
    try:
        connection = get_connection()
        all_listings = db.get_all_listings(connection)
        return {"listings": all_listings}
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/listings/search")
def search_listings(search_term: str):
    try:
        connection = get_connection()
        searched_listings = db.search_listings(connection, search_term)
        return searched_listings
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/listings/{listing_id}")
def get_listing_by_id(listing_id: int):
    try:
        connection = get_connection()
        listing_by_id = db.get_listing_by_id(connection, listing_id)
        if listing_by_id is None:
            raise HTTPException(status_code=404, detail="Listing not found.")
        return listing_by_id
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


# Testa ev detta: int | None
@app.patch("/listings/{listing_id}")
def update_listing(
    listing_id: int,
    category_id: int = None,
    title: str = None,
    listing_type: str = None,
    price: float = None,
    region: str = None,
    description: str = None,
    image_url: str = None
):
    try:
        connection = get_connection()
        updated_listing = db.update_listing(
            connection,
            listing_id,
            category_id,
            title,
            listing_type,
            price,
            region,
            description,
            image_url
        )
        if updated_listing is None:
            raise HTTPException(status_code=404, detail="Listing not found.")
        return updated_listing
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.delete("/listings/{listing_id}")
def delete_listing(listing_id: int):
    try:
        connection = get_connection()
        deleted_listing = db.delete_listing(connection, listing_id)
        if deleted_listing is None:
            raise HTTPException(status_code=404, detail="Listing not found.")
        return {
            "message": f"Listing with listing id {listing_id} deleted.",
            "deleted_listing": deleted_listing
        }
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/listings/categories/{category_id}")
def get_listings_by_category(category_id: int):
    try:
        connection = get_connection()
        listings_by_category = db.get_listings_by_category(connection, category_id)
        return listings_by_category
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


# Listings_watch_list
@app.post("/listings_watch_list", status_code=201)
def add_to_watch_list(user_id: int, listing_id: int):
    try:
        connection = get_connection()
        new_watch_listing = db.add_to_watch_list(connection, user_id, listing_id)
        if new_watch_listing is None:
            raise HTTPException(status_code=404, detail="Listing not found.")
        return new_watch_listing
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/listings_watch_list/{user_id}")
def get_all_watched_listings_for_user(user_id: int):
    try:
        connection = get_connection()
        watched_listings = db.get_all_watched_listings(connection, user_id)
        return {"listings_watch_list": watched_listings}
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.delete("/listings_watch_list/{user_id}/{listing_id}")
def delete_watch_listing(user_id: int, listing_id: int):
    try:
        connection = get_connection()
        removed_watch_listing = db.remove_from_watch_list(connection, user_id, listing_id)
        if removed_watch_listing is None:
            raise HTTPException(status_code=404, detail="Listing not found.")
        return {"message": f"Listing with id {listing_id} removed from watch list."}
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


# Messages
@app.post("/messages", status_code=201)
def create_message(
    sender_id: int,
    recipent_id: int,
    listing_id: int,
    message_text: str
):
    try:
        connection = get_connection()
        new_message = db.create_message(
            connection,
            sender_id,
            recipent_id,
            listing_id,
            message_text
        )
        return new_message
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/messages")
def get_all_messages():
    try:
        connection = get_connection()
        all_messages = db.get_all_messages(connection)
        return {"messages": all_messages}
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/users/{user_id}/messages")
def get_user_messages(user_id: int):
    try:
        connection = get_connection()
        user_messages = db.get_all_user_messages(connection, user_id)
        return {"messages": user_messages}
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/messages/{message_id}")
def get_message_by_id(message_id: int):
    try:
        connection = get_connection()
        message_by_id = db.get_message_by_id(connection, message_id)
        if message_by_id is None:
            raise HTTPException(status_code=404, detail="Message not found.")
        return message_by_id
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.delete("/messages/{message_id}")
def delete_message(message_id: int):
    try:
        connection = get_connection()
        deleted_message = db.delete_message(connection, message_id)
        if deleted_message is None:
            raise HTTPException(status_code=404, detail="Message not found.")
        return {"message": f"Message with id {message_id} deleted."}
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


# Payments
@app.post("/payments", status_code=201)
def create_payment(
    transaction_id: int,
    listing_id: int,
    payment_method: str,
    amount: float,
):
    try:
        connection = get_connection()
        new_payment = db.create_payment(
            connection,
            transaction_id,
            listing_id,
            payment_method,
            amount
        )
        return new_payment
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/payments")
def get_all_payments():
    try:
        connection = get_connection()
        all_payments = db.get_all_payments(connection)
        return {"payments": all_payments}
    except HTTPException as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/users/{user_id}/payments")
def get_user_payments(user_id: int):
    try:
        connection = get_connection()
        user_payments = db.get_all_user_payments(connection, user_id)
        return {"payments": user_payments}
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/payments/{payment_id}")
def get_payment_by_id(payment_id: int):
    try:
        connection = get_connection()
        payment_by_id = db.get_payment_by_id(connection, payment_id)
        if payment_by_id is None:
            raise HTTPException(status_code=404, detail=" Payment not found.")
        return payment_by_id
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.put("/payments/{payment_id}/refund")
def request_refund(payment_id: int):
    try:
        connection = get_connection()
        refund_request = db.request_refund(connection, payment_id)
        if refund_request is None:
            raise HTTPException(status_code=404, detail="Payment not found.")
        return refund_request
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.delete("/payments/{payment_id}")
def delete_payment(payment_id: int):
    try:
        connection = get_connection()
        deleted_payment = db.delete_payment(connection, payment_id)
        if deleted_payment is None:
            raise HTTPException(status_code=404, detail="Payment not found.")
        return {"message": f"Payment with id {payment_id} deleted."}
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


# Bids
@app.post("/bids", status_code=201)
def create_bid(user_id: int, listing_id: int, amount: float):
    try:
        connection = get_connection()
        new_bid = db.create_bid(
            connection, user_id, listing_id, amount) 
        return new_bid
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/bids")
def get_all_bids():
    try:
        connection = get_connection()
        all_bids = db.get_all_bids(connection)
        return {"bids": all_bids}
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
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/listings/{listing_id}/bids")
def get_bids_for_listing(listing_id: int):
    try:
        connection = get_connection()
        bids_for_listing = db.get_bids_for_listing(connection, listing_id)
        return {"bids": bids_for_listing}  # If a listing has no bids it returns an empty list
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.delete("/bids/{bid_id}")
def delete_bid(bid_id: int):
    try:
        connection = get_connection()
        deleted_bid = db.delete_bid(connection, bid_id)
        if deleted_bid is None:
            raise HTTPException(status_code=404, detail="Bid not found.")
        return {"message": f"Bid with id {bid_id} deleted."}
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
        new_rating = db.create_user_rating(connection, user_id, total_ratings, average_rating)
        return new_rating
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


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
        if user_rating is None:
            raise HTTPException(status_code=404, detail="Rating not found.")
        return user_rating
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.put("/users/{user_id}/rating")
def update_user_rating(
    user_id: int, total_ratings: int = None, average_rating: float = None):
    try:
        connection = get_connection()
        updated_rating = db.update_user_rating(connection, user_id, total_ratings, average_rating)
        if updated_rating is None:
            raise HTTPException(status_code=404, detail="Rating not found.")
        return updated_rating
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.delete("/users/{user_id}/rating")
def delete_user_rating(user_id: int):
    try:
        connection = get_connection()
        deleted_rating = db.delete_user_rating(connection, user_id)
        if deleted_rating is None:
            raise HTTPException(status_code=404, detail="Rating not found.")
        return {
            "message": f"Rating for user {user_id} deleted.",
            "deleted_rating": deleted_rating
        }
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


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
            connection, 
            reviewer_id, 
            reviewed_user_id, 
            listing_id, 
            rating, 
            review_text
        )
        return new_review
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/reviews")
def get_all_reviews():
    try:
        connection = get_connection()
        all_reviews = db.get_all_reviews(connection)
        return {"reviews": all_reviews}
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/reviews/{review_id}")
def get_review(review_id: int):
    try:
        connection = get_connection()
        review_by_id = db.get_review_by_id(connection, review_id)
        if review_by_id is None:
            raise HTTPException(status_code=404, detail="Review not found.")
        return review_by_id
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/users/{user_id}/reviews")
def get_reviews_for_user(user_id: int):
    try:
        connection = get_connection()
        reviews_for_user = db.get_reviews_for_user(connection, user_id)
        return {"reviews": reviews_for_user}
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.delete("/reviews/{review_id}")
def delete_review(review_id: int):
    try:
        connection = get_connection()
        deleted_review = db.delete_review(connection, review_id)
        if deleted_review is None:
            raise HTTPException(status_code=404, detail="Review not found.")
        return {
            "message": f"Review with id {review_id} deleted.",
            "deleted_review": deleted_review
        }
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


# Reports
@app.post("/reports", status_code=201)
def create_report(user_id: int, listing_id: int, report_reason: str):
    try:
        connection = get_connection()
        new_report = db.create_report(connection, user_id, listing_id, report_reason)
        return new_report
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/reports")
def get_all_reports():
    try:
        connection = get_connection()
        all_reports = db.get_all_reports(connection)
        return {"reports": all_reports}
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/reports/{report_id}")
def get_report(report_id: int):
    try:
        connection = get_connection()
        report_by_id = db.get_report_by_id(connection, report_id)
        if report_by_id is None:
            raise HTTPException(status_code=404, detail="Report not found.")
        return report_by_id
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/listings/{listing_id}/reports")
def get_reports_for_listing(listing_id: int):
    try:
        connection = get_connection()
        reports_for_listing = db.get_reports_for_listing(connection, listing_id)
        return {"reports": reports_for_listing}
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.delete("/reports/{report_id}")
def delete_report(report_id: int):
    try:
        connection = get_connection()
        deleted_report = db.delete_report(connection, report_id)
        if deleted_report is None:
            raise HTTPException(status_code=404, detail="Report not found.")
        return {
            "message": f"Report with id {report_id} deleted.",
            "deleted_report": deleted_report
        }
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


# Images
@app.post("/images", status_code=201)
def create_image(user_id: int, listing_id: int, image_url: str):
    try:
        connection = get_connection()
        new_image = db.create_image(connection, user_id, listing_id, image_url)
        return new_image
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/images")
def get_all_images():
    try:
        connection = get_connection()
        all_images = db.get_all_images(connection)
        return {"images": all_images}
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/images/{image_id}")
def get_image(image_id: int):
    try:
        connection = get_connection()
        image_by_id = db.get_image_by_id(connection, image_id)
        if image_by_id is None:
            raise HTTPException(status_code=404, detail="Image not found.")
        return image_by_id
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.get("/listings/{listing_id}/images")
def get_images_for_listing(listing_id: int):
    try:
        connection = get_connection()
        images_for_listing = db.get_images_for_listing(connection, listing_id)
        return {"images": images_for_listing}
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")


@app.delete("/images/{image_id}")
def delete_image(image_id: int):
    try:
        connection = get_connection()
        deleted_image = db.delete_image(connection, image_id)
        if deleted_image is None:
            raise HTTPException(status_code=404, detail="Image not found.")
        return {f"message: Image with {image_id} deleted."}
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {error}")
