from flask import Flask
import os
from . import routes

import sqlite3

DATABASE = 'employee.db'

def init_db():
    """Create or initialize the database outside of a request."""
    with sqlite3.connect(DATABASE) as conn:
        print("Opened a temporary, standalone database connection.")
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS employee (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, role TEXT, UNIQUE(name, age, role))"
            )
        print("Closed the temporary database connection.")

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret_key'

    # Database path — relative to project root
    app.config['DATABASE'] = os.path.join(os.getcwd(), DATABASE)

    # Register the blueprint from routes.py
    app.register_blueprint(routes.bp)
    
    init_db()

    return app
