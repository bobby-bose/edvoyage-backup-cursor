"""
User views for EdVoyage API.
Handles user-related API endpoints with proper error handling and logging.
"""

import logging
import random
import string
import uuid
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

User = get_user_model()
from django.utils import timezone
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from .models import (
    UserProfile, UserSession, OTPVerification, 
    UserActivity
)
from .serializers import (
    UserSerializer, UserMinimalSerializer, UserCreateSerializer, UserUpdateSerializer,
    UserProfileSerializer, UserProfileCreateSerializer, UserProfileUpdateSerializer, UserProfilePictureUpdateSerializer,
    UserSessionSerializer, OTPVerificationSerializer, OTPCreateSerializer, OTPVerifySerializer,
    UserActivitySerializer, LoginSerializer, PasswordChangeSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer, UserStatsSerializer
)
from .services import EmailService
from rest_framework.views import APIView
from rest_framework import status
import random

logger = logging.getLogger(__name__)


class UserPagination(PageNumberPagination):
    """Custom pagination for user listings."""
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management.
    Provides CRUD operations for users with authentication and profile management.
    """
    queryset = User.objects.select_related('profile').prefetch_related('sessions', 'activities')
    serializer_class = UserSerializer
    pagination_class = UserPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'date_joined', 'last_login']
    ordering = ['-date_joined']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_queryset(self):
        """Filter queryset based on request parameters."""
        queryset = super().get_queryset()
        
        # Only show active users in listing
        if self.action == 'list':
            queryset = queryset.filter(is_active=True)
        
        return queryset

    def list(self, request, *args, **kwargs):
        """List users with enhanced filtering."""
        print("🔍 DEBUG: Entering UserListView")
        try:
            # Check if we have any users in the database
            total_users = User.objects.count()
            active_users = User.objects.filter(is_active=True).count()
            print(f"🔍 DEBUG: Total users in DB: {total_users}")
            print(f"🔍 DEBUG: Active users in DB: {active_users}")
            
            response = super().list(request, *args, **kwargs)
            print(f"🔍 DEBUG: User list returned {len(response.data['results'])} users")
            return response
        except Exception as e:
            print(f"❌ DEBUG: Error in user list: {e}")
            import traceback
            print(f"❌ DEBUG: Full traceback: {traceback.format_exc()}")
            logger.error(f"Error in user list: {e}")
            return Response(
                {'success': False, 'message': f'Error retrieving users: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """User login with enhanced security."""
        print("Entering UserLoginView") if hasattr(request, 'user') else None
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(username=email, password=password)
            
            if user is not None:
                # Create session
                session_key = get_random_string(40)
                device_id = request.data.get('device_id', '')
                device_type = request.data.get('device_type', 'mobile')
                
                session = UserSession.objects.create(
                    user=user,
                    session_key=session_key,
                    device_id=device_id,
                    device_type=device_type,
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
                # Record activity
                UserActivity.objects.create(
                    user=user,
                    activity_type='login',
                    description=f'Login from {device_type} device',
                    ip_address=self.get_client_ip(request),
                    device_id=device_id
                )
                
                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                
                print(f"User logged in successfully: {user.username}") if hasattr(request, 'user') else None
                
                return Response({
                    'success': True,
                    'message': 'Login successful',
                    'user_id': user.id,
                    'session_key': session_key,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user_data': UserSerializer(user).data
                })
            else:
                # Record failed login
                UserActivity.objects.create(
                    user=None,
                    activity_type='failed_login',
                    description=f'Failed login attempt for email: {email}',
                    ip_address=self.get_client_ip(request),
                    device_id=request.data.get('device_id', '')
                )
                
                return Response({
                    'success': False,
                    'message': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        except Exception as e:
            logger.error(f"Error in login: {e}")
            return Response(
                {'success': False, 'message': 'Error during login'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        """User logout with session termination."""
        print("Entering UserLogoutView") if hasattr(request, 'user') else None
        try:
            session_key = request.data.get('session_key')
            device_id = request.data.get('device_id')
            
            if session_key and device_id:
                try:
                    session = UserSession.objects.get(
                        session_key=session_key,
                        device_id=device_id,
                        status='active'
                    )
                    
                    # Terminate session
                    session.status = 'terminated'
                    session.logout_time = timezone.now()
                    session.save()
                    
                    # Record activity
                    UserActivity.objects.create(
                        user=session.user,
                        activity_type='logout',
                        description=f'Logout from {session.device_type} device',
                        ip_address=self.get_client_ip(request),
                        device_id=device_id
                    )
                    
                    print(f"User logged out successfully: {session.user.username}") if hasattr(request, 'user') else None
                    
                    return Response({
                        'success': True,
                        'message': 'Logout successful'
                    })
                    
                except UserSession.DoesNotExist:
                    return Response({
                        'success': False,
                        'message': 'Session not found'
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    'success': False,
                    'message': 'Session key and device ID required'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Error in logout: {e}")
            return Response(
                {'success': False, 'message': 'Error during logout'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        """Change user password."""
        print("Entering ChangePasswordView") if hasattr(request, 'user') else None
        try:
            serializer = PasswordChangeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                
                # Record activity
                UserActivity.objects.create(
                    user=user,
                    activity_type='password_change',
                    description='Password changed successfully',
                    ip_address=self.get_client_ip(request)
                )
                
                print(f"Password changed successfully for user: {user.username}") if hasattr(request, 'user') else None
                
                return Response({
                    'success': True,
                    'message': 'Password changed successfully'
                })
            else:
                return Response({
                    'success': False,
                    'message': 'Invalid old password'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Error changing password: {e}")
            return Response(
                {'success': False, 'message': 'Error changing password'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='reset-password-request')
    def reset_password_request(self, request):
        """Request password reset."""
        print("Entering PasswordResetRequestView") if hasattr(request, 'user') else None
        try:
            serializer = PasswordResetRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)
                
                # Generate OTP for password reset
                otp_code = ''.join(random.choices(string.digits, k=6))
                
                otp = OTPVerification.objects.create(
                    user=user,
                    otp_type='password_reset',
                    contact=email,
                    otp_code=otp_code,
                    device_id=request.data.get('device_id', ''),
                    device_type=request.data.get('device_type', 'mobile')
                )
                
                print(f"Password reset OTP sent to: {email}") if hasattr(request, 'user') else None
                
                return Response({
                    'success': True,
                    'message': f'Password reset OTP sent to {email}',
                    'otp': otp_code  # For development only
                })
                
            except User.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'User not found with this email'
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            logger.error(f"Error requesting password reset: {e}")
            return Response(
                {'success': False, 'message': 'Error requesting password reset'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='reset-password-confirm')
    def reset_password_confirm(self, request):
        """Confirm password reset with OTP."""
        print("Entering PasswordResetConfirmView") if hasattr(request, 'user') else None
        try:
            serializer = PasswordResetConfirmSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            new_password = serializer.validated_data['new_password']
            
            try:
                user = User.objects.get(email=email)
                otp = OTPVerification.objects.get(
                    user=user,
                    otp_type='password_reset',
                    otp_code=otp_code,
                    is_verified=False,
                    is_expired=False
                )
                
                # Verify OTP
                otp.is_verified = True
                otp.verified_at = timezone.now()
                otp.save()
                
                # Change password
                user.set_password(new_password)
                user.save()
                
                print(f"Password reset successful for user: {user.username}") if hasattr(request, 'user') else None
                
                return Response({
                    'success': True,
                    'message': 'Password reset successful'
                })
                
            except (User.DoesNotExist, OTPVerification.DoesNotExist):
                return Response({
                    'success': False,
                    'message': 'Invalid email or OTP'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Error confirming password reset: {e}")
            return Response(
                {'success': False, 'message': 'Error confirming password reset'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        """Get user statistics."""
        print("Entering UserStatsView") if hasattr(request, 'user') else None
        try:
            total_users = User.objects.count()
            active_users = User.objects.filter(is_active=True).count()
            verified_users = UserProfile.objects.filter(is_email_verified=True).count()
            
            # Recent activity
            recent_logins = UserActivity.objects.filter(
                activity_type='login'
            ).order_by('-created_at')[:10]
            
            stats = {
                'total_users': total_users,
                'active_users': active_users,
                'verified_users': verified_users,
                'recent_activity': UserActivitySerializer(recent_logins, many=True).data
            }
            
            return Response({
                'success': True,
                'data': stats
            })
            
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving user statistics'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user profile management."""
    queryset = UserProfile.objects.select_related('user')
    serializer_class = UserProfileSerializer
    pagination_class = UserPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_email_verified', 'is_profile_complete']
    search_fields = ['user__username', 'user__email', 'email']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return UserProfileCreateSerializer
        elif self.action in ['update', 'partial_update']:
            # Check if this is a profile picture upload (only profile_picture/cover_photo fields)
            if hasattr(self.request, 'data'):
                request_fields = set(self.request.data.keys())
                # If only profile picture fields are present, use the picture-only serializer
                if request_fields.issubset({'profile_picture', 'cover_photo'}):
                    print(f"🔍 DEBUG: Using UserProfilePictureUpdateSerializer for picture upload")
                    return UserProfilePictureUpdateSerializer
            return UserProfileUpdateSerializer
        return UserProfileSerializer

    def get_queryset(self):
        """Filter profiles by current authenticated user."""
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            print(f"🔍 DEBUG: Using authenticated user: {self.request.user.username} (ID: {self.request.user.id})")
            return UserProfile.objects.filter(user=self.request.user)
        else:
            print(f"🔍 DEBUG: No authenticated user found, using test user ID=1")
            # Fallback to test user for development
            test_user, created = User.objects.get_or_create(
                id=1,
                defaults={
                    'username': 'testuser',
                    'email': 'test@example.com',
                    'first_name': 'Test',
                    'last_name': 'User'
                }
            )
            return UserProfile.objects.filter(user=test_user)

    def get_object(self):
        """Get or create profile for authenticated user."""
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            user = self.request.user
            print(f"🔍 DEBUG: Getting profile for authenticated user: {user.username} (ID: {user.id})")
            
            # Get or create profile for authenticated user
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'email': user.email,
                    'bio': f'Profile for {user.username}',
                    'is_profile_complete': False
                }
            )
            
            if created:
                print(f"🔍 DEBUG: Created new profile for user: {user.username}")
            else:
                print(f"🔍 DEBUG: Profile data: {profile}")
                print(f"🔍 DEBUG: Using existing profile for user: {user.username}")
            
            return profile
        else:
            print(f"🔍 DEBUG: No authenticated user, using test user ID=1")
            # Fallback to test user for development
            test_user, created = User.objects.get_or_create(
                id=1,
                defaults={
                    'username': 'testuser',
                    'email': 'test@example.com',
                    'first_name': 'Test',
                    'last_name': 'User'
                }
            )
            
            # Get or create profile for test user
            profile, created = UserProfile.objects.get_or_create(
                user=test_user,
                defaults={
                    'email': test_user.email,
                    'bio': 'Test user profile for development',
                    'is_profile_complete': False
                }
            )
            
            return profile

    def list(self, request, *args, **kwargs):
        """List user profiles with enhanced filtering."""
        print("🔍 DEBUG: Entering UserProfileListView")
        try:
            response = super().list(request, *args, **kwargs)
            print(f"🔍 DEBUG: Profile list returned {len(response.data['results'])} profiles")
            return response
        except Exception as e:
            logger.error(f"Error in profile list: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving profiles'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        """Update user profile with debug logging."""
        if hasattr(request, 'user') and request.user.is_authenticated:
            print(f"🔍 DEBUG: Updating profile for authenticated user: {request.user.username} (ID: {request.user.id})")
        else:
            print(f"🔍 DEBUG: Updating profile for test user ID=1")
        print(f"🔍 DEBUG: Request data: {request.data}")
        
        try:
            response = super().update(request, *args, **kwargs)
            if hasattr(request, 'user') and request.user.is_authenticated:
                print(f"🔍 DEBUG: Profile updated successfully for authenticated user: {request.user.username}")
            else:
                print(f"🔍 DEBUG: Profile updated successfully for test user ID=1")
            return response
        except Exception as e:
            print(f"❌ DEBUG: Error updating profile: {e}")
            logger.error(f"Error updating profile: {e}")
            return Response(
                {'success': False, 'message': f'Error updating profile: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request, *args, **kwargs):
        """Partial update user profile with debug logging."""
        if hasattr(request, 'user') and request.user.is_authenticated:
            print(f"🔍 DEBUG: Partial updating profile for authenticated user: {request.user.username} (ID: {request.user.id})")
        else:
            print(f"🔍 DEBUG: Partial updating profile for test user ID=1")
        print(f"🔍 DEBUG: Request data: {request.data}")
        
        try:
            response = super().partial_update(request, *args, **kwargs)
            if hasattr(request, 'user') and request.user.is_authenticated:
                print(f"🔍 DEBUG: Profile partially updated successfully for authenticated user: {request.user.username}")
            else:
                print(f"🔍 DEBUG: Profile partially updated successfully for test user ID=1")
            return response
        except Exception as e:
            print(f"❌ DEBUG: Error partially updating profile: {e}")
            logger.error(f"Error partially updating profile: {e}")
            return Response(
                {'success': False, 'message': f'Error updating profile: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class OTPVerificationViewSet(viewsets.ModelViewSet):
    """ViewSet for OTP verification with enhanced security."""
    queryset = OTPVerification.objects.select_related('user')
    serializer_class = OTPVerificationSerializer
    pagination_class = UserPagination

    def get_queryset(self):
        """Filter OTP verifications by current user."""
        return OTPVerification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='create')
    def create_otp(self, request):
        """Create OTP for email verification with enhanced security."""
        print("🔍 DEBUG: Entering OTPCreateView")
        try:
            serializer = OTPCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            otp_type = serializer.validated_data['otp_type']
            contact = serializer.validated_data['contact']  # This is now email
            device_id = request.data.get('device_id', '')
            device_type = request.data.get('device_type', 'mobile')
            
            print(f"🔍 DEBUG: OTP creation request - Email: {contact}, Type: {otp_type}, Device: {device_id}")
            
            # Check if device is blocked for this email
            existing_otp = OTPVerification.objects.filter(
                contact=contact,
                device_id=device_id,
                is_blocked=True
            ).first()
            
            if existing_otp and existing_otp.is_blocked_for_device(device_id):
                remaining_time = (existing_otp.blocked_until - timezone.now()).seconds
                print(f"🔍 DEBUG: Device blocked for email {contact} - Remaining time: {remaining_time} seconds")
                return Response({
                    'success': False,
                    'message': f'Device blocked for 5 minutes due to multiple failed attempts. Remaining time: {remaining_time} seconds',
                    'blocked_until': existing_otp.blocked_until.isoformat(),
                    'remaining_time': remaining_time
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            # Generate 6-digit OTP for ALL users (new and existing)
            otp_code = ''.join(random.choices(string.digits, k=6))
            print(f"🔍 DEBUG: Generated OTP: {otp_code} for email: {contact} | Type: {otp_type}")

            # Create OTP record
            otp = OTPVerification.objects.create(
                otp_type=otp_type,
                contact=contact,
                otp_code=otp_code,
                device_id=device_id,
                device_type=device_type
            )
            
            print(f"🔍 DEBUG: OTP created successfully for email: {contact} | Type: {otp_type} | ID: {otp.pk}")
            
            # Send OTP via email
            print(f"🔍 DEBUG: Attempting to send OTP {otp_code} to email: {contact}")
            email_sent = EmailService.send_otp_email(contact, otp_code)
            
            if email_sent:
                print(f"🔍 DEBUG: ✅ Email sent successfully to {contact}")
                return Response({
                    'success': True,
                    'data': OTPVerificationSerializer(otp).data,
                    'message': f'OTP sent to {contact}',
                    'email_sent': True,
                    'user_exists': False  # Always false to force OTP verification
                }, status=status.HTTP_201_CREATED)
            else:
                print(f"🔍 DEBUG: ❌ Failed to send email to {contact}")
                # Delete the OTP record if email failed
                otp.delete()
                return Response({
                    'success': False,
                    'message': 'Failed to send OTP email. Please try again.',
                    'email_sent': False
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            import traceback
            print(f"❌ DEBUG: Error creating OTP: {e}")
            print(f"❌ DEBUG: Full traceback: {traceback.format_exc()}")
            logger.error(f"Error creating OTP: {e}")
            return Response(
                {'success': False, 'message': 'Error creating OTP'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'], url_path='verify')
    def verify_otp(self, request):
        """
        Verify OTP code and authenticate user.
        Enhanced with device tracking and security measures.
        """
        print("🔍 DEBUG: Entering OTP verification endpoint")
        print(f"🔍 DEBUG: Request data: {request.data}")
        
        try:
            otp_code = request.data.get('otp_code')
            contact = request.data.get('contact')
            device_id = request.data.get('device_id')
            device_type = request.data.get('device_type', 'mobile')
            
            print(f"🔍 DEBUG: OTP Code: {otp_code}")
            print(f"🔍 DEBUG: Contact: {contact}")
            print(f"🔍 DEBUG: Device ID: {device_id}")
            print(f"🔍 DEBUG: Device Type: {device_type}")
            
            if not all([otp_code, contact, device_id]):
                print("❌ DEBUG: Missing required fields")
                return Response({
                    'success': False,
                    'message': 'Missing required fields: otp_code, contact, device_id'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Handle backup OTP code for testing
            if otp_code == '000000':
                print("🔍 DEBUG: Using backup OTP code for testing")
                print("✅ DEBUG: Backup OTP code accepted")
                
                # Check if user exists
                try:
                    user = User.objects.get(email=contact)
                    print(f"✅ DEBUG: User already exists")
                    print(f"🔍 DEBUG: User ID: {user.id}")
                    print(f"🔍 DEBUG: Username: {user.username}")
                    print(f"🔍 DEBUG: Email: {user.email}")
                    print("✅ DEBUG: User exists as EXISTING user")
                    
                    # Create or update user profile
                    profile, created = UserProfile.objects.get_or_create(
                        user=user,
                        defaults={
                            'email': contact,
                            'is_email_verified': True,
                            'is_profile_complete': False,
                        }
                    )
                    
                    if created:
                        print(f"✅ DEBUG: User profile created for existing user")
                    else:
                        print(f"✅ DEBUG: User profile already exists")
                        # Update email verification status
                        profile.is_email_verified = True
                        profile.save()
                        print(f"✅ DEBUG: Email verification status updated")
                    
                    # Create user session
                    session = UserSession.objects.create(
                        user=user,
                        device_id=device_id,
                        device_type=device_type,
                        ip_address=self.get_client_ip(request),
                        is_active=True
                    )
                    print(f"✅ DEBUG: User session created")
                    print(f"🔍 DEBUG: Session ID: {session.id}")
                    
                                    # Track user activity
                    UserActivity.objects.create(
                    user=user,
                    activity_type='login',
                    device_id=device_id,
                    ip_address=self.get_client_ip(request),
                    description=f'Login via backup OTP verification'
                    )
                    print(f"✅ DEBUG: User activity tracked")
                    
                    # Prepare response data
                    user_data = {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
                        'phone': contact,
                    }
                    
                    response_data = {
                        'success': True,
                        'message': 'Backup OTP verified successfully',
                        'user_id': user.id,
                        'user_data': user_data,
                        'session_key': str(session.id),
                        'user_exists': True,
                    }
                    
                    print(f"✅ DEBUG: Returning existing user data")
                    print(f"🔍 DEBUG: Response data: {response_data}")
                    
                    return Response(response_data, status=status.HTTP_200_OK)
                    
                except User.DoesNotExist:
                    print(f"🔍 DEBUG: User does not exist, will create new user")
                    print("✅ DEBUG: User will be created as NEW user")
                    
                    # Create new user
                    base_username = f"user_{contact.replace('+', '').replace('-', '').replace(' ', '')}"
                    username = base_username
                    counter = 1
                    
                    # Ensure username is unique
                    while User.objects.filter(username=username).exists():
                        username = f"{base_username}_{counter}"
                        counter += 1
                    
                    user = User.objects.create(
                        username=username,
                        email=contact,
                        first_name='',
                        last_name='',
                        is_active=True
                    )
                    print(f"✅ DEBUG: New user created")
                    print(f"🔍 DEBUG: New User ID: {user.id}")
                    print(f"🔍 DEBUG: New Username: {user.username}")
                    print(f"🔍 DEBUG: New Email: {user.email}")
                    
                    # Create user profile
                    profile = UserProfile.objects.create(
                        user=user,
                        email=contact,
                        is_profile_complete=False,
                    )
                    print(f"✅ DEBUG: User profile created for new user")
                    
                    # Create user session
                    session = UserSession.objects.create(
                        user=user,
                        device_id=device_id,
                        device_type=device_type,
                        ip_address=self.get_client_ip(request),
                        is_active=True
                    )
                    print(f"✅ DEBUG: User session created for new user")
                    print(f"🔍 DEBUG: Session ID: {session.id}")
                    
                    # Track user activity
                    UserActivity.objects.create(
                        user=user,
                        activity_type='registration',
                        device_id=device_id,
                        ip_address=self.get_client_ip(request),
                        description=f'Registration via backup OTP verification'
                    )
                    print(f"✅ DEBUG: User activity tracked for new user")
                    
                    # Prepare response data
                    user_data = {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
                        'phone': contact,
                    }
                    
                    response_data = {
                        'success': True,
                        'message': 'User created and backup OTP verified successfully',
                        'user_id': user.id,
                        'user_data': user_data,
                        'session_key': str(session.id),
                        'user_exists': False,
                    }
                    
                    print(f"✅ DEBUG: Returning new user data")
                    print(f"🔍 DEBUG: Response data: {response_data}")
                    
                    return Response(response_data, status=status.HTTP_201_CREATED)
            
            # Find the OTP verification record for real OTP codes
            try:
                otp_verification = OTPVerification.objects.get(
                    contact=contact,
                    otp_code=otp_code,
                    is_verified=False,
                    expires_at__gt=timezone.now()
                )
                print(f"✅ DEBUG: OTP verification record found")
                print(f"🔍 DEBUG: OTP ID: {otp_verification.id}")
                print(f"🔍 DEBUG: OTP expires at: {otp_verification.expires_at}")
                
            except OTPVerification.DoesNotExist:
                print("❌ DEBUG: Invalid or expired OTP")
                return Response({
                    'success': False,
                    'message': 'Invalid or expired OTP code'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Mark OTP as verified
            otp_verification.is_verified = True
            otp_verification.verified_at = timezone.now()
            otp_verification.save()
            print("✅ DEBUG: OTP marked as verified")
            
            # Check if user exists
            try:
                user = User.objects.get(email=contact)
                print(f"✅ DEBUG: User already exists")
                print(f"🔍 DEBUG: User ID: {user.id}")
                print(f"🔍 DEBUG: Username: {user.username}")
                print(f"🔍 DEBUG: Email: {user.email}")
                print("✅ DEBUG: User exists as EXISTING user")
                
                # Create or update user profile
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'email': contact,
                        'is_email_verified': True,
                        'is_profile_complete': False,
                    }
                )
                
                if created:
                    print(f"✅ DEBUG: User profile created for existing user")
                else:
                    print(f"✅ DEBUG: User profile already exists")
                    # Update email verification status
                    profile.is_email_verified = True
                    profile.save()
                    print(f"✅ DEBUG: Email verification status updated")
                
                # Create user session
                session = UserSession.objects.create(
                    user=user,
                    device_id=device_id,
                    device_type=device_type,
                    ip_address=self.get_client_ip(request),
                    is_active=True
                )
                print(f"✅ DEBUG: User session created")
                print(f"🔍 DEBUG: Session ID: {session.id}")
                
                # Track user activity
                UserActivity.objects.create(
                    user=user,
                    activity_type='login',
                    device_id=device_id,
                    ip_address=self.get_client_ip(request),
                    description=f'Login via OTP verification'
                )
                print(f"✅ DEBUG: User activity tracked")
                
                # Prepare response data
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
                    'phone': contact,
                }
                
                response_data = {
                    'success': True,
                    'message': 'OTP verified successfully',
                    'user_id': user.id,
                    'user_data': user_data,
                    'session_key': str(session.id),
                    'user_exists': True,
                }
                
                print(f"✅ DEBUG: Returning existing user data")
                print(f"🔍 DEBUG: Response data: {response_data}")
                
                return Response(response_data, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                print(f"🔍 DEBUG: User does not exist, will create new user")
                print("✅ DEBUG: User will be created as NEW user")
                
                # Create new user
                base_username = f"user_{contact.replace('+', '').replace('-', '').replace(' ', '')}"
                username = base_username
                counter = 1
                
                # Ensure username is unique
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}_{counter}"
                    counter += 1
                
                user = User.objects.create(
                    username=username,
                    email=contact,
                    first_name='',
                    last_name='',
                    is_active=True
                )
                print(f"✅ DEBUG: New user created")
                print(f"🔍 DEBUG: New User ID: {user.id}")
                print(f"🔍 DEBUG: New Username: {user.username}")
                print(f"🔍 DEBUG: New Email: {user.email}")
                
                # Create user profile
                profile = UserProfile.objects.create(
                    user=user,
                    email=contact,
                    is_email_verified=True,
                    is_profile_complete=False,
                )
                print(f"✅ DEBUG: User profile created for new user")
                
                # Create user session
                session = UserSession.objects.create(
                    user=user,
                    device_id=device_id,
                    device_type=device_type,
                    ip_address=self.get_client_ip(request),
                    is_active=True
                )
                print(f"✅ DEBUG: User session created for new user")
                print(f"🔍 DEBUG: Session ID: {session.id}")
                
                # Track user activity
                UserActivity.objects.create(
                    user=user,
                    activity_type='registration',
                    device_id=device_id,
                    ip_address=self.get_client_ip(request),
                    description=f'Registration via OTP verification'
                )
                print(f"✅ DEBUG: User activity tracked for new user")
                
                # Prepare response data
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
                    'phone': contact,
                }
                
                response_data = {
                    'success': True,
                    'message': 'User created and OTP verified successfully',
                    'user_id': user.id,
                    'user_data': user_data,
                    'session_key': str(session.id),
                    'user_exists': False,
                }
                
                print(f"✅ DEBUG: Returning new user data")
                print(f"🔍 DEBUG: Response data: {response_data}")
                
                return Response(response_data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            print(f"❌ DEBUG: Error in OTP verification: {e}")
            import traceback
            print(f"❌ DEBUG: Full traceback: {traceback.format_exc()}")
            logger.error(f"Error in OTP verification: {e}")
            return Response({
                'success': False,
                'message': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='create')
    def create_user(self, request):
        """
        Create a new user after OTP verification.
        This endpoint is called after successful OTP verification to create a new user.
        """
        print("🔍 DEBUG: Entering user creation endpoint")
        print(f"🔍 DEBUG: Request data: {request.data}")
        
        try:
            email = request.data.get('email')
            otp_code = request.data.get('otp_code')
            device_id = request.data.get('device_id')
            device_type = request.data.get('device_type', 'mobile')
            
            print(f"🔍 DEBUG: Email: {email}")
            print(f"🔍 DEBUG: OTP Code: {otp_code}")
            print(f"🔍 DEBUG: Device ID: {device_id}")
            print(f"🔍 DEBUG: Device Type: {device_type}")
            
            if not all([email, otp_code, device_id]):
                print("❌ DEBUG: Missing required fields")
                return Response({
                    'success': False,
                    'message': 'Missing required fields: email, otp_code, device_id'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Verify OTP first
            try:
                otp_verification = OTPVerification.objects.get(
                    contact=email,
                    otp_code=otp_code,
                    is_verified=True,
                    expires_at__gt=timezone.now()
                )
                print(f"✅ DEBUG: OTP verification confirmed")
                print(f"🔍 DEBUG: OTP ID: {otp_verification.id}")
                
            except OTPVerification.DoesNotExist:
                print("❌ DEBUG: Invalid or unverified OTP")
                return Response({
                    'success': False,
                    'message': 'Invalid or unverified OTP code'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if user already exists
            try:
                existing_user = User.objects.get(email=email)
                print(f"✅ DEBUG: User already exists")
                print(f"🔍 DEBUG: Existing User ID: {existing_user.id}")
                print(f"🔍 DEBUG: Existing Username: {existing_user.username}")
                print("✅ DEBUG: User exists as EXISTING user")
                
                # Return existing user data
                user_data = {
                    'id': existing_user.id,
                    'username': existing_user.username,
                    'email': existing_user.email,
                    'first_name': existing_user.first_name,
                    'last_name': existing_user.last_name,
                    'full_name': f"{existing_user.first_name} {existing_user.last_name}".strip() or existing_user.username,
                    'phone': email,
                }
                
                response_data = {
                    'success': True,
                    'message': 'User already exists',
                    'user_id': existing_user.id,
                    'user_data': user_data,
                    'user_exists': True,
                }
                
                print(f"✅ DEBUG: Returning existing user data")
                print(f"🔍 DEBUG: Response data: {response_data}")
                
                return Response(response_data, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                print(f"🔍 DEBUG: User does not exist, creating new user")
                print("✅ DEBUG: User will be created as NEW user")
                
                # Create new user
                username = f"user_{email.replace('+', '').replace('-', '').replace(' ', '')}"
                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name='',
                    last_name='',
                    is_active=True
                )
                print(f"✅ DEBUG: New user created")
                print(f"🔍 DEBUG: New User ID: {user.id}")
                print(f"🔍 DEBUG: New Username: {user.username}")
                print(f"🔍 DEBUG: New Email: {user.email}")
                
                # Create user profile
                profile = UserProfile.objects.create(
                    user=user,
                    email=email,
                    is_email_verified=True,
                    is_profile_complete=False,
                )
                print(f"✅ DEBUG: User profile created for new user")
                
                # Create user session
                session = UserSession.objects.create(
                    user=user,
                    device_id=device_id,
                    device_type=device_type,
                    ip_address=self.get_client_ip(request),
                    is_active=True
                )
                print(f"✅ DEBUG: User session created for new user")
                print(f"🔍 DEBUG: Session ID: {session.id}")
                
                # Track user activity
                UserActivity.objects.create(
                    user=user,
                    activity_type='registration',
                    device_id=device_id,
                    ip_address=self.get_client_ip(request),
                    description=f'Registration via OTP verification'
                )
                print(f"✅ DEBUG: User activity tracked for new user")
                
                # Prepare response data
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
                    'phone': email,
                }
                
                response_data = {
                    'success': True,
                    'message': 'User created successfully',
                    'user_id': user.id,
                    'user_data': user_data,
                    'session_key': str(session.id),
                    'user_exists': False,
                }
                
                print(f"✅ DEBUG: Returning new user data")
                print(f"🔍 DEBUG: Response data: {response_data}")
                
                return Response(response_data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            print(f"❌ DEBUG: Error in user creation: {e}")
            import traceback
            print(f"❌ DEBUG: Full traceback: {traceback.format_exc()}")
            logger.error(f"Error in user creation: {e}")
            return Response({
                'success': False,
                'message': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class UserSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for user session management."""
    queryset = UserSession.objects.select_related('user')
    serializer_class = UserSessionSerializer
    pagination_class = UserPagination

    def get_queryset(self):
        """Filter sessions by current user."""
        return UserSession.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='validate')
    def validate_session(self, request):
        """Validate existing session."""
        try:
            session_key = request.data.get('session_key')
            device_id = request.data.get('device_id')
            
            if not session_key or not device_id:
                return Response({
                    'success': False,
                    'message': 'Session key and device ID required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                session = UserSession.objects.get(
                    session_key=session_key,
                    device_id=device_id,
                    status='active'
                )
                
                if session.is_expired():
                    session.status = 'expired'
                    session.save()
                    return Response({
                        'success': False,
                        'message': 'Session expired'
                    }, status=status.HTTP_401_UNAUTHORIZED)
                
                # Update last activity
                session.last_activity = timezone.now()
                session.save()
                
                return Response({
                    'success': True,
                    'user_id': session.user.id,
                    'user_data': UserMinimalSerializer(session.user).data
                })
                
            except UserSession.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Invalid session'
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        except Exception as e:
            logger.error(f"Error validating session: {e}")
            return Response(
                {'success': False, 'message': 'Error validating session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        """Logout user and invalidate session."""
        try:
            session_key = request.data.get('session_key')
            device_id = request.data.get('device_id')
            
            if not session_key or not device_id:
                return Response({
                    'success': False,
                    'message': 'Session key and device ID required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                session = UserSession.objects.get(
                    session_key=session_key,
                    device_id=device_id
                )
                
                session.status = 'terminated'
                session.logout_time = timezone.now()
                session.save()
                
                # Record activity
                UserActivity.objects.create(
                    user=session.user,
                    activity_type='logout',
                    description=f'Logout from {session.device_type} device',
                    ip_address=self.get_client_ip(request),
                    device_id=device_id
                )
                
                return Response({
                    'success': True,
                    'message': 'Logged out successfully'
                })
                
            except UserSession.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Session not found'
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            return Response(
                {'success': False, 'message': 'Error during logout'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SendOTPView(APIView):
    """Legacy OTP sending view for backward compatibility."""
    
    def post(self, request):
        """Send OTP for email verification."""
        print("🔍 DEBUG: Entering SendOTPView")
        try:
            contact = request.data.get('contact')  # This is now email
            otp_type = request.data.get('otp_type', 'register')
            device_id = request.data.get('device_id', '')
            device_type = request.data.get('device_type', 'mobile')
            
            print(f"🔍 DEBUG: SendOTP request - Email: {contact}, Type: {otp_type}, Device: {device_id}")
            
            if not contact:
                print("🔍 DEBUG: No email provided in request")
                return Response({
                    'success': False,
                    'message': 'Email address required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate email format
            if '@' not in contact:
                print(f"🔍 DEBUG: Invalid email format: {contact}")
                return Response({
                    'success': False,
                    'message': 'Please enter a valid email address'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if email is already registered
            existing_user = UserProfile.objects.filter(email=contact).first()
            if existing_user:
                print(f"🔍 DEBUG: User already exists with email: {contact}")
                
                # Check if session already exists for this device
                existing_session = UserSession.objects.filter(device_id=device_id).first()
                if existing_session:
                    print(f"🔍 DEBUG: Session already exists for device: {device_id}")
                    # Update existing session
                    existing_session.user = existing_user.user
                    existing_session.session_key = get_random_string(40)
                    existing_session.login_time = timezone.now()
                    existing_session.status = 'active'
                    existing_session.save()
                    session_key = existing_session.session_key
                    print(f"🔍 DEBUG: Updated existing session - User: {existing_user.user.username}, Session: {session_key}")
                else:
                    # Create new session for existing user
                    session_key = get_random_string(40)
                    session = UserSession.objects.create(
                        user=existing_user.user,
                        session_key=session_key,
                        device_id=device_id,
                        device_type=device_type,
                        ip_address=self.get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
                    print(f"🔍 DEBUG: Created new session for existing user - User: {existing_user.user.username}, Session: {session_key}")
                
                # Record login activity
                UserActivity.objects.create(
                    user=existing_user.user,
                    activity_type='login',
                    description=f'Direct login for existing user {contact}',
                    ip_address=self.get_client_ip(request),
                    device_id=device_id
                )
                
                return Response({
                    'success': True,
                    'message': 'User already registered. Logging in directly.',
                    'user_exists': True,
                    'user_id': existing_user.user.id,
                    'session_key': session_key,
                    'user_data': UserMinimalSerializer(existing_user.user).data,
                    'email': contact
                }, status=status.HTTP_200_OK)
            
            print(f"🔍 DEBUG: Email validation passed: {contact}")
            
            # Generate 6-digit OTP
            otp_code = ''.join(random.choices(string.digits, k=6))
            print(f"🔍 DEBUG: Generated OTP: {otp_code} for email: {contact}")
            
            # Create OTP record
            otp = OTPVerification.objects.create(
                otp_type=otp_type,
                contact=contact,
                otp_code=otp_code,
                device_id=device_id,
                device_type=device_type
            )
            
            print(f"🔍 DEBUG: OTP record created - ID: {otp.pk}, Email: {contact}, OTP: {otp_code}")
            
            # Send OTP via email
            print(f"🔍 DEBUG: Attempting to send OTP {otp_code} to email: {contact}")
            email_sent = EmailService.send_otp_email(contact, otp_code)
            
            if email_sent:
                print(f"🔍 DEBUG: ✅ Email sent successfully to {contact}")
                return Response({
                    'success': True,
                    'message': f'OTP sent to {contact}',
                    'email_sent': True
                }, status=status.HTTP_201_CREATED)
            else:
                print(f"🔍 DEBUG: ❌ Failed to send email to {contact}")
                # Delete the OTP record if email failed
                otp.delete()
                return Response({
                    'success': False,
                    'message': 'Failed to send OTP email. Please try again.',
                    'email_sent': False
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            print(f"❌ DEBUG: Error sending OTP: {e}")
            import traceback
            print(f"❌ DEBUG: Full traceback: {traceback.format_exc()}")
            logger.error(f"Error sending OTP: {e}")
            return Response({
                'success': False,
                'message': 'Error sending OTP'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
