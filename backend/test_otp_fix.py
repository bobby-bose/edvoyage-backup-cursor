#!/usr/bin/env python
"""
Test script to verify OTP verification serializers work without recursion errors.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edvoayge.edvoayge.settings')
django.setup()

from users.serializers import (
    UserMinimalSerializer, 
    OTPVerificationSerializer, 
    OTPCreateSerializer, 
    OTPVerifySerializer
)
from users.models import OTPVerification
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def test_serializers():
    """Test that serializers work without recursion errors."""
    print("Testing OTP serializers...")
    
    try:
        # Test OTPCreateSerializer
        print("1. Testing OTPCreateSerializer...")
        create_data = {
            'otp_type': 'register',
            'contact': '+1234567890',
            'device_id': 'test_device_123',
            'device_type': 'mobile'
        }
        create_serializer = OTPCreateSerializer(data=create_data)
        if create_serializer.is_valid():
            print("✓ OTPCreateSerializer validation passed")
        else:
            print("✗ OTPCreateSerializer validation failed:", create_serializer.errors)
            return False
        
        # Test OTPVerifySerializer
        print("2. Testing OTPVerifySerializer...")
        verify_data = {
            'otp_code': '123456',
            'contact': '+1234567890',
            'device_id': 'test_device_123',
            'device_type': 'mobile'
        }
        verify_serializer = OTPVerifySerializer(data=verify_data)
        if verify_serializer.is_valid():
            print("✓ OTPVerifySerializer validation passed")
        else:
            print("✗ OTPVerifySerializer validation failed:", verify_serializer.errors)
            return False
        
        # Test OTPVerificationSerializer with a mock object
        print("3. Testing OTPVerificationSerializer...")
        # Create a test user
        test_user = User.objects.create_user(
            username='testuser_otp',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a test OTP verification
        test_otp = OTPVerification.objects.create(
            user=test_user,
            otp_type='register',
            contact='+1234567890',
            otp_code='123456',
            device_id='test_device_123',
            device_type='mobile',
            expires_at=timezone.now() + timedelta(minutes=15)
        )
        
        # Test serialization
        otp_serializer = OTPVerificationSerializer(test_otp)
        serialized_data = otp_serializer.data
        print("✓ OTPVerificationSerializer serialization passed")
        print(f"  Serialized data keys: {list(serialized_data.keys())}")
        
        # Test UserMinimalSerializer
        print("4. Testing UserMinimalSerializer...")
        user_serializer = UserMinimalSerializer(test_user)
        user_data = user_serializer.data
        print("✓ UserMinimalSerializer serialization passed")
        print(f"  User data keys: {list(user_data.keys())}")
        
        # Clean up
        test_otp.delete()
        test_user.delete()
        
        print("\n🎉 All serializer tests passed! No recursion errors detected.")
        return True
        
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_serializers()
    sys.exit(0 if success else 1) 