import sqlite3

DB_NAME = "pinoy_cuisine.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

# CREATE TABLES
def create_tables():
    """Create the necessary tables for the Pinoy Cuisine database."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS dishes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        classification TEXT NOT NULL,
        methodology TEXT NOT NULL,
        origin TEXT,
        taste_profile TEXT,
        description TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dish_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        type TEXT CHECK(type IN ('meat', 'vegetable')) NOT NULL,
        FOREIGN KEY (dish_id) REFERENCES dishes(id)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Tables created successfully.")

def insert_default_data():
    """Insert default data into the dishes and ingredients tables."""
    conn = get_connection()
    cur = conn.cursor()

    # Insert dishes
    # dict_results

    # Dishes data

    conn.commit()
    conn.close()
    print("✅ Default data inserted successfully.")
