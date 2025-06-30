import sqlite3

conn = sqlite3.connect("pinoy_cuisine.db")
cur = conn.cursor()

# DISHES TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS dishes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    classification TEXT NOT NULL,
    methodology TEXT NOT NULL
)
""")

# INGREDIENTS TABLE
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
