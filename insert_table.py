import sqlite3

conn = sqlite3.connect("pinoy_cuisine.db")
cur = conn.cursor()

# Insert dishes
dishes = [
    ("Adobo", "Main Course", "Stewing"),
    ("Afritada", "Main Course", "Simmering"),
    ("Pancit", "Noodle", "Sautéing")
]
cur.executemany("INSERT INTO dishes (name, classification, methodology) VALUES (?, ?, ?)", dishes)

# Get dish IDs
cur.execute("SELECT id, name FROM dishes")
dish_ids = {name.lower(): id for id, name in cur.fetchall()}

# Grouped data like your JSON
ingredient_data = {
    "adobo": {
        "meat": ["chicken", "pork"],
        "vegetables": ["garlic"]
    },
    "afritada": {
        "meat": ["chicken", "pork"],
        "vegetables": ["garlic", "onion", "bell peppers"]
    },
    "pancit": {
        "meat": ["chicken", "pork", "crab", "mussels"],
        "vegetables": ["garlic", "onion", "bell peppers", "cabbage", "string beans"]
    }
}

# Insert ingredients
for dish_name, types in ingredient_data.items():
    dish_id = dish_ids[dish_name]
    for ingredient_type, items in types.items():
        for name in items:
            cur.execute("INSERT INTO ingredients (dish_id, name, type) VALUES (?, ?, ?)",
                        (dish_id, name, 'meat' if ingredient_type == 'meat' else 'vegetable'))

conn.commit()
conn.close()
print("✅ Data inserted successfully.")
