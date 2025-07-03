from sqlite3 import connect

CUISINE_DB = "pinoy_cuisine.db"

# CREATE TABLES
def create_tables():
    """Create the necessary tables for the Pinoy Cuisine database."""
    conn = connect(CUISINE_DB)
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
    conn = connect(CUISINE_DB)
    cur = conn.cursor()

    # Insert dishes
    cur.execute("""INSERT INTO dishes (name, classification, methodology, 
            origin, taste_profile, description) VALUES (?, ?, ?, ?, ?, ?)""",
            ("Adobo", "Main Dish", "Stewing", "N/A","Sour", 
             "Stewed meat marinated in vinegar, soy sauce, and garlic."))
    
    latest_id = cur.lastrowid
    cur.execute(""" INSERT INTO ingredients (dish_id, name, type) 
            VALUES (?, ?, ?)""", (latest_id, "pork", "meat"))
    cur.execute(""" INSERT INTO ingredients (dish_id, name, type) 
            VALUES (?, ?, ?)""", (latest_id, "garlic", "vegetable"))
    
    conn.commit()
    conn.close()

    print("✅ Default data inserted successfully.")

def add_dish(name, classification, methodology, origin, taste,
        description, ingredients):
    """ Insert a new dish object to the database """
    conn = connect(CUISINE_DB)
    cur = conn.cursor()
    cur.execute("""INSERT INTO dishes (name, classification, methodology, 
            origin, taste_profile, description) VALUES (?, ?, ?, ?, ?, ?)""", 
            (name, classification, methodology, origin, taste, description))
    new_dish_id = cur.lastrowid
    
    if (new_dish_id == 0):
        return new_dish_id

    # Insert the ingredients associated to the dish
    for meat_value in ingredients['meat']:
        cur.execute("""INSERT INTO ingredients (dish_id, name, type) VALUES 
                (?, ?, 'meat')""", (new_dish_id, meat_value))
    for veggie_value in ingredients['vegetable']:
        cur.execute("""INSERT INTO ingredients (dish_id, name, type) VALUES 
                (?, ?, 'vegetable')""", (new_dish_id, veggie_value))
        
    conn.commit()
    conn.close()
    return new_dish_id

def search_dish(id):
    """ Search for a dish using the ID and return formatted dictionary """
    conn = connect(CUISINE_DB)
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

    dict_results = find_ingredients(ingredients, id, dict_results)

    return dict_results

def search_ingredient(search_ingredient):
    """ Search for dishes that contain a specific ingredient """
    conn = connect(CUISINE_DB)
    cur = conn.cursor()
    query = "SELECT dish_id FROM ingredients WHERE name = LOWER(?)"
    search_results = cur.execute(query, (search_ingredient,)).fetchall()
    conn.close()

    return search_results

def update_dish(dish_id, name, classification, methodology, origin, taste_profile, description, ingredients):
    """ Update a dish details by its ID """
    conn = connect(CUISINE_DB)
    cur = conn.cursor()

    # check if dish exists
    cur.execute("SELECT id FROM dishes WHERE id = ?", (dish_id,))
    dish = cur.fetchone()

    if not dish:
        conn.close()
        return {'error': 'Dish not found'}

    # update dish info
    cur.execute(""" UPDATE dishes SET name = ?, classification = ?, 
            methodology = ?, origin = ?, taste_profile = ?, description = ? 
            WHERE id = ?""", (name, classification, methodology, origin, 
            taste_profile, description, dish_id,))

    # Delete old ingredients
    cur.execute("DELETE FROM ingredients WHERE dish_id = ?", (dish_id,))

    # Insert new ingredients
    for meat in ingredients.get("meat", []):
        cur.execute("""INSERT INTO ingredients (dish_id, name, type) 
                VALUES (?, ?, 'meat')""", (dish_id, meat))

    for veggie in ingredients.get("vegetable", []):
        cur.execute("""INSERT INTO ingredients (dish_id, name, type) 
                VALUES (?, ?, 'vegetable')""",(dish_id, veggie))

    conn.commit()
    conn.close()

    return {'message': f'Dish with ID {dish_id} updated successfully.'}


def view_all_records():
    """ Returns all available dishes including the ingredients """
    conn = connect(CUISINE_DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM dishes")
    dishes = cur.fetchall()

    cur.execute("SELECT * FROM ingredients")
    ingredients = cur.fetchall()
    conn.close()

    results = []

    # Iterate over available dishes and format each into a dictionary
    for dish in dishes:
        dish_id = dish[0]

        dish_dict = {
            "name": dish[1],
            "classification": dish[2],
            "methodology": dish[3],
            "origin": dish[4],
            "taste_profile": dish[5],
            "description": dish[6],
            "ingredients": {
                "meat": [],
                "vegetable": []
            }
        }

        dish_dict = find_ingredients(ingredients, dish_id, dish_dict)
        results.append(dish_dict)

    return results

def find_ingredients(ingredients, dish_id, dish_dict):
    """ Helper function to search ingredients related to a dish """
    for ingredient in ingredients:
        if ingredient[1] == dish_id:
            if ingredient[3] == "meat":
                dish_dict["ingredients"]["meat"].append(ingredient[2])
            elif ingredient[3] == "vegetable":
                dish_dict["ingredients"]["vegetable"].append(ingredient[2])

    return dish_dict