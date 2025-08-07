"""
Admin configuration for users app.
Provides Django admin interface for user management.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import (
    UserProfile, UserSession, OTPVerification, UserActivity
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile model."""
    
    list_display = [
        'user_username', 'user_email', 'full_name', 'email', 
        'is_email_verified', 'is_profile_complete',
        'last_active', 'created_at'
    ]
    list_filter = [
        'is_email_verified', 'is_profile_complete',
        'gender', 'marital_status', 'email_notifications', 
        'push_notifications', 'sms_notifications', 'created_at'
    ]
    search_fields = [
        'user__username', 'user__email', 'user__first_name', 
        'user__last_name', 'email', 'city', 'country'
    ]
    readonly_fields = [
        'user', 'age', 'full_name', 'last_active', 'created_at', 'updated_at'
    ]
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'full_name', 'age')
        }),
        ('Personal Information', {
            'fields': ('email', 'date_of_birth', 'gender', 'marital_status')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code'),
            'classes': ('collapse',)
        }),
        ('Profile Information', {
            'fields': ('bio', 'profile_picture', 'cover_photo')
        }),
        ('Preferences', {
            'fields': ('email_notifications', 'push_notifications', 'sms_notifications'),
            'classes': ('collapse',)
        }),
        ('Verification Status', {
            'fields': ('is_email_verified', 'is_profile_complete')
        }),
        ('Metadata', {
            'fields': ('last_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_username(self, obj):
        """Display username with link."""
        if obj.user:
            url = reverse('admin:auth_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return '-'
    user_username.short_description = 'Username'
    user_username.admin_order_field = 'user__username'
    
    def user_email(self, obj):
        """Display user email."""
        return obj.user.email if obj.user else '-'
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'
    
    def full_name(self, obj):
        """Display full name."""
        return obj.full_name
    full_name.short_description = 'Full Name'
    
    def age(self, obj):
        """Display age."""
        return obj.age or '-'
    age.short_description = 'Age'
    
    list_per_page = 25
    ordering = ['-created_at']


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """Admin for UserSession model."""
    
    list_display = [
        'user_username', 'device_name', 'browser', 'ip_address', 
        'status', 'login_time', 'duration', 'is_secure', 'is_mobile'
    ]
    list_filter = [
        'status', 'is_secure', 'is_mobile', 'device_type', 
        'login_time', 'created_at'
    ]
    search_fields = [
        'user__username', 'device_name', 'browser', 'ip_address'
    ]
    readonly_fields = [
        'user', 'session_key', 'login_time', 'logout_time', 
        'last_activity', 'duration', 'created_at', 'updated_at'
    ]
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Session Information', {
            'fields': ('session_key', 'status', 'login_time', 'logout_time', 'duration')
        }),
        ('Device Information', {
            'fields': ('device_type', 'device_name', 'browser', 'user_agent')
        }),
        ('Network Information', {
            'fields': ('ip_address', 'is_secure', 'is_mobile')
        }),
        ('Metadata', {
            'fields': ('last_activity', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_username(self, obj):
        """Display username with link."""
        if obj.user:
            url = reverse('admin:auth_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return '-'
    user_username.short_description = 'Username'
    user_username.admin_order_field = 'user__username'
    
    def duration(self, obj):
        """Display session duration."""
        duration = obj.duration
        if duration:
            total_seconds = int(duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}h {minutes}m"
        return '-'
    duration.short_description = 'Duration'
    
    list_per_page = 25
    ordering = ['-login_time']
    
    actions = ['terminate_sessions']
    
    def terminate_sessions(self, request, queryset):
        """Terminate selected sessions."""
        updated = queryset.update(
            status='terminated',
            logout_time=timezone.now()
        )
        self.message_user(request, f'{updated} sessions terminated successfully.')
    terminate_sessions.short_description = "Terminate selected sessions"


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    """Admin for OTPVerification model."""
    
    list_display = [
        'user_username', 'otp_type', 'contact', 'otp_code', 
        'is_verified', 'is_expired', 'is_valid', 'failed_attempts', 'created_at'
    ]
    list_filter = [
        'otp_type', 'is_verified', 'is_expired', 'created_at'
    ]
    search_fields = [
        'user__username', 'contact', 'otp_code'
    ]
    readonly_fields = [
        'user', 'otp_code', 'is_verified', 'is_expired', 'is_valid',
        'created_at', 'expires_at', 'verified_at', 'failed_attempts', 'max_attempts'
    ]
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('OTP Information', {
            'fields': ('otp_type', 'contact', 'otp_code')
        }),
        ('Status', {
            'fields': ('is_verified', 'is_expired', 'is_valid', 'failed_attempts', 'max_attempts')
        }),
        ('Timing', {
            'fields': ('created_at', 'expires_at', 'verified_at')
        }),
    )
    
    def user_username(self, obj):
        """Display username with link."""
        if obj.user:
            url = reverse('admin:auth_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return '-'
    user_username.short_description = 'Username'
    user_username.admin_order_field = 'user__username'
    
    def is_valid(self, obj):
        """Display validity status."""
        return obj.is_valid
    is_valid.boolean = True
    is_valid.short_description = 'Valid'
    
    list_per_page = 25
    ordering = ['-created_at']
    
    actions = ['expire_otps']
    
    def expire_otps(self, request, queryset):
        """Expire selected OTPs."""
        updated = queryset.update(is_expired=True)
        self.message_user(request, f'{updated} OTPs expired successfully.')
    expire_otps.short_description = "Expire selected OTPs"


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """Admin for UserActivity model."""
    
    list_display = [
        'user_username', 'activity_type', 'description', 'ip_address',
        'created_at'
    ]
    list_filter = [
        'activity_type', 'created_at'
    ]
    search_fields = [
        'user__username', 'activity_type', 'description', 'ip_address'
    ]
    readonly_fields = [
        'user', 'activity_type', 'description', 'ip_address', 
        'user_agent', 'created_at'
    ]
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Activity Information', {
            'fields': ('activity_type', 'description')
        }),
        ('Network Information', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )
    
    def user_username(self, obj):
        """Display username with link."""
        if obj.user:
            url = reverse('admin:auth_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return '-'
    user_username.short_description = 'Username'
    user_username.admin_order_field = 'user__username'
    
    list_per_page = 50
    ordering = ['-created_at']
    
    actions = ['clear_old_activities']
    
    def clear_old_activities(self, request, queryset):
        """Clear activities older than 30 days."""
        from datetime import timedelta
        cutoff_date = timezone.now() - timedelta(days=30)
        deleted, _ = queryset.filter(created_at__lt=cutoff_date).delete()
        self.message_user(request, f'{deleted} old activities deleted successfully.')
    clear_old_activities.short_description = "Clear activities older than 30 days"


# Extend User admin
class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    """Extended User admin with profile inline."""
    inlines = (UserProfileInline,)
    list_display = [
        'username', 'email', 'first_name', 'last_name', 'is_active',
        'is_staff', 'date_joined', 'last_login'
    ]
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 'groups', 'date_joined'
    ]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['-date_joined']


# Re-register User admin
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, UserAdmin)
