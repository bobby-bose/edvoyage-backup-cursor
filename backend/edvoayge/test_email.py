#!/usr/bin/env python
"""
Test script to verify email configuration and send a test email.
Run this script to test if the email setup is working correctly.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edvoayge.settings')
django.setup()

from users.services import EmailService

def test_email_configuration():
    """Test the email configuration and send a test email."""
    print("=" * 50)
    print("EMAIL CONFIGURATION TEST")
    print("=" * 50)
    
    # Check email configuration status
    print("\n1. Checking email configuration...")
    config_status = EmailService.get_email_config_status()
    for key, value in config_status.items():
        print(f"   {key}: {value}")
    
    # Test email connection
    print("\n2. Testing email connection...")
    connection_success = EmailService.test_email_connection()
    
    if connection_success:
        print("   ✅ Email connection test successful!")
    else:
        print("   ❌ Email connection test failed!")
        return False
    
    # Test OTP email sending
    print("\n3. Testing OTP email sending...")
    test_email = "bobbykboseoffice@gmail.com"  # Send to yourself for testing
    test_otp = "123456"
    
    email_sent = EmailService.send_otp_email(test_email, test_otp)
    
    if email_sent:
        print("   ✅ OTP email sent successfully!")
        print(f"   📧 Check your email: {test_email}")
        print("   🔢 Test OTP code: 123456")
    else:
        print("   ❌ Failed to send OTP email!")
        return False
    
    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    try:
        success = test_email_configuration()
        if success:
            print("\n🎉 Email setup is working correctly!")
            print("You can now use the OTP email feature in your application.")
        else:
            print("\n❌ Email setup has issues. Please check the configuration.")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during email testing: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        sys.exit(1) 