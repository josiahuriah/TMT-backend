from create_app import create_app, db
import os

# Ensure instance directory exists
instance_dir = "/Users/jduncanson/Documents/TMT_Rental/server/instance"
os.makedirs(instance_dir, exist_ok=True)

app = create_app()
with app.app_context():
    db.create_all()
    print("Database created successfully!")