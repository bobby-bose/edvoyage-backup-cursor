"""
User models for EdVoyage application.
Handles user authentication, profiles, sessions, and biometric authentication.
"""

import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta


class UserProfile(models.Model):
    """
    Extended user profile model with additional information.
    """
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Information
    email_regex = RegexValidator(
        regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        message="Please enter a valid email address."
    )
    email = models.EmailField(validators=[email_regex], unique=True, verbose_name="Email")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, verbose_name="Gender")
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True, verbose_name="Marital Status")
    
    # Address Information
    address = models.TextField(blank=True, verbose_name="Address")
    city = models.CharField(max_length=100, blank=True, verbose_name="City")
    state = models.CharField(max_length=100, blank=True, verbose_name="State")
    country = models.CharField(max_length=100, blank=True, verbose_name="Country")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="Postal Code")
    
    # Profile Information
    bio = models.TextField(blank=True, verbose_name="Bio")
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True, verbose_name="Profile Picture")
    cover_photo = models.ImageField(upload_to='profiles/covers/', null=True, blank=True, verbose_name="Cover Photo")
    
    # Preferences
    email_notifications = models.BooleanField(default=True, verbose_name="Email Notifications")
    push_notifications = models.BooleanField(default=True, verbose_name="Push Notifications")
    sms_notifications = models.BooleanField(default=False, verbose_name="SMS Notifications")
    
    # Verification
    is_email_verified = models.BooleanField(default=False, verbose_name="Email Verified")
    is_profile_complete = models.BooleanField(default=False, verbose_name="Profile Complete")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(auto_now=True, verbose_name="Last Active")
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self, *args, **kwargs):
        print(f"🔍 DEBUG: Saving user profile - User: {self.user.username}, Email: {self.email}")
        if self.pk:
            print(f"🔍 DEBUG: Updating existing user profile: {self.user.username}")
        else:
            print(f"🔍 DEBUG: Creating new user profile: {self.user.username}")
        super().save(*args, **kwargs)
        print(f"🔍 DEBUG: User profile saved successfully - ID: {self.pk}")
    
    @property
    def age(self):
        """Calculate user age from date of birth."""
        if self.date_of_birth:
            today = timezone.now().date()
            age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            print(f"🔍 DEBUG: Calculated age for {self.user.username}: {age}")
            return age
        print(f"🔍 DEBUG: No date of birth for {self.user.username}")
        return None
    
    @property
    def full_name(self):
        """Get user's full name."""
        full_name = f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
        print(f"🔍 DEBUG: Full name for {self.user.username}: {full_name}")
        return full_name


class UserSession(models.Model):
    """
    User session model for tracking login sessions and device information.
    """
    SESSION_STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, verbose_name="Session Key")
    
    # Device Information
    device_type = models.CharField(max_length=50, blank=True, verbose_name="Device Type")
    device_name = models.CharField(max_length=100, blank=True, verbose_name="Device Name")
    device_id = models.CharField(max_length=255, verbose_name="Device ID")
    browser = models.CharField(max_length=100, blank=True, verbose_name="Browser")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    
    # Session Information
    status = models.CharField(max_length=20, choices=SESSION_STATUS_CHOICES, default='active')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name="Login Time")
    logout_time = models.DateTimeField(null=True, blank=True, verbose_name="Logout Time")
    last_activity = models.DateTimeField(auto_now=True, verbose_name="Last Activity")
    
    # Security
    is_secure = models.BooleanField(default=False, verbose_name="Secure Connection")
    is_mobile = models.BooleanField(default=False, verbose_name="Mobile Device")
    is_active = models.BooleanField(default=True, verbose_name="Active Session")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"
        ordering = ['-login_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.device_type} ({self.session_key})"
    
    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Updating user session: {self.user.username}") if hasattr(self, '_meta') else None
        else:
            print(f"Creating new user session: {self.user.username}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)
    
    @property
    def duration(self):
        """Calculate session duration."""
        if self.logout_time:
            return self.logout_time - self.login_time
        return timezone.now() - self.login_time
    
    def is_expired(self):
        """Check if session is expired (24 hours)"""
        return timezone.now() - self.last_activity > timedelta(hours=24)


class OTPVerification(models.Model):
    """
    OTP verification model for email verification with enhanced security.
    """
    OTP_TYPE_CHOICES = [
        ('email', 'Email'),
        ('password_reset', 'Password Reset'),
        ('login', 'Login'),
        ('register', 'Register'),  # Added for registration OTPs
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_verifications', null=True, blank=True)
    otp_type = models.CharField(max_length=20, choices=OTP_TYPE_CHOICES, verbose_name="OTP Type")
    contact = models.CharField(max_length=255, verbose_name="Contact (Email)")
    otp_code = models.CharField(max_length=6, verbose_name="OTP Code")
    
    # Verification Status
    is_verified = models.BooleanField(default=False, verbose_name="Verified")
    is_expired = models.BooleanField(default=False, verbose_name="Expired")
    
    # Enhanced Security - Attempt Limiting
    failed_attempts = models.PositiveIntegerField(default=0, verbose_name="Failed Attempts")
    max_attempts = models.PositiveIntegerField(default=3, verbose_name="Max Attempts")
    blocked_until = models.DateTimeField(null=True, blank=True, verbose_name="Blocked Until")
    is_blocked = models.BooleanField(default=False, verbose_name="Is Blocked")
    
    # Device Tracking
    device_id = models.CharField(max_length=255, blank=True, verbose_name="Device ID")
    device_type = models.CharField(max_length=50, blank=True, verbose_name="Device Type")
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(verbose_name="Expires At")
    verified_at = models.DateTimeField(null=True, blank=True, verbose_name="Verified At")
    
    class Meta:
        verbose_name = "OTP Verification"
        verbose_name_plural = "OTP Verifications"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.contact} - {self.otp_type} ({self.otp_code})"
    
    def save(self, *args, **kwargs):
        print(f"🔍 DEBUG: Saving OTP verification - Contact: {self.contact}, Type: {self.otp_type}, Code: {self.otp_code}")
        if not self.pk:
            # Set expiration time (15 minutes from creation)
            self.expires_at = timezone.now() + timedelta(minutes=15)
            print(f"🔍 DEBUG: Setting OTP expiration to: {self.expires_at}")
            
        super().save(*args, **kwargs)
        print(f"🔍 DEBUG: OTP verification saved successfully - ID: {self.pk}")
    
    @property
    def is_expired_property(self):
        """Check if OTP is expired based on expires_at field."""
        is_expired = timezone.now() > self.expires_at
        print(f"🔍 DEBUG: OTP expiration check - Current: {timezone.now()}, Expires: {self.expires_at}, Is Expired: {is_expired}")
        return is_expired
    
    @property
    def is_valid(self):
        """Check if OTP is still valid."""
        is_valid = not self.is_expired_property and not self.is_verified and self.failed_attempts < self.max_attempts
        print(f"🔍 DEBUG: OTP validity check - Expired: {self.is_expired_property}, Verified: {self.is_verified}, Failed attempts: {self.failed_attempts}, Valid: {is_valid}")
        return is_valid
    
    def is_blocked_for_device(self, device_id):
        """Check if device is blocked"""
        if self.is_blocked and self.blocked_until:
            is_blocked = timezone.now() < self.blocked_until
            print(f"🔍 DEBUG: Device blocked check - Device: {device_id}, Blocked: {is_blocked}")
            return is_blocked
        return False
    
    def increment_failed_attempts(self):
        """Increment failed attempts and block if needed"""
        print(f"🔍 DEBUG: Incrementing failed attempts - Current: {self.failed_attempts}")
        self.failed_attempts += 1
        if self.failed_attempts >= self.max_attempts:
            self.is_blocked = True
            self.blocked_until = timezone.now() + timedelta(minutes=5)
            print(f"🔍 DEBUG: Device blocked due to max attempts - Blocked until: {self.blocked_until}")
        self.save()
    
    def reset_attempts(self):
        """Reset failed attempts after successful verification"""
        print(f"🔍 DEBUG: Resetting failed attempts")
        self.failed_attempts = 0
        self.is_blocked = False
        self.blocked_until = None
        self.save()


class BiometricAuthentication(models.Model):
    """
    Biometric authentication model for face and voice recognition.
    """
    BIOMETRIC_TYPE_CHOICES = [
        ('face', 'Face Recognition'),
        ('voice', 'Voice Recognition'),
        ('fingerprint', 'Fingerprint'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='biometric_auths')
    biometric_type = models.CharField(max_length=20, choices=BIOMETRIC_TYPE_CHOICES, verbose_name="Biometric Type")
    
    # Biometric Data (encrypted/hashed)
    biometric_data = models.TextField(verbose_name="Biometric Data")
    biometric_hash = models.CharField(max_length=255, verbose_name="Biometric Hash")
    
    # Status
    is_enabled = models.BooleanField(default=True, verbose_name="Enabled")
    is_verified = models.BooleanField(default=False, verbose_name="Verified")
    
    # Security
    last_used = models.DateTimeField(null=True, blank=True, verbose_name="Last Used")
    failed_attempts = models.PositiveIntegerField(default=0, verbose_name="Failed Attempts")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Biometric Authentication"
        verbose_name_plural = "Biometric Authentications"
        unique_together = ['user', 'biometric_type']
    
    def __str__(self):
        return f"{self.user.username} - {self.biometric_type}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Updating biometric auth: {self.user.username} - {self.biometric_type}") if hasattr(self, '_meta') else None
        else:
            print(f"Creating biometric auth: {self.user.username} - {self.biometric_type}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)


class UserActivity(models.Model):
    """
    User activity tracking model for analytics and security.
    """
    ACTIVITY_TYPE_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('profile_update', 'Profile Update'),
        ('password_change', 'Password Change'),
        ('email_verification', 'Email Verification'),
        ('phone_verification', 'Phone Verification'),
        ('otp_verification', 'OTP Verification'),
        ('failed_login', 'Failed Login'),
        ('account_locked', 'Account Locked'),
        ('otp_blocked', 'OTP Blocked'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES, verbose_name="Activity Type")
    
    # Activity Details
    description = models.TextField(blank=True, verbose_name="Description")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    device_id = models.CharField(max_length=255, blank=True, verbose_name="Device ID")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} ({self.created_at})"
    
    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Updating user activity: {self.user.username} - {self.activity_type}") if hasattr(self, '_meta') else None
        else:
            print(f"Creating new user activity: {self.user.username} - {self.activity_type}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)
