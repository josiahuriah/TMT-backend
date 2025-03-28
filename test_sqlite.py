import sqlite3
import os

db_path = "/Users/jduncanson/Documents/TMT_Rental/server/instance/cars.db"
print(f"Attempting to connect to: {db_path}")

# Ensure directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Test SQLite connection
try:
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY)")
    conn.close()
    print("SQLite connection successful, database created!")
except sqlite3.OperationalError as e:
    print(f"SQLite error: {e}")