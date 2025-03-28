# routes.py (assumed)
from flask import Blueprint, jsonify
from models import Car, CarCategory
from create_app import db

bp = Blueprint("routes", __name__)

@bp.route("/car-categories", methods=["GET"])
def get_car_categories():
    categories = CarCategory.query.all()
    return jsonify([{
        "id": c.id,
        "title": c.title,
        "image": c.image,
        "description": c.description,
        "rate": float(c.rate)
    } for c in categories])

@bp.route("/cars", methods=["GET"])
def get_cars():
    cars = Car.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "model": c.model,
        "category": c.category,
        "price_per_day": float(c.price_per_day),
        "quantity": c.quantity
    } for c in cars])

@bp.route("/cars/reserve", methods=["POST"])
def reserve_car():
    data = request.get_json()
    car_id = data.get("car_id")
    car = Car.query.get(car_id)
    if car and car.quantity > 0:
        car.quantity -= 1
        db.session.commit()
        return jsonify({"message": "Car reserved"}), 200
    return jsonify({"error": "Car not available"}), 400