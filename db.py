import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException

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

# Users
def create_user(connection, username, email, password, user_since, date_of_birth, phone_number):
    # open connection
    with connection:
        # create cursor
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO users (username, email, password, user_since, date_of_birth, phone_number) 
                VALUES (%s, %s, %s, %s, %s, %s) 
                RETURNING id;""",
                (username, email, password, user_since, date_of_birth, phone_number),
            )
            # get id from dictionary
            user_id = cursor.fetchone()["id"]
        return user_id


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
            cursor.execute("SELECT * FROM users")
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
            update_user = cursor.fetchone()
        return update_user


def delete_user(connection, user_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s RETURNING *;", (user_id,))
            deleted_user = cursor.fetchone()
            return deleted_user


# Categories
def get_all_categories(connection):
    with connection:
        # Creates a cursor to run SQL commands
        # RealDictCursor turns the results into dictionarys (easier to read)
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM categories;
                """
            )  # Run SQL ("Fetch everything from the table categories")
            all_categories = (
            cursor.fetchall()
            )  # Fetch all the results and saves it in the varible categories
        return all_categories  # Returns the result


def get_category_by_id(connection, category_id):
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

        if not category_by_id:
            raise HTTPException(status_code=404, detail=f"Category with id {category_id} does not exist.")
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
    status,
    description,
    image_url=None,
):
    """ Creates a new listing in the database """
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO listings 
                (user_id, category_id, title, listing_type, price, region, status, description, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
                RETURNING *;
                """,
                # Run SQL ("Insert a new listing with these values")
                # RETURNING *: return the new row that was created
                # %s: placeholder for each value
                (
                    user_id,
                    category_id,
                    title,
                    listing_type,
                    price,
                    region,
                    status,
                    description,
                    image_url,
                ),  # Sending all the values
            )
            new_listing = cursor.fetchone()  # Fetch only one result (the first one)
        return new_listing


def get_all_listings(connection):
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


def get_listing_by_id(connection, listing_id):  # Parameter: listing_id
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
            listing_by_id = cursor.fetchone()  # Fetch only one result (the first one)

    if not listing_by_id:
        raise HTTPException(status_code=404, detail=f"Listing with id {listing_id} does not exist.")
    return listing_by_id


def update_listing(
    connection,
    listing_id,
    category_id=None,
    title=None,
    listing_type=None,
    price=None,
    region=None,
    status=None,
    description=None,
    image_url=None,
):
    """ Updates an existing listing with the values that the user choose """
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
                status = COALESCE(%s, status),
                description = COALESCE(%s, description),
                image_url = COALESCE(%s, image_url)
                WHERE id = %s 
                RETURNING *;
                """,
                (
                    listing_id,
                    category_id,
                    title,
                    listing_type,
                    price,
                    region,
                    status,
                    description,
                    image_url,
                ),
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

        if not delete_listing:
            raise HTTPException(status_code=404, detail=f"Listing with id {listing_id} not found.")
    return deleted_listing


def search_listings(connection, search_term):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM listings 
                WHERE title ILIKE %s OR description ILIKE %s;
                """,
                (f"%{search_term}%", f"%{search_term}%")
            )
            searched_listings = cursor.fetchall()
    return searched_listings


def get_listings_by_category(connection, category_id):
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
def get_all_watched_listings(connection, user_id):
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
    """ Fetches all messages for a specific user """
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
            all_messages = cursor.fetchall()
        return all_messages


def get_message_by_id(connection, message_id):
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

        if not message_by_id:
            raise HTTPException(status_code=404, detail=f"Message with id {message_id} does not exist.")
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

        if not delete_message:
            raise HTTPException(status_code=404, detail=f"Message with id {message_id} not found.")
    return deleted_message


# Payments
def create_payment(
        connection, 
        transaction_id, 
        listing_id, 
        payment_method, 
        payment_status, 
        amount):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO payments 
                (transaction_id, listing_id, payment_method, payment_status, amount) 
                VALUES (%s, %s, %s, %s, %s) 
                RETURNING *;
                """,
                (transaction_id, listing_id, payment_method, payment_status, amount)
            )
            new_payment = cursor.fetchone()
    return new_payment


def get_all_payments(connection):
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

            if not payment_by_id:
                raise HTTPException(status_code=404, detail=f"Payment with id {payment_id} not found.")
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
                ('refund_requested', payment_id)
            )
            refund_request = cursor.fetchone()
    return refund_request


# Bids
def create_bid(connection, user_id, listing_id, bid_amount):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO bids (user_id, listing_id, bid_amount)
                VALUES (%s, %s, %s)
                RETURNING *; 
                """,
                (user_id, listing_id, bid_amount)
            )
            new_bid = cursor.fetchone()
    return new_bid


def get_all_bids(connection):
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

    if not bid_by_id:
        raise HTTPException(status_code=404, detail=f"Bid with id {bid_id} not found.")
    return bid_by_id


def get_bids_for_listing(connection, listing_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM bids 
                WHERE listing_id = %s 
                ORDER BY bid_amount DESC;
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

    if not deleted_bid:
        raise HTTPException(status_code=404, detail=f"Bid with id {bid_id} not found.")
    return delete_bid


# User Ratings
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

    if not rating_by_user_id:
        raise HTTPException(status_code=404, detail=f"Rating for user {user_id} not found.")
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

    if not updated_rating:
        raise HTTPException(status_code=404, detail=f"Rating for user {user_id} not found.")
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

    if not deleted_rating:
        raise HTTPException(status_code=404, detail=f"Rating for user {user_id} not found.")
    return deleted_rating


# Reviews
def create_review(
    connection, reviewer_id, reviewed_user_id, listing_id, rating, review_text=None):
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

    if not review_by_id:
        raise HTTPException(status_code=404, detail=f"Review with id {review_id} not found.")
    return review_by_id


def get_reviews_for_user(connection, user_id):
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

        if not deleted_review:
            raise HTTPException(status_code=404, detail=f"Review with id {review_id} not found.")
    return deleted_review


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
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM images 
                ORDER BY created_at DESC;
                """
            )
            images = cursor.fetchall()
    return images


def get_image_by_id(connection, image_id):
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

    if not image_by_id:
        raise HTTPException(status_code=404, detail=f"Image with id {image_id} not found.")
    return image_by_id


def get_images_for_listing(connection, listing_id):
    """ Gets all the images for a listing """
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

    if not deleted_image:
        raise HTTPException(status_code=404, detail=f"Image with id {image_id} not found.")
    return delete_image


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
                (user_id, listing_id, report_reason),
            )
            new_report = cursor.fetchone()
    return new_report


def get_all_reports(connection):
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

    if not report_by_id:
        raise HTTPException(status_code=404, detail=f"Report with id {report_id} not found.")
    return report_by_id


def get_reports_for_listing(connection, listing_id):
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
            report_for_listing = cursor.fetchall()
    return report_for_listing


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

    if not deleted_report:
        raise HTTPException(status_code=404, detail=f"Report with id {report_id} not found.")
    return deleted_report


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
            notifications_by_username = cursor.fetchall()
        return notifications_by_username


def get_unread_notifications(connection, user_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
            SELECT * FROM notifications
            WHERE user_id = %s AND is_read = FALSE""",
                (user_id,),
            )
            notifications_by_username = cursor.fetchall()
        return notifications_by_username


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
            get_comments_by_listing_id = cursor.fetchall()
        return get_comments_by_listing_id


def get_comments_by_user_id(connection, user_id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
            SELECT * FROM listing_comments
            WHERE user_id = %s""",
                (user_id,),
            )
            get_comments_by_user_id = cursor.fetchall()
        return get_comments_by_user_id


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
            deleted_listing_comments = cursor.fetchone()
            return deleted_listing_comments