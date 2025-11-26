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
    this way we'll start a new connection each time
    someone hits one of our endpoints, which isn't great for performance
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
    Creates database tables for the tradera application.
    Can be run multiple times due to IF NOT EXISTS clauses.
    """
    connection = get_connection()
    cursor = connection.cursor()

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

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "bids" (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            --listing_id BIGINT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            bid_amount DECIMAL(10,2) NOT NULL
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "transaction" (
            id BIGSERIAL PRIMARY KEY NOT NULL,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            bid_id BIGINT REFERENCES "bids"(id),
            --listing_id BIGINT NOT NULL REFERENCES "listings"(id),
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(50) NOT NULL,
            amount DECIMAL(10,2) NOT NULL
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "images" (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            --listing_id BIGINT NOT NULL,
            image_url VARCHAR(500) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "user_ratings" (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            total_ratings INT NOT NULL DEFAULT 0,
            average_rating DECIMAL(3,2) NOT NULL DEFAULT 0.00
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "reviews" (
            id BIGSERIAL PRIMARY KEY,
            reviewer_id BIGINT NOT NULL,
            reviewed_user_id BIGINT NOT NULL,
            --listing_id BIGINT,
            rating INT NOT NULL,
            review_text TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "notifications" (
            id BIGSERIAL PRIMARY KEY NOT NULL,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            --listing_id BIGINT NOT NULL REFERENCES "listings"(id),
            notification_type VARCHAR(50) NOT NULL,
            notification_message TEXT NOT NULL,
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP NOT NULL
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "reports" (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            --listing_id BIGINT NOT NULL,
            report_reason TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "listing_comments" (
            id BIGSERIAL PRIMARY KEY NOT NULL,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            --listing_id BIGINT NOT NULL REFERENCES "listings"(id),
            comment_text TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            answer_text TEXT,
            answered_at TIMESTAMP
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "shipping_details" (
            id BIGSERIAL PRIMARY KEY NOT NULL,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            --listing_id BIGINT NOT NULL REFERENCES "listings"(id),
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
