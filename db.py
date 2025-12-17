import psycopg2
from fastapi import HTTPException
from psycopg2.extras import RealDictCursor

"""
This file contains database functions for FastAPI endpoints.
Each function execute queries, returns the result and handles exceptions when necessary. 
"""

# Users
def create_user(
    connection, username, email, password, date_of_birth, phone_number
):
    # open connection
    with connection:
        # create cursor
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO users (username, email, password, date_of_birth, phone_number) 
                VALUES (%s, %s, %s, %s, %s) 
                RETURNING *;""",
                (username, email, password, date_of_birth, phone_number),
            )
            new_user = cursor.fetchone()
        return new_user


def get_user_by_id(connection, user_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
            SELECT id, username, email, user_since, date_of_birth, phone_number 
            FROM users 
            WHERE id = %s""",
                (user_id,),
            )
            user_by_id = cursor.fetchone()
        return user_by_id


# get user by email for login
def get_user_by_email(connection, email):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
            SELECT id, username, email, user_since, date_of_birth, phone_number 
            FROM users 
            WHERE email = %s""",
                (email,),
            )
            user_by_email = cursor.fetchone()
        return user_by_email


# get user by username for login
def get_user_by_username(connection, username):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
            SELECT id, username, email, user_since, date_of_birth, phone_number 
            FROM users 
            WHERE username = %s""",
                (username,),
            )
            user_by_username = cursor.fetchone()
        return user_by_username


def get_all_users(connection):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users;")
            all_users = cursor.fetchall()
        return all_users


def update_user(connection, user_id, email=None, phone_number=None):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE users 
                SET email = COALESCE (%s, email),
                    phone_number = COALESCE (%s, phone_number)
                WHERE id = %s RETURNING *;
                """,
                (email, phone_number, user_id),
            )
            updated_user = cursor.fetchone()
        return updated_user


def delete_user(connection, user_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s RETURNING *;", (user_id,))
            deleted_user = cursor.fetchone()
            return deleted_user


# Categories
def get_all_categories(connection):
    """ Returns all categories """
    with connection:
        # Create a cursor to run SQL commands
        # RealDictCursor turn the results into dictionarys
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(  # Run SQL ("Fetch everything from the table categories")
                """
                SELECT * 
                FROM categories;
                """
            )
            all_categories = cursor.fetchall()  # Fetch all the results
        return all_categories


def get_category_by_id(connection, category_id):
    """ Returns a category with a specific id """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM categories 
                WHERE id = %s;
                """,
                (category_id,)
            )
            category_by_id = cursor.fetchone()
        if category_by_id is None:
            raise ValueError(f"Category with id {category_id} not found.")
    return category_by_id


# Listings
def create_listing(
    connection,
    user_id,
    category_id,
    title,
    listing_type,
    price,
    region,
    description,
    image_url=None,
):
    """ Creates a new listing in the database """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute( # Run SQL ("Insert a new listing with these values")
                """
                INSERT INTO listings 
                (user_id, category_id, title, listing_type, price, region, description, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
                RETURNING *;
                """,
                # RETURNING *: return the new row that was created
                # %s: placeholder for each value
                (
                    user_id,
                    category_id,
                    title,
                    listing_type,
                    price,
                    region,
                    description,
                    image_url,
                ) # Sending all the values
            )
            new_listing = cursor.fetchone() # Fetch only one result (the first one)
        return new_listing


def get_all_listings(connection):
    """ Returns all listings """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM listings;
                """
            )
            all_listings = cursor.fetchall()
        return all_listings


def get_listing_by_id(connection, listing_id):
    """ Returns a listing with a specific id """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM listings 
                WHERE id = %s;
                """,
                (listing_id,)
            )  # %s: placeholder for listing_id
            listing_by_id = cursor.fetchone()
        if listing_by_id is None:
            raise ValueError(f"Listing with id {listing_id} not found.")
    return listing_by_id


def update_listing(
    connection,
    listing_id,
    category_id=None,
    title=None,
    listing_type=None,
    price=None,
    region=None,
    description=None,
    image_url=None,
):
    """ Partially updates a listing with the given values, keeping the other values unchanged """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                # COALESCE: if there is no new value, keep the old value
                # WHERE id = %s: only update this listing
                """
                UPDATE listings 
                SET
                category_id = COALESCE(%s, category_id),
                title = COALESCE(%s, title),
                listing_type = COALESCE(%s, listing_type),
                price = COALESCE(%s, price),
                region = COALESCE(%s, region),
                description = COALESCE(%s, description),
                image_url = COALESCE(%s, image_url)
                WHERE id = %s 
                RETURNING *;
                """,
                (
                    category_id,
                    title,
                    listing_type,
                    price,
                    region,
                    description,
                    image_url,
                    listing_id,
                )
            )
            updated_listing = cursor.fetchone()
        return updated_listing


def delete_listing(connection, listing_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                DELETE 
                FROM listings 
                WHERE id = %s 
                RETURNING *;
                """,
                (listing_id,)
            )
            deleted_listing = cursor.fetchone()
        if deleted_listing is None:
            raise ValueError(f"Listing with id {listing_id} not found.")
    return deleted_listing


def search_listings(connection, search_term):
    """ Searches listings by title and description """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                # ILIKE: makes the search case-insensitive
                """
                SELECT * 
                FROM listings 
                WHERE title ILIKE %s OR description ILIKE %s;
                """,
                (f"%{search_term}%", f"%{search_term}%") # %{search_term}%: search anywhere in the text
            )
            searched_listings = cursor.fetchall()
    return searched_listings


def get_listings_by_category(connection, category_id):
    """ Returns all listings with a specific category """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM listings 
                WHERE category_id = %s;
                """,
                (category_id,)
            )
            listings_by_category = cursor.fetchall()
    return listings_by_category


# Listings_watch_list
def add_to_watch_list(connection, user_id, listing_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO listings_watch_list (user_id, listing_id)
                VALUES (%s, %s) 
                RETURNING *;
                """,
                (user_id, listing_id)
            )
            new_watch_listing = cursor.fetchone()
        return new_watch_listing


def get_all_watched_listings(connection, user_id):
    """ Returns all watched_listing for a specific user """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM listings_watch_list 
                WHERE user_id = %s;
                """,
                (user_id,)
            )
            watched_listings = cursor.fetchall()
        return watched_listings


def remove_from_watch_list(connection, user_id, listing_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                DELETE 
                FROM listings_watch_list 
                WHERE user_id = %s AND listing_id = %s 
                RETURNING *;
                """,
                (user_id, listing_id)
            )
            deleted_watch_listing = cursor.fetchone()
        return deleted_watch_listing


# Messages
def create_message(connection, sender_id, recipient_id, listing_id, message_text):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO messages (sender_id, recipient_id, listing_id, message_text)
                VALUES (%s, %s, %s, %s) 
                RETURNING *;
                """,
                (sender_id, recipient_id, listing_id, message_text)
            )
            new_message = cursor.fetchone()
        return new_message


def get_all_messages(connection):
    """ Returns all messages """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM messages;
                """
            )
            all_messages = cursor.fetchall()
        return all_messages


def get_all_user_messages(connection, user_id):
    """ Returns all messages for a specific user """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM messages 
                WHERE sender_id= %s OR recipient_id = %s;
                """,
                (user_id, user_id)
            )
            user_messages = cursor.fetchall()
        return user_messages


def get_message_by_id(connection, message_id):
    """ Returns a message with a specific id """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM messages 
                WHERE id = %s;
                """,
                (message_id,)
            )
            message_by_id = cursor.fetchone()
        if message_by_id is None:
            raise ValueError(f"Message with id {message_id} not found.")
    return message_by_id


def delete_message(connection, message_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                DELETE 
                FROM messages 
                WHERE id = %s RETURNING *;
                """,
                (message_id,)
            )
            deleted_message = cursor.fetchone()
        if deleted_message is None:
            raise ValueError(f"Message with id {message_id} not found.")
    return deleted_message


# Payments
def create_payment(
    connection, transaction_id, listing_id, payment_method, amount
):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO payments 
                (transaction_id, listing_id, payment_method, amount) 
                VALUES (%s, %s, %s, %s) 
                RETURNING *;
                """,
                (transaction_id, listing_id, payment_method, amount)
            )
            new_payment = cursor.fetchone()
    return new_payment


def get_all_payments(connection):
    """ Returns all payments """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM payments;
                """
            )
            all_payments = cursor.fetchall()
        return all_payments


def get_all_user_payments(connection, user_id):
    """ Returns all payments for a specific user """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM payments 
                WHERE transaction_id 
                IN (SELECT id FROM transactions WHERE user_id = %s);
                """,
                (user_id,)
            )
            payments = cursor.fetchall()
    return payments


def get_payment_by_id(connection, payment_id):
    """ Returns a payment with a specific id """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM payments 
                WHERE id = %s;
                """,
                (payment_id,)
            )
            payment_by_id = cursor.fetchone()
        if payment_by_id is None:
            raise ValueError(f"Payment with id {payment_id} not found.")
    return payment_by_id


def request_refund(connection, payment_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE payments 
                SET payment_status = %s 
                WHERE id = %s 
                RETURNING *;
                """,
                ("refund_requested", payment_id)
            )
            refund_request = cursor.fetchone()
    return refund_request


def delete_payment(connection, payment_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                DELETE 
                FROM payments 
                WHERE id = %s 
                RETURNING id;
                """,
                (payment_id,)
            )
            deleted_payment = cursor.fetchone()
        if deleted_payment is None:
            raise ValueError(f"Payment with id {payment_id} not found.")
    return deleted_payment


# Bids
def create_bid(connection, user_id, listing_id, amount):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO bids (user_id, listing_id, amount)
                VALUES (%s, %s, %s)
                RETURNING *; 
                """,
                (user_id, listing_id, amount)
            )
            new_bid = cursor.fetchone()
    return new_bid


def get_all_bids(connection):
    """ Returns all bids """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM bids 
                ORDER BY created_at DESC;
                """
            )
            all_bids = cursor.fetchall()
    return all_bids


def get_bid_by_id(connection, bid_id):
    """ Returns a bid with a specific id """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM bids 
                WHERE id = %s;
                """,
                (bid_id,)
            )
            bid_by_id = cursor.fetchone()
        if bid_by_id is None:
            raise ValueError(f"Bid with id {bid_id} not found.")
    return bid_by_id


def get_bids_for_listing(connection, listing_id):
    """ Returns all bids for a listing """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM bids 
                WHERE listing_id = %s 
                ORDER BY amount DESC;
                """,
                (listing_id,)
            )
            bids_for_listing = cursor.fetchall()
    return bids_for_listing


def delete_bid(connection, bid_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                DELETE 
                FROM bids 
                WHERE id = %s 
                RETURNING id;
                """,
                (bid_id,)
            )
            deleted_bid = cursor.fetchone()
        if deleted_bid is None:
            raise ValueError(f"Bid with id {bid_id} not found.")
    return deleted_bid


# User_ratings
def create_user_rating(connection, user_id, total_ratings=0, average_rating=0.00):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO user_ratings (user_id, total_ratings, average_rating)
                VALUES (%s, %s, %s)
                RETURNING *;
                """,
                (user_id, total_ratings, average_rating)
            )
            new_rating = cursor.fetchone()
    return new_rating


def get_all_user_ratings(connection):
    """ Returns all user ratings """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM user_ratings;
                """
            )
            all_ratings = cursor.fetchall()
    return all_ratings


def get_user_rating_by_user_id(connection, user_id):
    """ Returns user rating for a specific user """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM user_ratings 
                WHERE user_id = %s;
                """,
                (user_id,)
            )
            rating_by_user_id = cursor.fetchone()
        if rating_by_user_id is None:
            raise ValueError(f"Rating for user {user_id} not found.")
    return rating_by_user_id


def update_user_rating(connection, user_id, average_rating, total_ratings):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE user_ratings 
                SET average_rating = %s, total_ratings = %s
                WHERE user_id = %s 
                RETURNING *;
                """,
                (average_rating, total_ratings, user_id)
            )
            updated_rating = cursor.fetchone()
        if updated_rating is None:
            raise ValueError(f"Rating for user {user_id} not found.")
    return updated_rating


def delete_user_rating(connection, user_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                DELETE 
                FROM user_ratings 
                WHERE user_id = %s 
                RETURNING id;
                """,
                (user_id,)
            )
            deleted_rating = cursor.fetchone()
        if deleted_rating is None:
            raise ValueError(f"Rating for user {user_id} not found.")
    return deleted_rating


# Reviews
def create_review(connection, reviewer_id, reviewed_user_id, listing_id, rating, review_text=None):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO reviews (reviewer_id, reviewed_user_id, listing_id, rating, review_text)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (reviewer_id, reviewed_user_id, listing_id, rating, review_text)
            )
            new_review = cursor.fetchone()
    return new_review


def get_all_reviews(conncection):
    """ Returns all reviews """
    with conncection:
        with conncection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM reviews 
                ORDER BY created_at DESC;
                """
            )
            all_reviews = cursor.fetchall()
    return all_reviews


def get_review_by_id(connection, review_id):
    """ Returns a review with a specific id """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM reviews 
                WHERE id = %s;""",
                (review_id,)
            )
            review_by_id = cursor.fetchone()
        if review_by_id is None:
            raise ValueError(f"Review with id {review_id} not found.")
    return review_by_id


def get_reviews_for_user(connection, user_id):
    """ Returns all the reviews for a specific user """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM reviews 
                WHERE reviewed_user_id = %s 
                ORDER BY created_at DESC;
                """,
                (user_id,)
            )
            reviews_for_user = cursor.fetchall()
    return reviews_for_user


def delete_review(connection, review_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                DELETE FROM reviews 
                WHERE id = %s 
                RETURNING id;
                """,
                (review_id,)
            )
            deleted_review = cursor.fetchone()
        if deleted_review is None:
            raise ValueError(f"Review with id {review_id} not found.")
    return deleted_review


# Reports
def create_report(connection, user_id, listing_id, report_reason):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO reports (user_id, listing_id, report_reason)
                VALUES (%s, %s, %s)
                RETURNING *;
                """,
                (user_id, listing_id, report_reason)
            )
            new_report = cursor.fetchone()
    return new_report


def get_all_reports(connection):
    """ Returns all reports """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT * 
                FROM reports 
                ORDER BY created_at DESC;
                """
            )
            all_reports = cursor.fetchall()
    return all_reports


def get_report_by_id(connection, report_id):
    """ Returns a report with a specific id """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM reports 
                WHERE id = %s;
                """,
                (report_id,)
            )
            report_by_id = cursor.fetchone()
        if report_by_id is None:
            raise ValueError(f"Report with id {report_id} not found.")
    return report_by_id


def get_reports_for_listing(connection, listing_id):
    """ Returns all the reports for a listing """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM reports 
                WHERE listing_id = %s 
                ORDER BY created_at DESC;
                """,
                (listing_id,)
            )
            reports_for_listing = cursor.fetchall()
    return reports_for_listing


def delete_report(connection, report_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                DELETE 
                FROM reports 
                WHERE id = %s 
                RETURNING id;
                """,
                (report_id,)
            )
            deleted_report = cursor.fetchone()
    if deleted_report is None:
        raise ValueError(f"Report with id {report_id} not found.")
    return deleted_report


# Images
def create_image(connection, user_id, listing_id, image_url):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO images (user_id, listing_id, image_url)
                VALUES (%s, %s, %s)
                RETURNING *;
                """,
                (user_id, listing_id, image_url)
            )
            new_image = cursor.fetchone()
    return new_image


def get_all_images(connection):
    """ Returns all images """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM images 
                ORDER BY created_at DESC;
                """
            )
            all_images = cursor.fetchall()
    return all_images


def get_image_by_id(connection, image_id):
    """ Returns an image with a specific id """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM images 
                WHERE id = %s;
                """,
                (image_id,)
            )
            image_by_id = cursor.fetchone()
    if image_by_id is None:
        raise ValueError(f"Image with id {image_id} not found.")
    return image_by_id


def get_images_for_listing(connection, listing_id):
    """ Returns all the images for a listing """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM images 
                WHERE listing_id = %s 
                ORDER BY created_at ASC
                """,
                (listing_id,)
            )
            images_for_listing = cursor.fetchall()
    return images_for_listing


def delete_image(connection, image_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                DELETE 
                FROM images 
                WHERE id = %s 
                RETURNING id;
                """,
                (image_id,)
            )
            deleted_image = cursor.fetchone()
    if deleted_image is None:
        raise ValueError(f"Image with id {image_id} not found.")
    return deleted_image


# Transactions
def create_transaction(connection, user_id, listing_id, amount, status, bid_id=None):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO transactions (user_id, listing_id, amount, status, bid_id) 
                VALUES (%s, %s, %s, %s, %s) 
                RETURNING id;
                """,
                (user_id, listing_id, amount, status, bid_id),
            )
            transaction_id = cursor.fetchone()["id"]
        return transaction_id


def get_transaction_by_id(connection, transaction_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
            SELECT * FROM transactions 
            WHERE id = %s""",
                (transaction_id,),
            )
            transaction_by_id = cursor.fetchone()
        return transaction_by_id


def get_transactions_by_user_id(connection, user_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
            SELECT id, user_id, bid_id, listing_id, status, amount
            FROM transactions 
            WHERE user_id = %s""",
                (user_id,),
            )
            transaction_by_user_id = cursor.fetchall()
        return transaction_by_user_id


def get_all_transactions(connection):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM transactions")
            all_transactions = cursor.fetchall()
        return all_transactions


# Update transaction for transaction status (eg. from pending to cancelled or completed)
def update_transaction(connection, transaction_id, new_status):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE transactions 
                SET status = COALESCE (%s, status)
                WHERE id = %s RETURNING *;
                """,
                (new_status, transaction_id),
            )
            updated_transaction = cursor.fetchone()
        return updated_transaction


# Shipping_details
def create_shipping_details(
    connection,
    user_id,
    listing_id,
    shipping_method,
    shipping_cost,
    estimated_delivery_days=None,
    tracking_number=None,
    status=None,
    shipped_at=None,
):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO shipping_details (user_id, listing_id, shipping_method, shipping_cost, estimated_delivery_days, tracking_number, status, shipped_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;""",
                (
                    user_id,
                    listing_id,
                    shipping_method,
                    shipping_cost,
                    estimated_delivery_days,
                    tracking_number,
                    status,
                    shipped_at,
                ),
            )
            shipping_id = cursor.fetchone()["id"]
        return shipping_id


def get_shipping_by_listing_id(connection, listing_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
            SELECT id, listing_id, shipping_method, shipping_cost, estimated_delivery_days, tracking_number, status, shipped_at
            FROM shipping_details 
            WHERE listing_id = %s""",
                (listing_id,),
            )
            shipping_by_listing_id = cursor.fetchone()
        return shipping_by_listing_id


def update_shipping_tracking(
    connection, tracking_number, shipping_id, status, shipped_at=None
):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE shipping_details 
                SET tracking_number = COALESCE (%s, tracking_number),
                shipped_at = COALESCE (%s, shipped_at),
                status = COALESCE (%s, status)
                WHERE id = %s RETURNING *;
                """,
                (tracking_number, shipped_at, status, shipping_id),
            )
            updated_shipping = cursor.fetchone()
        return updated_shipping


# Notifications
def create_notification(
    connection, user_id, listing_id, notification_type, notification_message
):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO notifications (user_id, listing_id, notification_type, notification_message) 
                VALUES (%s, %s, %s, %s)
                RETURNING id;""",
                (user_id, listing_id, notification_type, notification_message),
            )
            notification_id = cursor.fetchone()["id"]
        return notification_id


def get_notifications_by_user_id(connection, user_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
            SELECT *
            FROM notifications
            WHERE user_id = %s""",
                (user_id,),
            )
            notifications_by_user_id = cursor.fetchall()
        return notifications_by_user_id


def get_unread_notifications(connection, user_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
            SELECT * FROM notifications
            WHERE user_id = %s AND is_read = FALSE""",
                (user_id,),
            )
            unread_notifications = cursor.fetchall()
        return unread_notifications


def mark_all_notifications_as_read(connection, user_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE notifications
                SET is_read = TRUE 
                WHERE user_id = %s RETURNING *;
                """,
                (user_id,),
            )
            mark_notifications_read = cursor.fetchall()
        return mark_notifications_read


def delete_notification(connection, notification_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM notifications WHERE id = %s RETURNING *;",
                (notification_id,),
            )
            deleted_notification = cursor.fetchone()
            return deleted_notification


# Listing_comments
def create_listing_comment(connection, user_id, listing_id, comment_text):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO listing_comments (user_id, listing_id, comment_text) 
                VALUES (%s, %s, %s)
                RETURNING id;""",
                (user_id, listing_id, comment_text),
            )
            listing_comment_id = cursor.fetchone()["id"]
        return listing_comment_id


def get_comments_by_listing_id(connection, listing_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
            SELECT id, user_id, listing_id, comment_text, answer_text
            FROM listing_comments
            WHERE listing_id = %s""",
                (listing_id,),
            )
            comments_by_listing_id = cursor.fetchall()
        return comments_by_listing_id


def get_comments_by_user_id(connection, user_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
            SELECT * FROM listing_comments
            WHERE user_id = %s""",
                (user_id,),
            )
            comments_by_user_id = cursor.fetchall()
        return comments_by_user_id


def answer_comment(connection, answer_text, comment_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE listing_comments 
                SET answer_text = %s, answered_at = CURRENT_TIMESTAMP
                WHERE id = %s RETURNING *;
                """,
                (answer_text, comment_id),
            )
            answered_comment = cursor.fetchone()
        return answered_comment


def delete_listing_comment(connection, comment_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM listing_comments WHERE id = %s RETURNING *;", (comment_id,)
            )
            deleted_listing_comment = cursor.fetchone()
            return deleted_listing_comment
