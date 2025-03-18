#!/usr/bin/python3
import os
import sqlite3
from hbnb.app import create_app, db



def execute_script(db_path, script_path):
    """Executes a SQL script file against the SQLite database."""
    try:
        with sqlite3.connect(db_path) as conn:
            with open(script_path, 'r') as script:
                conn.executescript(script.read())
        print(f"Successfully executed: {script_path}")
    except Exception as e:
        print(f"Error executing script {script_path}: {e}")


def initialize_database():
    """Initializes the SQLite database by running schema and seed scripts."""
    base_dir = os.path.dirname(__file__)
    db_path = "/Users/priscilalopez/holbertonschool-hbnb/instance/development.db"
    scripts_path = os.path.join(base_dir, "hbnb/app/persistence", "scripts.sql")
    seed_path = os.path.join(base_dir, "hbnb/app/persistence", "seed.sql")

    # Check if the database directory exists
    if not os.path.exists(os.path.join(base_dir, "hbnb/app/persistence")):
        print("Error: The 'database' folder does not exist.")
        return

    # Execute schema and seed scripts
    print("Initializing database...")
    execute_script(db_path, scripts_path)
    execute_script(db_path, seed_path)
    print("Database initialization complete.")


app = create_app()

# Run database initialization within the app context
with app.app_context():
    # db.drop_all()
    initialize_database()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
