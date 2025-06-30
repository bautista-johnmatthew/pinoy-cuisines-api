import sqlite3

CUISINE_DB = "pinoy_cuisine.db"

# CREATE TABLES
def create_tables():
    """Create the necessary tables for the Pinoy Cuisine database."""
    conn = sqlite3.connect(CUISINE_DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS dishes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        classification TEXT NOT NULL,
        methodology TEXT NOT NULL,
        origin TEXT,
        taste_profile TEXT NOT NULL,
        description TEXT NOT NULL
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
    conn = sqlite3.connect(CUISINE_DB)
    cur = conn.cursor()

    # Insert dishes
    # dict_results

    # Dishes data

    conn.commit()
    conn.close()

    print("✅ Default data inserted successfully.")

def search_dish(id):
    """ Search for a dish using the ID and return formatted dictionary """
    conn = sqlite3.connect(CUISINE_DB)
    cur = conn.cursor()
    results = cur.execute("SELECT * FROM dishes WHERE id = ?", 
            (id,)).fetchone()
    ingredients = cur.execute("SELECT * FROM ingredients WHERE dish_id = ?", 
            (id,)).fetchall()

    dict_results = {
    "name" : results[1],
    "classification" : results[2],
    "methodology" : results[3],
    "origin" : results[4],
    "taste_profile" : results[5],
    "description" : results[6],
    "ingredients" : {
            "meat": [],
            "vegetable": []
        }
    }

    for ingredient in ingredients:
        if ingredient[3] == "meat":
            dict_results["ingredients"]["meat"].append(ingredient[2])
        elif ingredient[3] == "vegetable":
            dict_results["ingredients"]["vegetable"].append(ingredient[2])

    return dict_results

