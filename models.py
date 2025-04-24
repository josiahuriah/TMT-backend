from extensions import db
from datetime import datetime

class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    home = db.Column(db.String(20))
    cell = db.Column(db.String(20))
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    car = db.relationship("Car")

class CarCategory(db.Model):
    __tablename__ = "car_categories"
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