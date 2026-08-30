import sqlite3


DATABASE_NAME = "data/products.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)
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
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    """)

    connection.commit()
    connection.close()


def save_product(name, url, target_price):
    connection = sqlite3.connect(DATABASE_NAME)
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

    return product[0]


def save_price(product_id, price):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO price_history
        (product_id, price)
        VALUES (?, ?)
    """, (product_id, price))

    connection.commit()
    connection.close()


def get_products():
    connection = sqlite3.connect(DATABASE_NAME)
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


def get_latest_price(product_id):
    connection = sqlite3.connect(DATABASE_NAME)
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


def set_alert_sent(product_id, value):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE products
        SET alert_sent = ?
        WHERE id = ?
    """, (value, product_id))

    connection.commit()
    connection.close()


def get_price_history(product_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT price, recorded_at
        FROM price_history
        WHERE product_id = ?
        ORDER BY recorded_at ASC
    """, (product_id,))

    history = cursor.fetchall()

    connection.close()

    return history


if __name__ == "__main__":
    create_database()
    print("Database created successfully!")