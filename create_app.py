# create_app.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Single SQLAlchemy instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Use Render's DATABASE_URL with correct format
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)  # Bind db to the app

    from routes import bp
    app.register_blueprint(bp)

    return app