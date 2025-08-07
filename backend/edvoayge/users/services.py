import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
import traceback

logger = logging.getLogger(__name__)

class EmailService:
    """
    Service class for handling email operations in the EdVoyage application.
    Provides methods for sending OTP emails and other email notifications.
    """
    
    @staticmethod
    def send_otp_email(email_address, otp_code, user_name=None):
        """
        Send OTP verification email to the specified email address.
        
        Args:
            email_address (str): The recipient's email address
            otp_code (str): The OTP code to send
            user_name (str, optional): The user's name for personalization
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            print(f"EmailService: Starting OTP email send process for {email_address}")
            print(f"EmailService: OTP code to send: {otp_code}")
            
            # Prepare email context
            context = {
                'otp_code': otp_code,
                'user_name': user_name or 'User',
                'app_name': 'EdVoyage'
            }
            
            print(f"EmailService: Email context prepared: {context}")
            
            # Render HTML email template
            html_message = render_to_string('emails/otp_email.html', context)
            print(f"EmailService: HTML template rendered successfully")
            
            # Create plain text version
            plain_message = strip_tags(html_message)
            print(f"EmailService: Plain text version created")
            
            # Email subject
            subject = f'EdVoyage OTP Verification - {otp_code}'
            print(f"EmailService: Email subject: {subject}")
            
            # Send email
            print(f"EmailService: Attempting to send email via SMTP")
            email_sent = send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email_address],
                html_message=html_message,
                fail_silently=False
            )
            
            if email_sent:
                print(f"EmailService: ✅ Email sent successfully to {email_address}")
                logger.info(f"OTP email sent successfully to {email_address}")
                return True
            else:
                print(f"EmailService: ❌ Failed to send email to {email_address}")
                logger.error(f"Failed to send OTP email to {email_address}")
                return False
                
        except Exception as e:
            print(f"EmailService: ❌ Exception occurred while sending email: {str(e)}")
            print(f"EmailService: Exception details: {traceback.format_exc()}")
            logger.error(f"Exception sending OTP email to {email_address}: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    @staticmethod
    def test_email_connection():
        """
        Test the email configuration by sending a test email.
        
        Returns:
            bool: True if test email sent successfully, False otherwise
        """
        try:
            print("EmailService: Testing email connection...")
            
            test_subject = "EdVoyage Email Test"
            test_message = "This is a test email to verify the email configuration is working correctly."
            
            email_sent = send_mail(
                subject=test_subject,
                message=test_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],  # Send to self for testing
                fail_silently=False
            )
            
            if email_sent:
                print("EmailService: ✅ Email connection test successful")
                logger.info("Email connection test successful")
                return True
            else:
                print("EmailService: ❌ Email connection test failed")
                logger.error("Email connection test failed")
                return False
                
        except Exception as e:
            print(f"EmailService: ❌ Exception during email connection test: {str(e)}")
            print(f"EmailService: Exception details: {traceback.format_exc()}")
            logger.error(f"Exception during email connection test: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    @staticmethod
    def get_email_config_status():
        """
        Get the current email configuration status.
        
        Returns:
            dict: Configuration status information
        """
        config_status = {
            'backend': getattr(settings, 'EMAIL_BACKEND', 'Not configured'),
            'host': getattr(settings, 'EMAIL_HOST', 'Not configured'),
            'port': getattr(settings, 'EMAIL_PORT', 'Not configured'),
            'use_tls': getattr(settings, 'EMAIL_USE_TLS', False),
            'host_user': getattr(settings, 'EMAIL_HOST_USER', 'Not configured'),
            'host_password': 'Configured' if getattr(settings, 'EMAIL_HOST_PASSWORD', None) else 'Not configured',
            'default_from_email': getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not configured')
        }
        
        print(f"EmailService: Email configuration status: {config_status}")
        return config_status 