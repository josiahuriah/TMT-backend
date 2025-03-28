from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CarCategory(db.Model):
    __tablename__ = "car_categories"  # Match the database table name
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255))
    description = db.Column(db.Text)
    rate = db.Column(db.Float)

class Car(db.Model):
    __tablename__ = "cars"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(50))
    category = db.Column(db.String(50), nullable=False)
    price_per_day = db.Column(db.Float)
    quantity = db.Column(db.Integer, default=1)