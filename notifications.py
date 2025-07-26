import os
import logging
from typing import List, Optional
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from twilio.rest import Client
from jinja2 import Environment, BaseLoader
from sqlalchemy.orm import Session
from models import Users
import asyncio
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email configuration - Using Resend (FREE - 3,000 emails/month)
email_enabled = bool(os.getenv("RESEND_API_KEY") and os.getenv("RESEND_API_KEY") != "your-resend-api-key")

if email_enabled:
    email_config = ConnectionConfig(
        MAIL_USERNAME="resend",  # Resend uses "resend" as username
        MAIL_PASSWORD=os.getenv("RESEND_API_KEY", "your-resend-api-key"),
        MAIL_FROM=os.getenv("MAIL_FROM", "your-verified-email@yourdomain.com"),
        MAIL_PORT=587,
        MAIL_SERVER="smtp.resend.com",
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True
    )
    fastmail = FastMail(email_config)
    logger.info("Email notifications enabled using Resend")
else:
    fastmail = None
    logger.warning("Email notifications disabled - no valid Resend API key found")

# SMS configuration
sms_enabled = bool(
    os.getenv("TWILIO_ACCOUNT_SID") and 
    os.getenv("TWILIO_AUTH_TOKEN") and 
    os.getenv("TWILIO_PHONE_NUMBER") and
    os.getenv("TWILIO_ACCOUNT_SID") != "your-account-sid-here"
)

if sms_enabled:
    twilio_client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )
    twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
    logger.info("SMS notifications enabled using Twilio")
else:
    twilio_client = None
    twilio_phone = None
    logger.warning("SMS notifications disabled - no valid Twilio credentials found")

class NotificationService:
    def __init__(self):
        if email_enabled:
            self.fastmail = fastmail
        else:
            self.fastmail = None
        self.jinja_env = Environment(loader=BaseLoader())
    
    async def send_email_notification(self, user_email: str, user_name: str, notice_data: dict):
        """Send email notification to a user"""
        if not email_enabled or not self.fastmail:
            logger.warning("Email notifications are disabled")
            return False
            
        try:
            # Email template
            email_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background-color: #4CAF50; color: white; padding: 20px; text-align: center; }
                    .content { padding: 20px; background-color: #f9f9f9; }
                    .notice-box { background-color: white; padding: 15px; margin: 15px 0; border-left: 4px solid #4CAF50; }
                    .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔔 New Notice Alert</h1>
                    </div>
                    <div class="content">
                        <p>Hello {{ user_name }},</p>
                        <p>A new notice has been posted on the Notice Board:</p>
                        
                        <div class="notice-box">
                            <h3>{{ notice.title }}</h3>
                            <p><strong>Type:</strong> {{ notice.type }}</p>
                            <p><strong>Description:</strong> {{ notice.description }}</p>
                            {% if notice.event_date %}
                            <p><strong>Event Date:</strong> {{ notice.event_date }}</p>
                            {% endif %}
                            {% if notice.event_start_time %}
                            <p><strong>Event Time:</strong> {{ notice.event_start_time }} - {{ notice.event_end_time }}</p>
                            {% endif %}
                            <p><strong>Posted on:</strong> {{ notice.post_date }}</p>
                        </div>
                        
                        <p>Please check the Notice Board for more details.</p>
                        <p>Best regards,<br>Notice Board Team</p>
                    </div>
                    <div class="footer">
                        <p>This is an automated notification. Please do not reply to this email.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Render template
            template = self.jinja_env.from_string(email_template)
            html_content = template.render(
                user_name=user_name,
                notice=notice_data
            )
            
            # Create message
            message = MessageSchema(
                subject=f"🔔 New Notice: {notice_data['title']}",
                recipients=[user_email],
                body=html_content,
                subtype="html"
            )
            
            # Send email
            await self.fastmail.send_message(message)
            logger.info(f"Email notification sent to {user_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {user_email}: {e}")
            return False
    
    def send_sms_notification(self, phone_number: str, user_name: str, notice_data: dict):
        """Send SMS notification to a user"""
        if not sms_enabled or not twilio_client:
            logger.warning("SMS notifications are disabled")
            return False
            
        try:
            # Create SMS message
            message_body = f"""🔔 New Notice Alert

Hello {user_name},

A new notice has been posted:
Title: {notice_data['title']}
Type: {notice_data['type']}
Description: {notice_data['description']}

Check the Notice Board for more details.

- Notice Board Team"""

            # Send SMS
            message = twilio_client.messages.create(
                body=message_body,
                from_=twilio_phone,
                to=phone_number
            )
            
            logger.info(f"SMS notification sent to {phone_number}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS to {phone_number}: {e}")
            return False
    
    async def notify_all_users(self, db: Session, notice_data: dict):
        """Send notifications to all users"""
        users = db.query(Users).all()
        
        email_sent = 0
        sms_sent = 0
        
        for user in users:
            # Send email notification
            if user.email and email_enabled:
                email_success = await self.send_email_notification(
                    user.email, user.name, notice_data
                )
                if email_success:
                    email_sent += 1
            
            # Send SMS notification
            if user.phone_number and sms_enabled:
                sms_success = self.send_sms_notification(
                    user.phone_number, user.name, notice_data
                )
                if sms_success:
                    sms_sent += 1
        
        logger.info(f"Sent {email_sent}/{len(users)} email notifications")
        logger.info(f"Sent {sms_sent}/{len(users)} SMS notifications")

# Create notification service instance
notification_service = NotificationService() 