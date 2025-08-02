import os
import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.api_key = os.getenv('MAILGUN_API_KEY')
        self.domain = os.getenv('MAILGUN_DOMAIN')
        self.base_url = os.getenv('MAILGUN_BASE_URL', 'https://api.mailgun.net/v3')
        self.from_email = os.getenv('FROM_EMAIL', f'noreply@{self.domain}')
        
        if not self.api_key or not self.domain:
            logger.warning("Mailgun not configured properly. Email sending will be disabled.")
    
    def send_email(self, to_email, subject, html_content, text_content=None):
        """Send an email using Mailgun API"""
        if not self.api_key or not self.domain:
            logger.error("Mailgun not configured. Cannot send email.")
            return False
        
        url = f"{self.base_url}/{self.domain}/messages"
        
        data = {
            "from": f"TMT Coconut Cruisers <{self.from_email}>",
            "to": to_email,
            "subject": subject,
            "html": html_content,
        }
        
        if text_content:
            data["text"] = text_content
        
        try:
            response = requests.post(
                url,
                auth=("api", self.api_key),
                data=data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def send_booking_confirmation(self, reservation_data, car_data):
        """Send booking confirmation email"""
        
        # Calculate total with formatting
        total_price = float(reservation_data.get('total_price', 0))
        
        # Create HTML email content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; }}
                .header {{ background-color: #333; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .booking-details {{ background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .footer {{ background-color: #f0f0f0; padding: 15px; text-align: center; font-size: 12px; }}
                .total {{ font-size: 18px; font-weight: bold; color: #333; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>TMT's Coconut Cruisers</h1>
                <h2>Booking Confirmation</h2>
            </div>
            
            <div class="content">
                <p>Dear {reservation_data.get('firstname', '')} {reservation_data.get('lastname', '')},</p>
                
                <p>Thank you for choosing TMT's Coconut Cruisers! Your booking has been confirmed.</p>
                
                <div class="booking-details">
                    <h3>Booking Details</h3>
                    <p><strong>Name:</strong> {reservation_data.get('firstname', '')} {reservation_data.get('lastname', '')}</p>
                    <p><strong>Email:</strong> {reservation_data.get('email', '')}</p>
                    <p><strong>Phone:</strong> {reservation_data.get('cell', '')}</p>
                    <p><strong>Vehicle:</strong> {car_data.get('name', 'N/A')} ({car_data.get('category', 'N/A')})</p>
                    <p><strong>Pickup Date:</strong> {reservation_data.get('start_date', '')}</p>
                    <p><strong>Return Date:</strong> {reservation_data.get('end_date', '')}</p>
                    <p class="total"><strong>Total Price:</strong> ${total_price:.2f}</p>
                </div>
                
                <h3>Important Information</h3>
                <ul>
                    <li>Please bring a valid driver's license for pickup</li>
                    <li>A $100 security deposit is required at pickup</li>
                    <li>Pickup location: Deadman's Cay, Bahamas</li>
                    <li>$10 fee applies for pickup/drop-off beyond Deadman's Cay</li>
                </ul>
                
                <h3>Contact Information</h3>
                <p>If you have any questions, please contact us:</p>
                <p>📧 Email: info@tmtsbahamas.com</p>
                <p>📞 Phone: +1 (242) 472-0016 or +1 (242) 367-0942</p>
                
                <p>We look forward to serving you!</p>
                <p>Best regards,<br>TMT's Coconut Cruisers Team</p>
            </div>
            
            <div class="footer">
                <p>This is an automated confirmation email. Please do not reply to this email.</p>
                <p>TMT's Coconut Cruisers | Deadman's Cay, Bahamas</p>
            </div>
        </body>
        </html>
        """
        
        # Create text version for email clients that don't support HTML
        text_content = f"""
        TMT's Coconut Cruisers - Booking Confirmation
        
        Dear {reservation_data.get('firstname', '')} {reservation_data.get('lastname', '')},
        
        Thank you for choosing TMT's Coconut Cruisers! Your booking has been confirmed.
        
        Booking Details:
        - Name: {reservation_data.get('firstname', '')} {reservation_data.get('lastname', '')}
        - Email: {reservation_data.get('email', '')}
        - Phone: {reservation_data.get('cell', '')}
        - Vehicle: {car_data.get('name', 'N/A')} ({car_data.get('category', 'N/A')})
        - Pickup Date: {reservation_data.get('start_date', '')}
        - Return Date: {reservation_data.get('end_date', '')}
        - Total Price: ${total_price:.2f}
        
        Important Information:
        - Please bring a valid driver's license for pickup
        - A $100 security deposit is required at pickup
        - Pickup location: Deadman's Cay, Bahamas
        - $10 fee applies for pickup/drop-off beyond Deadman's Cay
        
        Contact Information:
        Email: info@tmtsbahamas.com
        Phone: +1 (242) 472-0016 or +1 (242) 367-0942
        
        We look forward to serving you!
        
        Best regards,
        TMT's Coconut Cruisers Team
        """
        
        subject = f"Booking Confirmation - TMT's Coconut Cruisers"
        
        return self.send_email(
            to_email=reservation_data.get('email'),
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

# Create a global instance
email_service = EmailService()