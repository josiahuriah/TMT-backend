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
        self.from_email = os.getenv('FROM_EMAIL', f'bookings@{self.domain}')
        self.admin_email = os.getenv('ADMIN_EMAIL', 'info@tmtsbahamas.com')
        
        if not self.api_key or not self.domain:
            logger.warning("Mailgun not configured properly. Email sending will be disabled.")
    
    def send_email(self, to_email, subject, html_content, text_content=None, bcc=None):
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
            
        if bcc:
            data["bcc"] = bcc
        
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
        """Send booking confirmation email with receipt"""
        
        # Calculate rental details
        total_price = float(reservation_data.get('total_price', 0))
        start_date = reservation_data.get('start_date', '')
        end_date = reservation_data.get('end_date', '')
        
        # Parse dates for better formatting
        try:
            from datetime import datetime
            start_dt = datetime.strptime(start_date, '%B %d, %Y')
            end_dt = datetime.strptime(end_date, '%B %d, %Y')
            rental_days = (end_dt - start_dt).days
        except:
            rental_days = 0
        
        # Generate booking reference number
        booking_ref = f"TMT-{datetime.now().strftime('%Y%m%d')}-{reservation_data.get('id', '000')}"
        
        # Create HTML email content with receipt styling
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ 
                    font-family: 'Arial', sans-serif; 
                    max-width: 600px; 
                    margin: 0 auto; 
                    background-color: #f5f5f5;
                }}
                .email-container {{
                    background-color: white;
                    margin: 20px auto;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .header {{ 
                    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                    color: white; 
                    padding: 30px; 
                    text-align: center; 
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                }}
                .header p {{
                    margin: 10px 0 0;
                    font-size: 16px;
                    opacity: 0.9;
                }}
                .content {{ 
                    padding: 30px; 
                }}
                .receipt-box {{
                    background: #f9f9f9;
                    border: 2px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 20px;
                    margin: 20px 0;
                }}
                .receipt-header {{
                    text-align: center;
                    border-bottom: 2px dashed #ccc;
                    padding-bottom: 15px;
                    margin-bottom: 20px;
                }}
                .booking-ref {{
                    font-size: 20px;
                    font-weight: bold;
                    color: #2c3e50;
                }}
                .detail-row {{
                    display: flex;
                    justify-content: space-between;
                    padding: 8px 0;
                    border-bottom: 1px solid #eee;
                }}
                .detail-label {{
                    font-weight: 600;
                    color: #555;
                }}
                .detail-value {{
                    text-align: right;
                    color: #333;
                }}
                .total-row {{
                    display: flex;
                    justify-content: space-between;
                    padding: 15px 0 10px;
                    font-size: 20px;
                    font-weight: bold;
                    color: #2c3e50;
                    border-top: 2px solid #333;
                    margin-top: 10px;
                }}
                .info-section {{
                    background: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .info-section h3 {{
                    margin-top: 0;
                    color: #856404;
                }}
                .info-section ul {{
                    margin: 10px 0;
                    padding-left: 20px;
                }}
                .footer {{ 
                    background-color: #2c3e50; 
                    color: white;
                    padding: 20px; 
                    text-align: center; 
                    font-size: 12px; 
                }}
                .footer a {{
                    color: #3498db;
                    text-decoration: none;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 30px;
                    background: #3498db;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h1>🌴 TMT's Coconut Cruisers</h1>
                    <p>Booking Confirmation & Receipt</p>
                </div>
                
                <div class="content">
                    <p style="font-size: 16px;">Dear <strong>{reservation_data.get('firstname', '')} {reservation_data.get('lastname', '')}</strong>,</p>
                    
                    <p>Thank you for choosing TMT's Coconut Cruisers! Your booking has been confirmed and your payment has been processed successfully.</p>
                    
                    <div class="receipt-box">
                        <div class="receipt-header">
                            <div class="booking-ref">Booking Reference</div>
                            <div style="font-size: 24px; color: #3498db; margin-top: 5px;">{booking_ref}</div>
                        </div>
                        
                        <h3 style="color: #2c3e50; margin-bottom: 15px;">📋 Rental Details</h3>
                        
                        <div class="detail-row">
                            <span class="detail-label">Customer Name:</span>
                            <span class="detail-value">{reservation_data.get('firstname', '')} {reservation_data.get('lastname', '')}</span>
                        </div>
                        
                        <div class="detail-row">
                            <span class="detail-label">Email:</span>
                            <span class="detail-value">{reservation_data.get('email', '')}</span>
                        </div>
                        
                        <div class="detail-row">
                            <span class="detail-label">Phone:</span>
                            <span class="detail-value">{reservation_data.get('cell', '')}</span>
                        </div>
                        
                        <div class="detail-row">
                            <span class="detail-label">Vehicle:</span>
                            <span class="detail-value"><strong>{car_data.get('name', 'N/A')}</strong></span>
                        </div>
                        
                        <div class="detail-row">
                            <span class="detail-label">Category:</span>
                            <span class="detail-value">{car_data.get('category', 'N/A')}</span>
                        </div>
                        
                        <div class="detail-row">
                            <span class="detail-label">Pickup Date:</span>
                            <span class="detail-value">{start_date}</span>
                        </div>
                        
                        <div class="detail-row">
                            <span class="detail-label">Return Date:</span>
                            <span class="detail-value">{end_date}</span>
                        </div>
                        
                        <div class="detail-row">
                            <span class="detail-label">Rental Duration:</span>
                            <span class="detail-value">{rental_days} days</span>
                        </div>
                        
                        <div class="detail-row">
                            <span class="detail-label">Daily Rate:</span>
                            <span class="detail-value">${car_data.get('price_per_day', 0):.2f}</span>
                        </div>
                        
                        <div class="total-row">
                            <span>TOTAL PAID:</span>
                            <span>${total_price:.2f} USD</span>
                        </div>
                    </div>
                    
                    <div class="info-section">
                        <h3>📍 Important Information</h3>
                        <ul>
                            <li><strong>Pickup Location:</strong> Deadman's Cay, Bahamas</li>
                            <li><strong>Required at Pickup:</strong> Valid driver's license & $100 security deposit</li>
                            <li><strong>Additional Fee:</strong> $10 for pickup/drop-off beyond Deadman's Cay</li>
                            <li><strong>Pickup Time:</strong> 8:00 AM - 6:00 PM</li>
                        </ul>
                    </div>
                    
                    <div style="background: #d4edda; border-left: 4px solid #28a745; padding: 15px; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #155724;">✅ What's Next?</h3>
                        <ol style="margin: 10px 0; padding-left: 20px;">
                            <li>Save this email for your records</li>
                            <li>Bring your driver's license and this confirmation to pickup</li>
                            <li>Prepare $100 cash for the security deposit</li>
                            <li>Contact us if you need to make any changes</li>
                        </ol>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <h3>Need Help?</h3>
                        <p>Our team is here to assist you!</p>
                        <p>
                            📧 <a href="mailto:info@tmtsbahamas.com">info@tmtsbahamas.com</a><br>
                            📞 +1 (242) 472-0016 or +1 (242) 367-0942
                        </p>
                    </div>
                </div>
                
                <div class="footer">
                    <p><strong>TMT's Coconut Cruisers</strong></p>
                    <p>Deadman's Cay, Long Island, Bahamas</p>
                    <p style="margin-top: 15px;">
                        This is an automated confirmation email. Please do not reply directly to this email.<br>
                        For assistance, contact us at <a href="mailto:info@tmtsbahamas.com">info@tmtsbahamas.com</a>
                    </p>
                    <p style="margin-top: 15px; font-size: 10px; opacity: 0.7;">
                        © {datetime.now().year} TMT's Coconut Cruisers. All rights reserved.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create text version
        text_content = f"""
        TMT's Coconut Cruisers - Booking Confirmation & Receipt
        ========================================================
        
        Booking Reference: {booking_ref}
        
        Dear {reservation_data.get('firstname', '')} {reservation_data.get('lastname', '')},
        
        Thank you for choosing TMT's Coconut Cruisers! Your booking has been confirmed.
        
        RENTAL DETAILS
        --------------
        Customer: {reservation_data.get('firstname', '')} {reservation_data.get('lastname', '')}
        Email: {reservation_data.get('email', '')}
        Phone: {reservation_data.get('cell', '')}
        
        Vehicle: {car_data.get('name', 'N/A')} ({car_data.get('category', 'N/A')})
        Pickup Date: {start_date}
        Return Date: {end_date}
        Rental Duration: {rental_days} days
        Daily Rate: ${car_data.get('price_per_day', 0):.2f}
        
        TOTAL PAID: ${total_price:.2f} USD
        
        IMPORTANT INFORMATION
        --------------------
        - Pickup Location: Deadman's Cay, Bahamas
        - Required at Pickup: Valid driver's license & $100 security deposit
        - Additional Fee: $10 for pickup/drop-off beyond Deadman's Cay
        - Pickup Time: 8:00 AM - 6:00 PM
        
        CONTACT US
        ----------
        Email: info@tmtsbahamas.com
        Phone: +1 (242) 472-0016 or +1 (242) 367-0942
        
        Thank you for your business!
        
        TMT's Coconut Cruisers Team
        """
        
        subject = f"Booking Confirmation #{booking_ref} - TMT's Coconut Cruisers"
        
        # Send email to customer and BCC to admin
        return self.send_email(
            to_email=reservation_data.get('email'),
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            bcc=self.admin_email  # Send copy to admin
        )

# Create a global instance
email_service = EmailService()