from flask import Flask, jsonify, render_template
from flask_flatpages import FlatPages
import sqlite3
from models import CUISINE_DB, search_dish

app = Flask(__name__)
app.config.update(
    FLATPAGES_EXTENSION='.md',
    FLATPAGES_ROOT='templates',
    FLATPAGES_AUTO_RELOAD=True
)
documentation = FlatPages(app)

def get_db_connection():
    conn = sqlite3.connect(CUISINE_DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    global documentation
    return render_template("index.html", pages=documentation)

# Main GET route: List all dishes
@app.route('/dishes', methods=['GET'])
def get_dishes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM dishes")
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# GET route for a specific dish by title (dynamic routing)
@app.route('/dishes/<string:dish_name>', methods=['GET'])
def get_dish_by_title(dish_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM dishes WHERE LOWER(name) = LOWER(?)", (dish_name,))
    dish = cur.fetchone()
    if not dish:
        conn.close()
        return jsonify({'error': 'Dish not found'}), 404
    result = search_dish(dish['id'])
    conn.close()
    return jsonify(result)

# DELETE route: Delete a dish by name
@app.route('/dishes/<string:dish_name>', methods=['DELETE'])
def delete_dish(dish_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM dishes WHERE LOWER(name) = LOWER(?)", (dish_name,))
    dish = cur.fetchone()
    if not dish:
        conn.close()
        return jsonify({'error': 'Dish not found'}), 404
    cur.execute("DELETE FROM ingredients WHERE dish_id = ?", (dish['id'],))
    cur.execute("DELETE FROM dishes WHERE id = ?", (dish['id'],))
    conn.commit()
    conn.close()
    return jsonify({'message': f'Dish "{dish_name}" deleted successfully.'})

if __name__ == "__main__":
    app.run(debug=True)