"""
URL patterns for users app.
Defines API endpoints for user management, authentication, and profiles.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserProfileViewSet, OTPVerificationViewSet,
    SendOTPView
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='userprofile')
router.register(r'otp', OTPVerificationViewSet, basename='otp')


app_name = 'users'

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
]

urlpatterns += [
    path('api/auth/send-otp/', SendOTPView.as_view(), name='send-otp'),
] 