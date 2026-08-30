import sqlite3
from pathlib import Path


# ==========================================
# DATABASE PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATABASE_NAME = DATA_DIR / "products.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():
    return sqlite3.connect(str(DATABASE_NAME))


# ==========================================
# CREATE DATABASE
# ==========================================

def create_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            target_price REAL NOT NULL,
            alert_sent INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            price REAL NOT NULL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id)
                REFERENCES products (id)
        )
    """)

    connection.commit()
    connection.close()


# ==========================================
# SAVE PRODUCT
# ==========================================

def save_product(name, url, target_price):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO products
        (name, url, target_price)
        VALUES (?, ?, ?)
    """, (name, url, target_price))

    connection.commit()

    cursor.execute("""
        SELECT id
        FROM products
        WHERE url = ?
    """, (url,))

    product = cursor.fetchone()

    connection.close()

    if product:
        return product[0]

    return None


# ==========================================
# SAVE PRICE
# ==========================================

def save_price(product_id, price):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO price_history
        (product_id, price)
        VALUES (?, ?)
    """, (product_id, price))

    connection.commit()
    connection.close()


# ==========================================
# GET PRODUCTS
# ==========================================

def get_products():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            url,
            target_price,
            alert_sent,
            created_at
        FROM products
        ORDER BY id DESC
    """)

    products = cursor.fetchall()

    connection.close()

    return products


# ==========================================
# GET LATEST PRICE
# ==========================================

def get_latest_price(product_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT price
        FROM price_history
        WHERE product_id = ?
        ORDER BY recorded_at DESC
        LIMIT 1
    """, (product_id,))

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return None


# ==========================================
# SET ALERT
# ==========================================

def set_alert_sent(product_id, value):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE products
        SET alert_sent = ?
        WHERE id = ?
    """, (value, product_id))

    connection.commit()
    connection.close()


# ==========================================
# PRICE HISTORY
# ==========================================

def get_price_history(product_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            price,
            recorded_at
        FROM price_history
        WHERE product_id = ?
        ORDER BY recorded_at ASC
    """, (product_id,))

    history = cursor.fetchall()

    connection.close()

    return history


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    create_database()

    print("Database created successfully!")

    print(f"Database location: {DATABASE_NAME}")