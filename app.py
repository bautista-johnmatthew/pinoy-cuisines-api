from flask import Flask, jsonify, render_template
from flask_flatpages import FlatPages
import sqlite3

app = Flask(__name__)
app.config.update(
    FLATPAGES_EXTENSION='.md',
    FLATPAGES_ROOT='templates',
    FLATPAGES_AUTO_RELOAD=True
)
documentation = FlatPages(app)

# TODO: Remove this type of implementation and focus database on models.py
DB = "pinoy_cuisine.db"

def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    global documentation
    return render_template("index.html", pages=documentation)

# GET /dishes → list all dishes
@app.route("/dishes", methods=["GET"])
def get_dishes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, classification, methodology FROM dishes")
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# GET /dishes/<dish_name> → get grouped ingredients for a specific dish
@app.route("/dishes/<dish_name>", methods=["GET"])
def get_dish_details(dish_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM dishes WHERE LOWER(name) = LOWER(?)", (dish_name,))
    dish = cur.fetchone()

    if not dish:
        return jsonify({"error": "Dish not found"}), 404

    cur.execute("SELECT name, type FROM ingredients WHERE dish_id = ?", (dish["id"],))
    ingredients = cur.fetchall()
    conn.close()

    grouped = {}
    for ing in ingredients:
        grouped.setdefault(ing["type"], []).append(ing["name"])

    return jsonify({dish_name.lower(): grouped})

if __name__ == "__main__":
    app.run(debug=True)
