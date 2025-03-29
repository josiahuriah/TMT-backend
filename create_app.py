import os
import time  
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS  

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)  

    uri = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    for _ in range(3):  # Retry 3 times
        try:
            db.init_app(app)
            with app.app_context():
                db.session.execute("SELECT 1")  # Test connection
            break
        except exc.OperationalError as e:
            print(f"Database connection failed: {e}. Retrying...")
            time.sleep(2)  # Wait before retrying
    else:
        raise Exception("Failed to connect to database after retries")

    from routes import bp
    app.register_blueprint(bp)

    return app
