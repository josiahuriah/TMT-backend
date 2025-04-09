from flask import Blueprint, jsonify, request, make_response
from models import Reservation 
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
    
@bp.route("/reservations", methods=["POST"])
def create_reservation():
    data = request.get_json()

    car = Car.query.get(data['car_id'])
    if car.quantity <= 0:
        return jsonify({"error": "Car not available"}), 400

    reservation = Reservation(
        firstname=data['firstname'],
        lastname=data['lastname'],
        email=data['email'],
        home=data.get('home'),
        cell=data.get('cell'),
        car_id=car.id,
        start_date=data['start_date'],
        end_date=data['end_date'],
        total_price=data['total_price']
    )

    # Decrease car availability
    car.quantity -= 1

    db.session.add(reservation)
    db.session.commit()

    return jsonify({"message": "Reservation successful"}), 201
    
@bp.route("/reservations", methods=["GET"])
def get_reservations():
    # Query all reservations
    reservations = Reservation.query.all()
    reservation_list = [{
        "id": r.id,
        "firstname": r.firstname,
        "lastname": r.lastname,
        "email": r.email,
        "home": r.home,
        "cell": r.cell,
        "car_name": r.car.name,
        "start_date": r.start_date.isoformat(),
        "end_date": r.end_date.isoformat(),
        "total_price": r.total_price,
        "created_at": r.created_at.isoformat()
    } for r in reservations]

    # Create response object
    response = make_response(jsonify(reservation_list))

    # Add Content-Range header (example: reservations 0-9/10)
    total_count = len(reservation_list)
    response.headers['Content-Range'] = f"reservations 0-{total_count - 1}/{total_count}"
    
    # Expose the Content-Range header for React Admin
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'

    return response

@bp.route("/reservations/<int:id>", methods=["DELETE"])
def cancel_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    car = Car.query.get(reservation.car_id)
    car.quantity += 1  # Make car available again
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"message": "Reservation canceled"}), 200
