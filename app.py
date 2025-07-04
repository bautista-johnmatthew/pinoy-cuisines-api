from flask import Flask, request, jsonify, render_template
from flask_flatpages import FlatPages
from sqlite3 import connect
from models import CUISINE_DB, search_dish, search_ingredient
from models import add_dish, update_dish, view_all_records

app = Flask(__name__)
app.config.update(
    FLATPAGES_EXTENSION='.md',
    FLATPAGES_ROOT='templates',
    FLATPAGES_AUTO_RELOAD=True
)
documentation = FlatPages(app)

@app.route("/")
def home():
    """ Default route that returns user manual """
    global documentation

    return render_template("index.html", pages=documentation)

# Main GET route: List all dishes
@app.route('/dishes', methods=['GET', 'POST' ])
def get_dishes():
    """ Returns all the dishes available in the database """
    if request.method == 'POST':
        json_request = request.json
        result_json = process_json(json_request)
        
        return jsonify(result_json)
    
    return jsonify(view_all_records())

def process_json(json_contents):
    """ Iterates over the json file and adds contents to the database. 
            Returns an array of the result messages """
    result_list = []

    for content in json_contents:
        result = add_dish(content['name'], content['classification'], 
                content['methodology'], content['origin'], 
                content['taste_profile'], content['description'], 
                content['ingredients'])
        
        if result == 0:
            result_list.append({'error', 'Dish cannot be added'})
        else:
            result_list.append({'message' : "Dish added successfully", 
                    'contents' : search_dish(result), 
                    'location' : f"dishes/{result}"})
            
    return result_list

# GET route for a specific dish by title (dynamic routing)
@app.route('/dishes/<string:dish_name>', methods=['GET'])
def get_dish_by_title(dish_name):
    """ Returns a specific dish by title (dynamic routing)"""
    conn = connect(CUISINE_DB)
    cur = conn.cursor()
    cur.execute("SELECT id FROM dishes WHERE LOWER(name) = LOWER(?)", 
            (dish_name))
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
    """ Returns a specific dish by the dish id """
    result = search_dish(dish_id)

    if not result:
        return jsonify({'error': 'Dish not found'}), 404
    
    return jsonify(result)

@app.route('/ingredients/<string:ingredient_name>', methods=['GET'])
def search_by_ingredient(ingredient_name):
    """ Returns all the dishes containing the given ingredient """
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

# PUT route: Update a dish ingredient by id
@app.route('/dishes/<int:dish_id>', methods=['PUT'])
def put_dish(dish_id):
    """ Updates a dish using the given dish id """
    dish_data = request.json
        
    if not dish_data:
        return jsonify({'error': 'No input provided'}), 400
    
    update_dish_details = ('name', 'classification', 'methodology', 'origin', 
            'taste_profile', 'description', 'ingredients')
    
    # check if all required fields are present
    for input in update_dish_details:
        if input not in dish_data:
            return jsonify({'error': f'Missing required field: {input}'}), 400
    
    new_details = update_dish(dish_id, 
            dish_data['name'], 
            dish_data['classification'], 
            dish_data['methodology'], 
            dish_data['origin'], 
            dish_data['taste_profile'], 
            dish_data['description'], 
            dish_data['ingredients']
    )

    if 'error' in new_details:
        return jsonify(new_details), 404
    
    return jsonify(new_details), 200

# DELETE route: Delete a dish by name
@app.route('/dishes/<string:dish_name>', methods=['DELETE'])
def delete_dish(dish_name):
    """ Deletes a dish based on the given dish name """
    conn = connect(CUISINE_DB)
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
    """ Deletes a dish based on the given dish id """
    conn = connect(CUISINE_DB)
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