import os

import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE_NAME")
PASSWORD = os.getenv("PASSWORD")

def get_connection():
    """
    Function that returns a single connection
    In reality, we might use a connection pool, since
    This way we'll start a new connection each time
    Someone hits one of our endpoints, which isn't great for performance
    """
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user="postgres",
        password=PASSWORD,
        host="localhost",
        port="5432",
    )

def create_tables():
    """
    Creates database tables for the Tradera application
    Can be run multiple times due to IF NOT EXISTS clauses
    """
    connection = get_connection()
    cursor = connection.cursor()
    
    # Users - Gabriella
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "users" (
            id BIGSERIAL PRIMARY KEY NOT NULL,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            user_since TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            date_of_birth DATE NOT NULL,
            phone_number VARCHAR(20)
        );
    """
    )

    # Categories - Bella
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "categories" (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL
        );
    """
    )

    # Listings - Bella
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "listings" (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            category_id BIGINT NOT NULL REFERENCES "categories"(id),
            title VARCHAR(100) NOT NULL,
            image_url VARCHAR(500),
            listing_type VARCHAR(255) NOT NULL CHECK (listing_type IN ('buying', 'selling', 'free')),
            price DECIMAL(10, 2) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            region VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL CHECK (status IN ('active', 'sold', 'closed')),
            description TEXT NOT NULL
        );
    """
    )

    # Listings watch list - Bella
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "listings_watch_list" (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            listing_id BIGINT NOT NULL REFERENCES "listings"(id),
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    # Messages - Bella
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "messages" (
            id BIGSERIAL PRIMARY KEY,
            sender_id BIGINT NOT NULL REFERENCES "users"(id),
            recipient_id BIGINT NOT NULL REFERENCES "users"(id),
            listing_id BIGINT NOT NULL REFERENCES "listings"(id),
            message_text TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            is_read BOOLEAN DEFAULT FALSE
        );
    """
    )
    
    # Bids
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "bids" (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            listing_id BIGINT NOT NULL REFERENCES "listings"(id),
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            amount DECIMAL(10,2) NOT NULL
        );
    """
    )
    
    # Transactions - Gabriella
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "transactions" (
            id BIGSERIAL PRIMARY KEY NOT NULL,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            bid_id BIGINT REFERENCES "bids"(id),
            listing_id BIGINT NOT NULL REFERENCES "listings"(id),
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(50) NOT NULL,
            amount DECIMAL(10,2) NOT NULL
        );
    """
    )

    # Payments - Bella
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "payments" (
            id BIGSERIAL PRIMARY KEY,
            transaction_id BIGINT NOT NULL REFERENCES "transactions"(id), 
            listing_id BIGINT NOT NULL REFERENCES "listings"(id),     
            payment_method VARCHAR(50) NOT NULL,
            payment_status VARCHAR(50) NOT NULL CHECK (payment_status IN ('pending', 'completed', 'failed', 'cancelled', 'refunded')),
            amount DECIMAL(10, 2) NOT NULL,
            paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    # Images
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "images" (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            listing_id BIGINT NOT NULL REFERENCES "listings"(id), 
            image_url VARCHAR(500) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    # User ratings
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "user_ratings" (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            total_ratings INT NOT NULL DEFAULT 0,
            average_rating DECIMAL(3,2) NOT NULL DEFAULT 0.00
        );
    """
    )

    # Reviews
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "reviews" (
            id BIGSERIAL PRIMARY KEY,
            reviewer_id BIGINT NOT NULL REFERENCES "users"(id),
            reviewed_user_id BIGINT NOT NULL REFERENCES "users"(id),
            listing_id BIGINT NOT NULL REFERENCES "listings"(id),
            rating INT NOT NULL,
            review_text TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    # Notifications - Gabriella
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "notifications" (
            id BIGSERIAL PRIMARY KEY NOT NULL,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            listing_id BIGINT NOT NULL REFERENCES "listings"(id),
            notification_type VARCHAR(50) NOT NULL,
            notification_message TEXT NOT NULL,
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP NOT NULL
        );
    """
    )

    # Reports
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "reports" (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            listing_id BIGINT NOT NULL REFERENCES "listings"(id),
            report_reason TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    # Listing comments - Gabriella
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "listing_comments" (
            id BIGSERIAL PRIMARY KEY NOT NULL,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            listing_id BIGINT NOT NULL REFERENCES "listings"(id),
            comment_text TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            answer_text TEXT,
            answered_at TIMESTAMP
        );
    """
    )

    # Shipping details - Gabriella
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "shipping_details" (
            id BIGSERIAL PRIMARY KEY NOT NULL,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            listing_id BIGINT NOT NULL REFERENCES "listings"(id),
            shipping_method VARCHAR(100) NOT NULL,
            shipping_cost DECIMAL(10,2) NOT NULL,
            estimated_delivery_days INT,
            tracking_number VARCHAR(100),
            shipped_at TIMESTAMP
        );
    """
    )

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
