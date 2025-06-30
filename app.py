from flask import Flask, jsonify, render_template
from flask_flatpages import FlatPages
from routes import routes  
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

# Register Blueprint for API routes
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)
