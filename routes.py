from flask import request, jsonify
from create_app import db
from models import Car, User
from datetime import datetime


def get_cars():
    cars = Car.query.all()
    return jsonify([{"id": car.id, 
                     "name": car.name, 
                     "category": car.category, 
                     "price_per_day": car.price_per_day, 
                     "quantity": car.quantity} for car in cars])

def add_car():
    data = request.json
    car = Car(
        name=data["name"],
        model=data["model"],
        category=data["category"],
        price_per_day=data["price_per_day"],
        quantity=data.get("quantity", 1)  # Default to 1 if not provided
    )
    db.session.add(car)
    db.session.commit()
    return jsonify({"message": "Car added"}), 201

def reserve_car():
    data = request.json
    car_id = data.get("car_id")
    car = Car.query.get(car_id)
    if not car or car.quantity <= 0:
        return jsonify({"error": "Car not available"}), 400
    car.quantity -= 1
    db.session.commit()
    return jsonify({"message": f"Reserved {car.name}, {car.quantity} remaining"}), 200

def process_payment():
    data = request.json
    car_id = data.get("car_id")
    category = data.get("category")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    card_number = data.get("card_number")
    expiry = data.get("expiry")
    cvc = data.get("cvc")
    total_price = data.get("total_price")

    car = Car.query.get(car_id)
    if not car or not car.available: # Double-check availability (should be reserved already)
        return jsonify({"success": False, "error": "Car not available"}), 400

    # Mock payment validation (replace with real payment gateway later)
    if len(card_number) < 16 or len(cvc) < 3 or "/" not in expiry:
        return jsonify({"success": False, "error": "Invalid payment details"}), 400

    try:
        # Car is already reserved by /cars/reserve, so just confirm payment
        return jsonify({
            "success": True,
            "message": f"Payment of ${total_price} processed for {category} (Car ID: {car_id})",
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500