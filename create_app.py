import os
import time
from sqlalchemy import exc, text
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate 

from extensions import db
from models import Reservation, Car, CarCategory
from routes import bp

 
def create_app():
    app = Flask(__name__)

    # Handle database URL properly for both development and production
    database_url = os.getenv("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback-secret-key")

    db.init_app(app)
    Migrate(app, db)

    # CORS configuration for production
    cors_origins = [
        "https://tmt-rental-frontend.onrender.com",
        "http://localhost:3000",  # For local development
        "http://localhost:5173"   # For Vite dev server
    ]
    
    # If in development, allow all origins
    if os.getenv("FLASK_ENV") == "development":
        cors_origins = "*"

    CORS(app, 
         origins=cors_origins,
         supports_credentials=True,
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "Range"],
         expose_headers=["Content-Range"])

    # Database connection retry logic (uncomment for production)
    for _ in range(3):  # Retry 3 times
        try:
            with app.app_context():
                db.session.execute(text("SELECT 1"))  # Test connection
            break
        except exc.OperationalError as e:
            print(f"Database connection failed: {e}. Retrying...")
            time.sleep(2)  # Wait before retrying
    else:
        print("Warning: Failed to connect to database after retries")

    from routes import bp
    app.register_blueprint(bp)

    return app