"""
User serializers for EdVoyage API.
Handles data serialization for user-related endpoints.
"""

import uuid
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from .models import (
    UserProfile, UserSession, OTPVerification, 
    BiometricAuthentication, UserActivity
)


class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal user serializer to avoid circular references."""
    
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    profile = serializers.SerializerMethodField()
    
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active', 'profile']
    
    def get_profile(self, obj):
        try:
            return UserProfileSerializer(obj.profile).data
        except UserProfile.DoesNotExist:
            return None


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating users."""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating users."""
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    user = UserMinimalSerializer(read_only=True)
    age = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField()
    profile_picture_url = serializers.SerializerMethodField()
    cover_photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'email', 'date_of_birth', 'gender', 'marital_status',
            'address', 'city', 'state', 'country', 'postal_code', 'bio',
            'profile_picture', 'profile_picture_url', 'cover_photo', 'cover_photo_url',
            'email_notifications', 'push_notifications', 'sms_notifications', 
            'is_email_verified', 'is_profile_complete', 'last_active', 'created_at', 
            'updated_at', 'age', 'full_name'
        ]
    
    def get_profile_picture_url(self, obj):
        """Return full URL for profile picture."""
        if obj.profile_picture:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_picture.url)
            return obj.profile_picture.url
        return None
    
    def get_cover_photo_url(self, obj):
        """Return full URL for cover photo."""
        if obj.cover_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_photo.url)
            return obj.cover_photo.url
        return None
    
    def to_representation(self, instance):
        """Add debugging to serialization."""
        print(f"🔍 DEBUG: Serializing user profile - User: {instance.user.username}, Email: {instance.email}")
        data = super().to_representation(instance)
        print(f"🔍 DEBUG: Serialized data keys: {list(data.keys())}")
        print(f"🔍 DEBUG: Profile picture URL: {data.get('profile_picture_url')}")
        return data


class UserProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating user profiles."""
    
    class Meta:
        model = UserProfile
        fields = [
            'email', 'date_of_birth', 'gender', 'marital_status',
            'address', 'city', 'state', 'country', 'postal_code', 'bio'
        ]
    
    def validate_email(self, value):
        """Validate email and check if already registered."""
        print(f"🔍 DEBUG: Validating email: {value}")
        
        # Check if email is already registered
        if UserProfile.objects.filter(email=value).exists():
            print(f"🔍 DEBUG: Email already registered: {value}")
            raise serializers.ValidationError("This email address is already registered.")
        
        print(f"🔍 DEBUG: Email validation passed: {value}")
        return value


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profiles."""
    
    class Meta:
        model = UserProfile
        fields = [
            'email', 'date_of_birth', 'gender', 'marital_status',
            'address', 'city', 'state', 'country', 'postal_code', 'bio',
            'profile_picture', 'cover_photo', 'email_notifications', 'push_notifications',
            'sms_notifications'
        ]


class UserProfilePictureUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating only profile pictures (no email required)."""
    
    class Meta:
        model = UserProfile
        fields = [
            'profile_picture', 'cover_photo'
        ]


class UserSessionSerializer(serializers.ModelSerializer):
    """Serializer for UserSession model."""
    user = UserMinimalSerializer(read_only=True)
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = UserSession
        fields = [
            'id', 'user', 'session_key', 'device_type', 'device_name', 'device_id',
            'browser', 'ip_address', 'user_agent', 'status', 'login_time', 'logout_time',
            'last_activity', 'is_secure', 'is_mobile', 'created_at', 'updated_at', 'duration'
        ]
    
    def get_duration(self, obj):
        return str(obj.duration) if obj.duration else None


class OTPVerificationSerializer(serializers.ModelSerializer):
    """Serializer for OTPVerification model."""
    user = UserMinimalSerializer(read_only=True)
    is_valid = serializers.ReadOnlyField()
    
    class Meta:
        model = OTPVerification
        fields = [
            'id', 'user', 'otp_type', 'contact', 'otp_code', 'is_verified', 'is_expired',
            'failed_attempts', 'max_attempts', 'blocked_until', 'is_blocked', 'device_id',
            'device_type', 'created_at', 'expires_at', 'verified_at', 'is_valid'
        ]


class OTPCreateSerializer(serializers.Serializer):
    """Serializer for creating OTP."""
    otp_type = serializers.ChoiceField(choices=OTPVerification.OTP_TYPE_CHOICES)
    contact = serializers.EmailField(max_length=255)
    device_id = serializers.CharField(max_length=255, required=False, allow_blank=True)
    device_type = serializers.CharField(max_length=50, required=False, allow_blank=True)
    
    def validate_contact(self, value):
        """Validate email format only."""
        print(f"🔍 DEBUG: Validating email for OTP: {value}")
        
        # Basic email format validation
        if not value or '@' not in value:
            print(f"🔍 DEBUG: Invalid email format: {value}")
            raise serializers.ValidationError("Please enter a valid email address.")
        
        print(f"🔍 DEBUG: Email validation passed for OTP: {value}")
        return value


class OTPVerifySerializer(serializers.Serializer):
    """Serializer for verifying OTP."""
    otp_code = serializers.CharField(max_length=6)
    contact = serializers.EmailField(max_length=255)
    device_id = serializers.CharField(max_length=255, required=False, allow_blank=True)
    device_type = serializers.CharField(max_length=50, required=False, allow_blank=True)
    
    def validate_contact(self, value):
        """Validate email format."""
        print(f"🔍 DEBUG: Validating email for OTP verification: {value}")
        
        if not value or '@' not in value:
            print(f"🔍 DEBUG: Invalid email format for verification: {value}")
            raise serializers.ValidationError("Please enter a valid email address.")
        
        print(f"🔍 DEBUG: Email validation passed for verification: {value}")
        return value


class BiometricAuthenticationSerializer(serializers.ModelSerializer):
    """Serializer for biometric authentication."""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = BiometricAuthentication
        fields = [
            'id', 'user_username', 'biometric_type', 'is_enabled',
            'is_verified', 'last_used', 'failed_attempts',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user_username', 'is_verified', 'last_used',
            'failed_attempts', 'created_at', 'updated_at'
        ]


class BiometricCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating biometric authentication."""
    
    class Meta:
        model = BiometricAuthentication
        fields = ['biometric_type', 'biometric_data']
    
    def validate_biometric_data(self, value):
        """Validate biometric data (basic validation)."""
        if not value or len(value) < 10:
            raise serializers.ValidationError("Biometric data is required and must be valid.")
        return value


class BiometricVerifySerializer(serializers.Serializer):
    """Serializer for biometric verification."""
    
    biometric_type = serializers.ChoiceField(choices=BiometricAuthentication.BIOMETRIC_TYPE_CHOICES)
    biometric_data = serializers.CharField()


class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer for UserActivity model."""
    user = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = UserActivity
        fields = [
            'id', 'user', 'activity_type', 'description', 'ip_address',
            'user_agent', 'device_id', 'created_at'
        ]


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    device_id = serializers.CharField(max_length=255, required=False, allow_blank=True)
    device_type = serializers.CharField(max_length=50, required=False, allow_blank=True)


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change."""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for password reset request."""
    email = serializers.EmailField()
    device_id = serializers.CharField(max_length=255, required=False, allow_blank=True)
    device_type = serializers.CharField(max_length=50, required=False, allow_blank=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for password reset confirmation."""
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)


class UserStatsSerializer(serializers.Serializer):
    """Serializer for user statistics."""
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    verified_users = serializers.IntegerField()
    recent_activity = UserActivitySerializer(many=True) 