import os
import time
from sqlalchemy import exc, text
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate  # <-- Import here

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app, 
         origins=["https://tmt-rental-frontend.onrender.com"],
         supports_credentials=True,
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"],
         expose_headers=["Content-Range"])

    uri = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    for _ in range(3):  # Retry 3 times
        try:
            db.init_app(app)
            with app.app_context():
                db.session.execute(text("SELECT 1"))  # Test connection
            break
        except exc.OperationalError as e:
            print(f"Database connection failed: {e}. Retrying...")
            time.sleep(2)  # Wait before retrying
    else:
        raise Exception("Failed to connect to database after retries")

    from routes import bp
    app.register_blueprint(bp)

    # Initialize Flask-Migrate with the app and db
    migrate = Migrate(app, db)

    return app
