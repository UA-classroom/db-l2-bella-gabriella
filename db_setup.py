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

    # Users
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

    # Categories
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "categories" (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL
        );
    """
    )

    # Listings
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "listings" (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            category_id BIGINT NOT NULL REFERENCES "categories"(id),
            title VARCHAR(100) NOT NULL,
            image_url VARCHAR(500),
            listing_type VARCHAR(255) NOT NULL CHECK (listing_type IN ('buying', 'selling', 'free')),
            price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            region VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL CHECK (status IN ('active', 'sold', 'closed')),
            description TEXT NOT NULL
        );
    """
    )

    # Listings_watch_list
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "listings_watch_list" (
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            listing_id BIGINT NOT NULL REFERENCES "listings"(id),
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, listing_id) -- Composite key --
        );
    """
    )

    # Messages
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

    # Transactions
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

    # Payments
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "payments" (
            id BIGSERIAL PRIMARY KEY,
            transaction_id BIGINT NOT NULL REFERENCES "transactions"(id), 
            listing_id BIGINT NOT NULL REFERENCES "listings"(id),     
            payment_method VARCHAR(50) NOT NULL,
            payment_status VARCHAR(50) NOT NULL CHECK (payment_status IN ('pending', 'completed', 'failed', 'cancelled', 'refunded', 'refund_requested')),
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

    # User_ratings
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

    # Notifications
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "notifications" (
            id BIGSERIAL PRIMARY KEY NOT NULL,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            listing_id BIGINT NOT NULL REFERENCES "listings"(id),
            notification_type VARCHAR(50) NOT NULL,
            notification_message TEXT NOT NULL,
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
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

    # Listing_comments
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "listing_comments" (
            id BIGSERIAL PRIMARY KEY NOT NULL,
            user_id BIGINT NOT NULL REFERENCES "users"(id),
            listing_id BIGINT NOT NULL REFERENCES "listings"(id),
            comment_text TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            answer_text TEXT,
            answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    # Shipping_details
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
            status VARCHAR(50),
            shipped_at TIMESTAMP
        );
    """
    )

# Some inserts for test data
# Users
    cursor.execute(
        """
        INSERT INTO users (username, email, password, date_of_birth, phone_number) VALUES 
            ('anna_svensson', 'anna@example.com', 'hashed_password_123', '1995-05-15', '0701234567'),
            ('erik_karlsson', 'erik@example.com', 'hashed_password_456', '1990-08-22', '0709876543'),
            ('sara_nilsson', 'sara@example.com', 'hashed_password_789', '1998-12-03', '0731122334')
        ON CONFLICT DO NOTHING;
        """
    )

# Categories
    cursor.execute(
        """
        INSERT INTO categories (name) VALUES 
            ('Elektronik'),
            ('Möbler'),
            ('Kläder')
        ON CONFLICT DO NOTHING;
        """
    )

# Listings
    cursor.execute(
        """
        INSERT INTO listings (user_id, category_id, title, listing_type, price, region, status, description, image_url) VALUES 
            (1, 1, 'iPhone 13 Pro', 'selling', 7000.00, 'Stockholm', 'active', 'Mycket bra skick, använd i 1 år', 'https://example.com/iphone.jpg'),
            (2, 2, 'IKEA Säng', 'selling', 1500.00, 'Göteborg', 'active', 'Dubbelsäng i bra skick', 'https://example.com/bed.jpg'),
            (3, 1, 'Laptop HP', 'selling', 4500.00, 'Malmö', 'active', 'Bärbar dator perfekt för studier', NULL)
        ON CONFLICT DO NOTHING;
        """
    )

# Listings_watch_list
    cursor.execute(
        """
        INSERT INTO listings_watch_list (user_id, listing_id) VALUES 
            (2, 1),
            (3, 1),
            (1, 3)
        ON CONFLICT DO NOTHING;
        """
    )

# Messages
    cursor.execute(
        """
        INSERT INTO messages (sender_id, recipient_id, listing_id, message_text) VALUES 
            (2, 1, 1, 'Hej! Är iPhone fortfarande tillgänglig?'),
            (1, 2, 1, 'Ja, den är kvar! Vill du komma och titta?'),
            (3, 2, 2, 'Kan du skicka sängen till Malmö?')
        ON CONFLICT DO NOTHING;
        """
    )

# Bids
    cursor.execute(
        """
        INSERT INTO bids (user_id, listing_id, amount) VALUES 
            (2, 1, 6500.00),
            (3, 1, 6800.00),
            (1, 3, 4200.00)
        ON CONFLICT DO NOTHING;
        """
    )

# Transactions
    cursor.execute(
        """
        INSERT INTO transactions (user_id, listing_id, status, amount, bid_id) VALUES 
            (2, 1, 'completed', 7000.00, 1),
            (3, 2, 'pending', 1500.00, NULL),
            (1, 3, 'completed', 4500.00, 3)
        ON CONFLICT DO NOTHING;
        """
    )

# Payments
    cursor.execute(
        """
        INSERT INTO payments (transaction_id, listing_id, payment_method, payment_status, amount) VALUES 
            (1, 1, 'Swish', 'completed', 7000.00),
            (2, 2, 'Banköverföring', 'pending', 1500.00),
            (3, 3, 'Swish', 'completed', 4500.00)
        ON CONFLICT DO NOTHING;
        """
    )

# Images
    cursor.execute(
        """
        INSERT INTO images (user_id, listing_id, image_url) VALUES 
            (1, 1, 'https://example.com/iphone_front.jpg'),
            (1, 1, 'https://example.com/iphone_back.jpg'),
            (2, 2, 'https://example.com/bed_main.jpg')
        ON CONFLICT DO NOTHING;
        """
    )

# User_ratings
    cursor.execute(
        """
        INSERT INTO user_ratings (user_id, total_ratings, average_rating) VALUES 
            (1, 5, 4.80),
            (2, 3, 4.33),
            (3, 2, 5.00)
        ON CONFLICT DO NOTHING;
        """
    )

# Reviews
    cursor.execute(
        """
        INSERT INTO reviews (reviewer_id, reviewed_user_id, listing_id, rating, review_text) VALUES 
            (2, 1, 1, 5, 'Snabb leverans och bra kommunikation!'),
            (3, 2, 2, 4, 'Sängen var precis som beskrivet.'),
            (1, 3, 3, 5, 'Perfekt affär!')
        ON CONFLICT DO NOTHING;
        """
    )

# Notifications
    cursor.execute(
        """
        INSERT INTO notifications (user_id, listing_id, notification_type, notification_message) VALUES 
            (1, 1, 'new_bid', 'Nytt bud på din annons'),
            (2, 2, 'message', 'Du har fått ett nytt meddelande'),
            (3, 3, 'sale_completed', 'Din försäljning är slutförd')
        ON CONFLICT DO NOTHING;
        """
    )

# Reports
    cursor.execute(
        """
        INSERT INTO reports (user_id, listing_id, report_reason) VALUES 
            (2, 3, 'Misstänkt bedrägeri'),
            (3, 1, 'Felaktig produktbeskrivning')
            ON CONFLICT DO NOTHING;
        """
    )

# Listing_comments
    cursor.execute(
        """
        INSERT INTO listing_comments (user_id, listing_id, comment_text, answer_text) VALUES 
            (2, 1, 'Är skärmen repig?', 'Nej, den är i perfekt skick!'),
            (3, 2, 'Kan man få sängen monterad?', NULL),
            (1, 3, 'Hur gammal är laptopen?', 'Den är 2 år gammal')
        ON CONFLICT DO NOTHING;
        """
    )

# Shipping_details
    cursor.execute(
        """
        INSERT INTO shipping_details (user_id, listing_id, shipping_method, shipping_cost, estimated_delivery_days, tracking_number, status) VALUES 
            (2, 1, 'PostNord', 99.00, 3, 'PN123456789SE', 'shipped'),
            (3, 2, 'DHL', 149.00, 2, 'DHL987654321SE', 'pending'),
            (1, 3, 'Schenker', 199.00, 5, NULL, 'pending')
        ON CONFLICT DO NOTHING;
        """
    )

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
