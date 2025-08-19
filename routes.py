from flask import Blueprint, jsonify, request, make_response
from models import Reservation, Car, CarCategory
from extensions import db
from email_service import email_service
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint("routes", __name__)

@bp.errorhandler(Exception)
def handle_error(error):
    logger.error(f"Unhandled error: {error}")
    return jsonify({"error": "Internal server error"}), 500

@bp.route("/car-categories", methods=["GET", "OPTIONS"])
def get_car_categories():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
        return response
    
    try:
        categories = CarCategory.query.all()
        return jsonify([{
            "id": c.id,
            "title": c.title,
            "image": c.image,
            "description": c.description,
            "rate": float(c.rate) if c.rate else 0
        } for c in categories])
    except Exception as e:
        logger.error(f"Error fetching car categories: {e}")
        return jsonify({"error": "Failed to fetch car categories"}), 500

@bp.route("/cars", methods=["GET", "OPTIONS"])
def get_cars():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
        return response
    
    try:
        cars = Car.query.all()
        return jsonify([{
            "id": c.id,
            "name": c.name,
            "model": c.model,
            "category": c.category,
            "price_per_day": float(c.price_per_day) if c.price_per_day else 0,
            "quantity": c.quantity or 0
        } for c in cars])
    except Exception as e:
        logger.error(f"Error fetching cars: {e}")
        return jsonify({"error": "Failed to fetch cars"}), 500
    
@bp.route("/reservations", methods=["POST", "OPTIONS"])
def create_reservation():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response
    
    try:
        data = request.get_json()
        logger.info(f"Received reservation request: {data}")
        
        # Validate required fields
        required_fields = ['car_id', 'firstname', 'lastname', 'email', 'start_date', 'end_date', 'total_price']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        car = Car.query.get(data['car_id'])
        if not car:
            return jsonify({"error": "Car not found"}), 404
            
        if car.quantity <= 0:
            return jsonify({"error": "Car not available"}), 400

        # Parse dates
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        reservation = Reservation(
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            home=data.get('home'),
            cell=data.get('cell'),
            car_id=car.id,
            start_date=start_date,
            end_date=end_date,
            total_price=float(data['total_price'])
        )

        # Decrease car availability
        car.quantity -= 1

        db.session.add(reservation)
        db.session.flush()  # Get the ID before commit
        reservation_id = reservation.id
        db.session.commit()
        
        logger.info(f"Reservation created: {reservation_id} for {reservation.email}")
        
        # Send confirmation email
        email_sent = False
        try:
            car_data = {
                'name': car.name,
                'model': car.model,
                'category': car.category,
                'price_per_day': car.price_per_day
            }
            
            reservation_data = {
                'id': reservation_id,
                'firstname': reservation.firstname,
                'lastname': reservation.lastname,
                'email': reservation.email,
                'home': reservation.home,
                'cell': reservation.cell,
                'start_date': reservation.start_date.strftime('%B %d, %Y'),
                'end_date': reservation.end_date.strftime('%B %d, %Y'),
                'total_price': reservation.total_price
            }
            
            logger.info(f"Sending email to {reservation.email}")
            email_sent = email_service.send_booking_confirmation(reservation_data, car_data)
            
            if email_sent:
                logger.info(f"Confirmation email sent successfully to {reservation.email}")
            else:
                logger.warning(f"Failed to send confirmation email to {reservation.email}")
                
        except Exception as email_error:
            logger.error(f"Error sending confirmation email: {email_error}", exc_info=True)
            # Don't fail the reservation if email fails
        
        return jsonify({
            "message": "Reservation successful", 
            "reservation_id": reservation_id,
            "email_sent": email_sent
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating reservation: {e}", exc_info=True)
        return jsonify({"error": "Failed to create reservation"}), 500
    
@bp.route("/reservations", methods=["GET", "OPTIONS"])
def get_reservations():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Range")
        response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
        return response
    
    try:
        reservations = Reservation.query.all()
        reservation_list = [{
            "id": r.id,
            "firstname": r.firstname,
            "lastname": r.lastname,
            "email": r.email,
            "home": r.home,
            "cell": r.cell,
            "car_name": r.car.name if r.car else "Unknown",
            "start_date": r.start_date.isoformat(),
            "end_date": r.end_date.isoformat(),
            "total_price": r.total_price,
            "created_at": r.created_at.isoformat()
        } for r in reservations]

        response = make_response(jsonify(reservation_list))
        total_count = len(reservation_list)
        response.headers['Content-Range'] = f"reservations 0-{total_count - 1}/{total_count}"
        response.headers['Access-Control-Expose-Headers'] = 'Content-Range'

        return response
    except Exception as e:
        logger.error(f"Error fetching reservations: {e}")
        return jsonify({"error": "Failed to fetch reservations"}), 500

@bp.route("/reservations/<int:id>", methods=["DELETE", "OPTIONS"])
def cancel_reservation(id):
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "DELETE, OPTIONS")
        return response
    
    try:
        reservation = Reservation.query.get_or_404(id)
        car = Car.query.get(reservation.car_id)
        if car:
            car.quantity += 1  # Make car available again
        
        db.session.delete(reservation)
        db.session.commit()
        
        logger.info(f"Reservation {id} canceled")
        return jsonify({"message": "Reservation canceled"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error canceling reservation {id}: {e}")
        return jsonify({"error": "Failed to cancel reservation"}), 500

@bp.route("/contact", methods=["POST", "OPTIONS"])
def send_contact_message():
    """Handle contact form submissions"""
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response
    
    try:
        data = request.get_json()
        logger.info(f"Received contact form submission from {data.get('email')}")
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Send email to admin
        success = email_service.send_contact_form_message(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone', 'Not provided'),
            message=data.get('message')
        )
        
        if success:
            # Also send confirmation to the user
            email_service.send_contact_confirmation(
                to_email=data.get('email'),
                name=data.get('name')
            )
            
            logger.info(f"Contact form email sent successfully")
            return jsonify({
                "message": "Message sent successfully",
                "success": True
            }), 200
        else:
            logger.error("Failed to send contact form email")
            return jsonify({
                "error": "Failed to send message",
                "success": False
            }), 500
            
    except Exception as e:
        logger.error(f"Error processing contact form: {e}", exc_info=True)
        return jsonify({"error": "Failed to process contact form"}), 500

@bp.route("/admin/send-email", methods=["POST", "OPTIONS"])
def admin_send_email():
    """Allow admins to send emails from the platform"""
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['to', 'subject', 'message']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        success = email_service.send_admin_email(
            to_email=data.get('to'),
            subject=data.get('subject'),
            message=data.get('message'),
            is_html=data.get('is_html', False)
        )
        
        if success:
            return jsonify({
                "message": "Email sent successfully",
                "success": True
            }), 200
        else:
            return jsonify({
                "error": "Failed to send email",
                "success": False
            }), 500
            
    except Exception as e:
        logger.error(f"Error sending admin email: {e}")
        return jsonify({"error": "Failed to send email"}), 500

@bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Test database connection
        from sqlalchemy import text
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "unhealthy", "database": "disconnected"}), 503

@bp.route("/", methods=["GET"])
def home():
    return jsonify({"status": "TMT Rental API is live", "version": "1.0"}), 200