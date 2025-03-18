from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app():
    load_dotenv()
    app = Flask(__name__)



db = SQLAlchemy()  # Initialize db without app (bound later)
jwt = JWTManager()
migrate = Migrate()

def create_app():
    load_dotenv()  # Load .env variables
    app = Flask(__name__)
    logger.debug(f"Current directory: {os.getcwd()}")
    instance_dir = os.path.join(os.path.dirname(__file__), "instance")
    os.makedirs(instance_dir, exist_ok=True)
    db_path = os.path.join(instance_dir, "cars.db")
    logger.debug(f"Database path: {db_path}")
    CORS(app, origins=["http://localhost:5001"])  # Update to frontend URL later

    # Configure the app
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", f"sqlite:///{db_path}")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dijah_bei")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions with the app
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Import and register models (optional, can be imported elsewhere)
    from models import Car, User  # Explicit imports

    # Define a basic route
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({"message": "Car Rental Backend running"}), 200

    # Register routes dynamically
    from routes import get_cars, add_car, reserve_car
    app.route("/cars", methods=["GET"])(get_cars)
    app.route("/cars", methods=["POST"])(add_car)
    app.route("/cars/reserve", methods=["POST"])(reserve_car)

    return app