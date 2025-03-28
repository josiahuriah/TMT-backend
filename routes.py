# routes.py
from flask import Blueprint, jsonify
from models import Car, CarCategory
from create_app import db

bp = Blueprint("routes", __name__)

@bp.route("/car-categories", methods=["GET"])
def get_car_categories():
    try:
        categories = CarCategory.query.all()
        return jsonify([{
            "id": c.id,
            "title": c.title,
            "image": c.image,
            "description": c.description,
            "rate": float(c.rate)
        } for c in categories])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/cars", methods=["GET"])
def get_cars():
    try:
        cars = Car.query.all()
        return jsonify([{
            "id": c.id,
            "name": c.name,
            "model": c.model,
            "category": c.category,
            "price_per_day": float(c.price_per_day),
            "quantity": c.quantity
        } for c in cars])
    except Exception as e:
        return jsonify({"error": str(e)}), 500