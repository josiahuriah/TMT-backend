# test_hostinger_email.py
import os
from dotenv import load_dotenv
load_dotenv()

from email_service import email_service
from datetime import datetime, timedelta

# Test data
test_reservation = {
    'id': '123',
    'firstname': 'Test',
    'lastname': 'User',
    'email': 'josh.duncanson@gmail.com',  # Your email for testing
    'cell': '242-555-1234',
    'start_date': datetime.now().strftime('%B %d, %Y'),
    'end_date': (datetime.now() + timedelta(days=5)).strftime('%B %d, %Y'),
    'total_price': 350.00
}

test_car = {
    'name': 'Ford Focus',
    'category': 'Economy',
    'price_per_day': 70.00
}

print(f"SMTP Server: {os.getenv('SMTP_SERVER')}")
print(f"SMTP Username: {os.getenv('SMTP_USERNAME')}")
print(f"Credentials configured: {bool(os.getenv('SMTP_PASSWORD'))}")

# Send test email
success = email_service.send_booking_confirmation(test_reservation, test_car)
print(f"Email sent: {success}")