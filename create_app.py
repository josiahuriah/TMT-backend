from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
import os
from dotenv import load_dotenv
import sqlite3
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


db = SQLAlchemy()  # Initialize db without app (bound later)
jwt = JWTManager()
migrate = Migrate()

def create_app():
    load_dotenv()  # Load .env variables
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:5173", "https://tmt-rental-frontend.onrender.com"])  # Update to frontend URL later

    db_uri = os.getenv("DATABASE_URL", "sqlite:///instance/cars.db")
    if db_uri.startswith("postgres://"):
        db_uri = db_uri.replace("postgres://", "postgresql://", 1)

    # logger.debug(f"Current directory: {os.getcwd()}")
    # instance_dir = os.path.join(os.path.dirname(__file__), "instance")
    # os.makedirs(instance_dir, exist_ok=True)
    # db_path = os.path.join(instance_dir, "cars.db")
    # logger.debug(f"Database path: {db_path}")

    # Configure the app
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL', 'sqlite:////Users/jduncanson/Documents/TMT_Rental/server/instance/cars.db')
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dijah_bei")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions with the app
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Import and register models (optional, can be imported elsewhere)
    from models import Car, User  # Explicit imports
    from models import Car, User, CarCategory

    # Define a basic route
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({"message": "Car Rental Backend running"}), 200

    # Register routes dynamically
    from routes import get_cars, add_car, reserve_car
    app.route("/cars", methods=["GET"])(get_cars)
    app.route("/cars", methods=["POST"])(add_car)
    app.route("/cars/reserve", methods=["POST"])(reserve_car)

    from routes import get_cars, add_car, reserve_car, process_payment
    app.route("/cars", methods=["GET"])(get_cars)
    app.route("/cars", methods=["POST"])(add_car)
    app.route("/cars/reserve", methods=["POST"])(reserve_car)
    app.route("/process-payment", methods=["POST"])(process_payment)

    @app.route("/car-categories", methods=["GET"])
    def get_car_categories():
        try:
            categories = CarCategory.query.all()
            return jsonify([{
                "id": category.id,
                "title": category.title,  # Match SmallCarCards field names
                "description": category.description,
                "image": category.image,
                "rate": category.rate
            } for category in categories]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app