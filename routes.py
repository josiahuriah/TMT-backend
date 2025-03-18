from flask import request, jsonify
from app import app, db
from models import Car, User

# Define category limits
CAR_LIMITS = {
    "Economy": 7,
    "Van": 4,
    "Full-Size Sedan": 2,
    "SUV": 8,
    "Luxury": 3
}

@app.route("/cars", methods=["GET"])
def get_cars():
    cars = Car.query.all()
    # Group cars by category and filter by availability
    result = []
    for car in cars:
        category_count = Car.query.filter_by(category=car.category, available=True).count()
        if category_count <= CAR_LIMITS.get(car.category, 0):
            result.append({
                "id": car.id,
                "name": car.name,
                "model": car.model,
                "category": car.category,
                "price_per_day": car.price_per_day,
                "available": car.available
            })
    return jsonify(result)

@app.route("/cars", methods=["POST"])
def add_car():
    data = request.json
    category = data["category"]
    
    # Check if adding a car exceeds the limit
    current_count = Car.query.filter_by(category=category).count()
    if current_count >= CAR_LIMITS.get(category, 0):
        return jsonify({"error": f"Limit of {category} cars reached"}), 400
    
    new_car = Car(
        name=data["name"],
        model=data["model"],
        category=category,
        price_per_day=data["price_per_day"],
        available=True
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify({"message": "Car added successfully"}), 201

@app.route("/cars/reserve", methods=["POST"])
def reserve_car():
    data = request.json
    car_id = data.get("car_id")
    car = Car.query.get(car_id)
    
    if not car or not car.available:
        return jsonify({"error": "Car not available"}), 400
    
    car.available = False
    db.session.commit()
    return jsonify({"message": "Car reserved successfully"}), 200