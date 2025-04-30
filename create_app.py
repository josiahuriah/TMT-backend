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

db = SQLAlchemy()
 
def create_app():
    app = Flask(__name__)

    uri = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)

    CORS(app, 
         origins=["https://tmt-rental-frontend.onrender.com"],
         supports_credentials=True,
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "Range"],
         expose_headers=["Content-Range"])

    # for _ in range(3):  # Retry 3 times
    #     try:
    #         db.init_app(app)
    #         with app.app_context():
    #             db.session.execute(text("SELECT 1"))  # Test connection
    #         break
    #     except exc.OperationalError as e:
    #         print(f"Database connection failed: {e}. Retrying...")
    #         time.sleep(2)  # Wait before retrying
    # else:
    #     raise Exception("Failed to connect to database after retries")

    from routes import bp
    app.register_blueprint(bp)

    return app
