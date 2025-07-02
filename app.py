from flask import Flask, jsonify, request, render_template
from flask_flatpages import FlatPages
import sqlite3
from models import CUISINE_DB, search_dish, view_all_records, search_ingredient, add_dish

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
@app.route('/dishes', methods=['GET', 'POST' ])
def get_dishes():
    if request.method == 'POST':
        content = request.json
        
        result = add_dish(content['name'], content['classification'], 
                content['methodology'], content['origin'], 
                content['taste_profile'], content['description'], 
                content['ingredients'])
        
        if result == 0:
            return jsonify({'error', 'Dish cannot be added'}), 500

        return jsonify({'message' : "Dish added successfully", 
                'contents' : search_dish(result), 
                'location' : f"dishes/{result}"}), 201
    
    return jsonify(view_all_records())

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

# GET route for a specific dish by ID (dynamic routing)
@app.route('/dishes/<int:dish_id>', methods=['GET'])
def get_dish_by_id(dish_id):
    result = search_dish(dish_id)
    if not result:
        return jsonify({'error': 'Dish not found'}), 404
    return jsonify(result)

@app.route('/ingredients/<string:ingredient_name>', methods=['GET'])
def search_by_ingredient(ingredient_name):
    # Find all dish_ids that use this ingredient
    dish_ids = search_ingredient(ingredient_name)
    if not dish_ids:
        return jsonify({'error': 'No dishes found with that ingredient'}), 404
    # Get full dish info for each dish_id
    results = []
    for row in dish_ids:
        dish_id = row[0]
        results.append(search_dish(dish_id))
    return jsonify(results)

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

# DELETE route: Delete a dish by ID
@app.route('/dishes/<int:dish_id>', methods=['DELETE'])
def delete_dish_by_id(dish_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM dishes WHERE id = ?", (dish_id,))
    dish = cur.fetchone()
    if not dish:
        conn.close()
        return jsonify({'error': 'Dish not found'}), 404
    cur.execute("DELETE FROM ingredients WHERE dish_id = ?", (dish['id'],))
    cur.execute("DELETE FROM dishes WHERE id = ?", (dish['id'],))
    conn.commit()
    conn.close()
    return jsonify({'message': f'Dish with ID {dish_id} deleted successfully.'})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)