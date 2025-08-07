"""
Tests for users app.
Comprehensive test suite for user models, serializers, and views.
"""

import logging
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from .models import (
    UserProfile, UserSession, OTPVerification, 
    BiometricAuthentication, UserActivity
)
from .serializers import (
    UserSerializer, UserCreateSerializer, UserProfileSerializer,
    OTPVerificationSerializer, BiometricAuthenticationSerializer
)

logger = logging.getLogger(__name__)


class UserModelTest(TestCase):
    """Test cases for User models."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            email='test@example.com',
            date_of_birth=timezone.now().date() - timedelta(days=365*25),
            gender='male',
            city='Test City',
            country='Test Country'
        )
    
    def test_user_profile_creation(self):
        """Test user profile creation."""
        print("Testing user profile creation")
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.email, 'test@example.com')
        self.assertEqual(self.profile.gender, 'male')
        self.assertTrue(self.profile.age > 20)
    
    def test_user_profile_full_name(self):
        """Test user profile full name property."""
        print("Testing user profile full name")
        self.assertEqual(self.profile.full_name, 'Test User')
    
    def test_user_profile_age_calculation(self):
        """Test user profile age calculation."""
        print("Testing user profile age calculation")
        self.assertIsNotNone(self.profile.age)
        self.assertTrue(self.profile.age > 0)
    
    def test_user_session_creation(self):
        """Test user session creation."""
        print("Testing user session creation")
        session = UserSession.objects.create(
            user=self.user,
            session_key='test_session_key',
            device_name='Test Device',
            browser='Test Browser',
            ip_address='127.0.0.1'
        )
        self.assertEqual(session.user, self.user)
        self.assertEqual(session.status, 'active')
        self.assertIsNotNone(session.duration)
    
    def test_otp_verification_creation(self):
        """Test OTP verification creation."""
        print("Testing OTP verification creation")
        otp = OTPVerification.objects.create(
            user=self.user,
            otp_type='phone',
            contact='+1234567890',
            otp_code='123456'
        )
        self.assertEqual(otp.user, self.user)
        self.assertEqual(otp.otp_type, 'phone')
        self.assertTrue(otp.is_valid)
    
    def test_biometric_authentication_creation(self):
        """Test biometric authentication creation."""
        print("Testing biometric authentication creation")
        biometric = BiometricAuthentication.objects.create(
            user=self.user,
            biometric_type='face',
            biometric_data='test_face_data',
            biometric_hash='test_hash'
        )
        self.assertEqual(biometric.user, self.user)
        self.assertEqual(biometric.biometric_type, 'face')
        self.assertTrue(biometric.is_enabled)
    
    def test_user_activity_creation(self):
        """Test user activity creation."""
        print("Testing user activity creation")
        activity = UserActivity.objects.create(
            user=self.user,
            activity_type='login',
            description='Test login activity',
            ip_address='127.0.0.1'
        )
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.activity_type, 'login')


class UserSerializerTest(TestCase):
    """Test cases for User serializers."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            email='test@example.com',
            gender='male'
        )
    
    def test_user_serializer(self):
        """Test UserSerializer."""
        print("Testing UserSerializer")
        serializer = UserSerializer(self.user)
        data = serializer.data
        
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['last_name'], 'User')
        self.assertIn('profile', data)
    
    def test_user_create_serializer(self):
        """Test UserCreateSerializer."""
        print("Testing UserCreateSerializer")
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        serializer = UserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
    
    def test_user_profile_serializer(self):
        """Test UserProfileSerializer."""
        print("Testing UserProfileSerializer")
        serializer = UserProfileSerializer(self.profile)
        data = serializer.data
        
        self.assertEqual(data['user_username'], 'testuser')
        self.assertEqual(data['user_email'], 'test@example.com')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['gender'], 'male')
    
    def test_otp_verification_serializer(self):
        """Test OTPVerificationSerializer."""
        print("Testing OTPVerificationSerializer")
        otp = OTPVerification.objects.create(
            user=self.user,
            otp_type='phone',
            contact='+1234567890',
            otp_code='123456'
        )
        serializer = OTPVerificationSerializer(otp)
        data = serializer.data
        
        self.assertEqual(data['user_username'], 'testuser')
        self.assertEqual(data['otp_type'], 'phone')
        self.assertEqual(data['contact'], '+1234567890')
        self.assertEqual(data['otp_code'], '123456')
    
    def test_biometric_authentication_serializer(self):
        """Test BiometricAuthenticationSerializer."""
        print("Testing BiometricAuthenticationSerializer")
        biometric = BiometricAuthentication.objects.create(
            user=self.user,
            biometric_type='face',
            biometric_data='test_data',
            biometric_hash='test_hash'
        )
        serializer = BiometricAuthenticationSerializer(biometric)
        data = serializer.data
        
        self.assertEqual(data['user_username'], 'testuser')
        self.assertEqual(data['biometric_type'], 'face')
        self.assertTrue(data['is_enabled'])


class UserAPITest(APITestCase):
    """Test cases for User API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            email='test@example.com',
            gender='male'
        )
        
        # Create JWT token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    
    def test_user_list(self):
        """Test user list endpoint."""
        print("Testing user list endpoint")
        url = reverse('user-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_user_detail(self):
        """Test user detail endpoint."""
        print("Testing user detail endpoint")
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
    
    def test_user_create(self):
        """Test user creation endpoint."""
        print("Testing user creation endpoint")
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['username'], 'newuser')
        self.assertTrue(UserProfile.objects.filter(user__username='newuser').exists())
    
    def test_user_login(self):
        """Test user login endpoint."""
        print("Testing user login endpoint")
        url = reverse('user-login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data['data'])
        self.assertIn('refresh_token', response.data['data'])
    
    def test_user_logout(self):
        """Test user logout endpoint."""
        print("Testing user logout endpoint")
        url = reverse('user-logout')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logout successful')
    
    def test_user_profile_list(self):
        """Test user profile list endpoint."""
        print("Testing user profile list endpoint")
        url = reverse('userprofile-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_user_profile_detail(self):
        """Test user profile detail endpoint."""
        print("Testing user profile detail endpoint")
        url = reverse('userprofile-detail', args=[self.profile.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
    
    def test_otp_create(self):
        """Test OTP creation endpoint."""
        print("Testing OTP creation endpoint")
        url = reverse('otp-create')
        data = {
            'otp_type': 'phone',
            'contact': '+1234567890'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['otp_type'], 'phone')
        self.assertEqual(response.data['data']['contact'], '+1234567890')
    
    def test_otp_verify(self):
        """Test OTP verification endpoint."""
        print("Testing OTP verification endpoint")
        # Create OTP first
        otp = OTPVerification.objects.create(
            user=self.user,
            otp_type='phone',
            contact='+1234567890',
            otp_code='123456'
        )
        
        url = reverse('otp-verify')
        data = {
            'otp_code': '123456'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'OTP verified successfully')
    
    def test_biometric_create(self):
        """Test biometric authentication creation endpoint."""
        print("Testing biometric authentication creation endpoint")
        url = reverse('biometric-list')
        data = {
            'biometric_type': 'face',
            'biometric_data': 'test_face_data_123456789'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['biometric_type'], 'face')
    
    def test_biometric_verify(self):
        """Test biometric verification endpoint."""
        print("Testing biometric verification endpoint")
        # Create biometric auth first
        biometric = BiometricAuthentication.objects.create(
            user=self.user,
            biometric_type='face',
            biometric_data='test_face_data_123456789',
            biometric_hash='test_hash'
        )
        
        url = reverse('biometric-verify')
        data = {
            'biometric_type': 'face',
            'biometric_data': 'test_face_data_123456789'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Biometric verification successful')
    
    def test_user_stats(self):
        """Test user statistics endpoint."""
        print("Testing user statistics endpoint")
        url = reverse('user-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_users', response.data['data'])
        self.assertIn('active_users', response.data['data'])
        self.assertIn('verified_users', response.data['data'])


class UserIntegrationTest(TestCase):
    """Integration tests for user functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            email='test@example.com'
        )
    
    def test_user_registration_flow(self):
        """Test complete user registration flow."""
        print("Testing user registration flow")
        
        # Test user creation
        user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        
        # Create user via API
        api_client = APIClient()
        url = reverse('user-list')
        response = api_client.post(url, user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify profile was created
        new_user = User.objects.get(username='newuser')
        self.assertTrue(UserProfile.objects.filter(user=new_user).exists())
    
    def test_user_authentication_flow(self):
        """Test complete user authentication flow."""
        print("Testing user authentication flow")
        
        api_client = APIClient()
        
        # Test login
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        url = reverse('user-login')
        response = api_client.post(url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data['data'])
        
        # Test authenticated request
        token = response.data['data']['access_token']
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        profile_url = reverse('userprofile-list')
        profile_response = api_client.get(profile_url)
        
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
    
    def test_otp_verification_flow(self):
        """Test complete OTP verification flow."""
        print("Testing OTP verification flow")
        
        api_client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        
        # Create OTP
        otp_data = {
            'otp_type': 'phone',
            'contact': '+1234567890'
        }
        create_url = reverse('otp-create')
        create_response = api_client.post(create_url, otp_data, format='json')
        
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        
        # Verify OTP
        verify_data = {
            'otp_code': create_response.data['data']['otp_code']
        }
        verify_url = reverse('otp-verify')
        verify_response = api_client.post(verify_url, verify_data, format='json')
        
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)


class UserPerformanceTest(TestCase):
    """Performance tests for user functionality."""
    
    def setUp(self):
        """Set up test data."""
        # Create multiple users for performance testing
        for i in range(100):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='testpass123'
            )
            UserProfile.objects.create(
                user=user,
                email=f'test{i}@example.com'
            )
    
    def test_user_list_performance(self):
        """Test user list endpoint performance."""
        print("Testing user list performance")
        
        api_client = APIClient()
        url = reverse('user-list')
        
        import time
        start_time = time.time()
        response = api_client.get(url)
        end_time = time.time()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(end_time - start_time, 1.0)  # Should complete within 1 second
    
    def test_user_search_performance(self):
        """Test user search performance."""
        print("Testing user search performance")
        
        api_client = APIClient()
        url = reverse('user-list')
        
        import time
        start_time = time.time()
        response = api_client.get(url, {'search': 'user'})
        end_time = time.time()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(end_time - start_time, 1.0)  # Should complete within 1 second


if __name__ == '__main__':
    # Run tests with verbose output
    import django
    django.setup()
    
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'test', 'users', '--verbosity=2'])
