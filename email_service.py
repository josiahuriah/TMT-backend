import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.hostinger.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.from_email = os.getenv('FROM_EMAIL', 'help@tmtsbahamas.com')
        self.from_name = os.getenv('FROM_NAME', 'TMT Coconut Cruisers')
        self.admin_email = os.getenv('ADMIN_EMAIL', 'help@tmtsbahamas.com')
        
        logger.info(f"EmailService initialized with SMTP server: {self.smtp_server}")
        logger.info(f"From email: {self.from_email}")
        
        if not self.smtp_username or not self.smtp_password:
            logger.warning("SMTP credentials not configured. Email sending will be disabled.")
    
    def send_email(self, to_email, subject, html_content, text_content=None, cc=None, bcc=None):
        """Send an email using SMTP"""
        if not self.smtp_username or not self.smtp_password:
            logger.error("SMTP not configured. Cannot send email.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            if cc:
                msg['Cc'] = cc if isinstance(cc, str) else ', '.join(cc)
            
            # Add text and HTML parts
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Prepare recipient list
            recipients = [to_email]
            if cc:
                recipients.extend(cc if isinstance(cc, list) else [cc])
            if bcc:
                recipients.extend(bcc if isinstance(bcc, list) else [bcc])
            
            # Connect and send
            logger.info(f"Connecting to SMTP server {self.smtp_server}:{self.smtp_port}")
            
            if self.smtp_port == 465:
                # SSL connection
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            else:
                # TLS connection
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
            
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg, from_addr=self.from_email, to_addrs=recipients)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def send_booking_confirmation(self, reservation_data, car_data):
        """Send booking confirmation email with receipt"""
        
        logger.info(f"Preparing to send booking confirmation to {reservation_data.get('email')}")
        
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
        
        # Create HTML email content
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
                    
                    <p>Thank you for choosing TMT's Coconut Cruisers! Your booking has been confirmed.</p>
                    
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
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <h3>Need Help?</h3>
                        <p>Our team is here to assist you!</p>
                        <p>
                            📧 <a href="mailto:help@tmtsbahamas.com">help@tmtsbahamas.com</a><br>
                            📞 +1 (242) 472-0016 or +1 (242) 367-0942
                        </p>
                    </div>
                </div>
                
                <div class="footer">
                    <p><strong>TMT's Coconut Cruisers</strong></p>
                    <p>Deadman's Cay, Long Island, Bahamas</p>
                    <p style="margin-top: 15px;">
                        This is an automated confirmation email from help@tmtsbahamas.com<br>
                        For assistance, contact us at <a href="mailto:help@tmtsbahamas.com">help@tmtsbahamas.com</a>
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
        
        TOTAL PAID: ${total_price:.2f} USD
        
        IMPORTANT INFORMATION
        --------------------
        - Pickup Location: Deadman's Cay, Bahamas
        - Required at Pickup: Valid driver's license & $100 security deposit
        - Additional Fee: $10 for pickup/drop-off beyond Deadman's Cay
        - Pickup Time: 8:00 AM - 6:00 PM
        
        CONTACT US
        ----------
        Email: help@tmtsbahamas.com
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

    def send_contact_form_message(self, name, email, phone, message):
        """Send contact form message to admin"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; }}
                .content {{ padding: 20px; background: #f9f9f9; }}
                .message-box {{ background: white; padding: 20px; border-radius: 5px; margin: 20px 0; }}
                .field {{ margin: 10px 0; }}
                .label {{ font-weight: bold; color: #555; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>New Contact Form Message</h2>
            </div>
            <div class="content">
                <div class="message-box">
                    <div class="field">
                        <span class="label">From:</span> {name}
                    </div>
                    <div class="field">
                        <span class="label">Email:</span> <a href="mailto:{email}">{email}</a>
                    </div>
                    <div class="field">
                        <span class="label">Phone:</span> {phone}
                    </div>
                    <div class="field">
                        <span class="label">Message:</span>
                        <p style="background: #f5f5f5; padding: 15px; border-left: 3px solid #3498db;">
                            {message}
                        </p>
                    </div>
                    <div class="field">
                        <span class="label">Received:</span> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        New Contact Form Message
        
        From: {name}
        Email: {email}
        Phone: {phone}
        
        Message:
        {message}
        
        Received: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
        """
        
        return self.send_email(
            to_email=self.admin_email,
            subject=f"Contact Form: Message from {name}",
            html_content=html_content,
            text_content=text_content
        )

    def send_contact_confirmation(self, to_email, name):
        """Send confirmation email to user who submitted contact form"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; }}
                .header {{ background: #2c3e50; color: white; padding: 30px; text-align: center; }}
                .content {{ padding: 30px; }}
                .footer {{ background: #f0f0f0; padding: 20px; text-align: center; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Thank You for Contacting Us!</h1>
            </div>
            <div class="content">
                <p>Dear {name},</p>
                
                <p>We've received your message and appreciate you reaching out to TMT's Coconut Cruisers.</p>
                
                <p>Our team will review your message and get back to you within 24-48 hours.</p>
                
                <p>If you need immediate assistance, please call us at:</p>
                <p>📞 +1 (242) 472-0016 or +1 (242) 367-0942</p>
                
                <p>Best regards,<br>
                TMT's Coconut Cruisers Team</p>
            </div>
            <div class="footer">
                <p>TMT's Coconut Cruisers | Deadman's Cay, Bahamas</p>
                <p>Email: help@tmtsbahamas.com</p>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Thank You for Contacting Us!
        
        Dear {name},
        
        We've received your message and appreciate you reaching out to TMT's Coconut Cruisers.
        
        Our team will review your message and get back to you within 24-48 hours.
        
        If you need immediate assistance, please call us at:
        +1 (242) 472-0016 or +1 (242) 367-0942
        
        Best regards,
        TMT's Coconut Cruisers Team
        
        Email: help@tmtsbahamas.com
        """
        
        return self.send_email(
            to_email=to_email,
            subject="Thank you for contacting TMT's Coconut Cruisers",
            html_content=html_content,
            text_content=text_content
        )

    def send_admin_email(self, to_email, subject, message, is_html=False):
        """Send email from admin panel"""
        
        if is_html:
            html_content = message
            text_content = None
        else:
            # Convert plain text to HTML
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }}
                </style>
            </head>
            <body>
                {message.replace(chr(10), '<br>')}
                <br><br>
                <p style="color: #666; font-size: 12px;">
                    This email was sent from TMT's Coconut Cruisers<br>
                    help@tmtsbahamas.com
                </p>
            </body>
            </html>
            """
            text_content = message + "\n\nThis email was sent from TMT's Coconut Cruisers\nhelp@tmtsbahamas.com"
        
        return self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

# Create a global instance
email_service = EmailService()