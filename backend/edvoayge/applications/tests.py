"""
Tests for applications app.
Comprehensive test suite for application models, serializers, and views.
"""

import logging
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import (
    Application, ApplicationDocument, ApplicationStatus, ApplicationInterview,
    ApplicationFee, ApplicationCommunication
)
from .serializers import (
    ApplicationSerializer, ApplicationCreateSerializer, ApplicationDocumentSerializer,
    ApplicationStatusSerializer, ApplicationInterviewSerializer, ApplicationFeeSerializer
)

logger = logging.getLogger(__name__)


class ApplicationModelTest(TestCase):
    """Test cases for Application models."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create university and program for testing
        from universities.models import University, UniversityProgram
        self.university = University.objects.create(
            name='Test University',
            short_name='TU',
            slug='test-university',
            university_type='public',
            country='Test Country',
            city='Test City'
        )
        
        self.program = UniversityProgram.objects.create(
            university=self.university,
            name='Computer Science',
            program_level='undergraduate',
            program_type='full_time',
            duration_years=4
        )
        
        self.application = Application.objects.create(
            user=self.user,
            university=self.university,
            program=self.program,
            application_number='APP-TEST123',
            status='draft',
            priority='medium',
            intended_start_date='2024-09-01',
            intended_start_semester='Fall 2024',
            academic_year='2024-2025',
            personal_statement='This is my personal statement.'
        )
    
    def test_application_creation(self):
        """Test application creation."""
        print("Testing application creation")
        self.assertEqual(self.application.user, self.user)
        self.assertEqual(self.application.university, self.university)
        self.assertEqual(self.application.program, self.program)
        self.assertEqual(self.application.application_number, 'APP-TEST123')
        self.assertEqual(self.application.status, 'draft')
    
    def test_application_days_since_submission(self):
        """Test days since submission calculation."""
        print("Testing days since submission")
        # Application not submitted yet
        self.assertIsNone(self.application.days_since_submission)
        
        # Submit application
        from django.utils import timezone
        self.application.status = 'submitted'
        self.application.submitted_at = timezone.now()
        self.application.save()
        
        self.assertIsNotNone(self.application.days_since_submission)
        self.assertEqual(self.application.days_since_submission, 0)
    
    def test_application_is_overdue(self):
        """Test application overdue check."""
        print("Testing application overdue check")
        # Application not submitted yet
        self.assertFalse(self.application.is_overdue)
        
        # Submit application
        from django.utils import timezone
        from datetime import timedelta
        self.application.status = 'submitted'
        self.application.submitted_at = timezone.now() - timedelta(days=31)
        self.application.save()
        
        self.assertTrue(self.application.is_overdue)
    
    def test_application_document_creation(self):
        """Test application document creation."""
        print("Testing application document creation")
        document = ApplicationDocument.objects.create(
            application=self.application,
            document_type='transcript',
            document_name='Academic Transcript',
            file=SimpleUploadedFile('transcript.pdf', b'file content'),
            is_required=True
        )
        self.assertEqual(document.application, self.application)
        self.assertEqual(document.document_type, 'transcript')
        self.assertTrue(document.is_required)
    
    def test_application_status_creation(self):
        """Test application status creation."""
        print("Testing application status creation")
        status_entry = ApplicationStatus.objects.create(
            application=self.application,
            status='submitted',
            description='Application submitted successfully',
            changed_by=self.user
        )
        self.assertEqual(status_entry.application, self.application)
        self.assertEqual(status_entry.status, 'submitted')
        self.assertEqual(status_entry.changed_by, self.user)
    
    def test_application_interview_creation(self):
        """Test application interview creation."""
        print("Testing application interview creation")
        from django.utils import timezone
        from datetime import timedelta
        
        interview = ApplicationInterview.objects.create(
            application=self.application,
            interview_type='video',
            status='scheduled',
            scheduled_date=timezone.now() + timedelta(days=7),
            duration_minutes=60,
            interviewer_name='Dr. Smith',
            interviewer_email='smith@university.edu'
        )
        self.assertEqual(interview.application, self.application)
        self.assertEqual(interview.interview_type, 'video')
        self.assertEqual(interview.status, 'scheduled')
    
    def test_application_fee_creation(self):
        """Test application fee creation."""
        print("Testing application fee creation")
        from datetime import date
        
        fee = ApplicationFee.objects.create(
            application=self.application,
            fee_type='application_fee',
            amount=50.00,
            currency='USD',
            due_date=date.today(),
            payment_status='pending'
        )
        self.assertEqual(fee.application, self.application)
        self.assertEqual(fee.fee_type, 'application_fee')
        self.assertEqual(fee.amount, 50.00)
    
    def test_application_communication_creation(self):
        """Test application communication creation."""
        print("Testing application communication creation")
        communication = ApplicationCommunication.objects.create(
            application=self.application,
            communication_type='email',
            direction='outbound',
            subject='Application Update',
            message='Your application has been received.',
            from_email='admissions@university.edu',
            to_email='student@example.com'
        )
        self.assertEqual(communication.application, self.application)
        self.assertEqual(communication.communication_type, 'email')
        self.assertEqual(communication.direction, 'outbound')


class ApplicationSerializerTest(TestCase):
    """Test cases for Application serializers."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        from universities.models import University, UniversityProgram
        self.university = University.objects.create(
            name='Test University',
            short_name='TU',
            slug='test-university',
            university_type='public',
            country='Test Country',
            city='Test City'
        )
        
        self.program = UniversityProgram.objects.create(
            university=self.university,
            name='Computer Science',
            program_level='undergraduate',
            program_type='full_time',
            duration_years=4
        )
        
        self.application = Application.objects.create(
            user=self.user,
            university=self.university,
            program=self.program,
            application_number='APP-TEST123',
            status='draft',
            priority='medium',
            intended_start_date='2024-09-01',
            intended_start_semester='Fall 2024',
            academic_year='2024-2025'
        )
    
    def test_application_serializer(self):
        """Test ApplicationSerializer."""
        print("Testing ApplicationSerializer")
        serializer = ApplicationSerializer(self.application)
        data = serializer.data
        
        self.assertEqual(data['application_number'], 'APP-TEST123')
        self.assertEqual(data['status'], 'draft')
        self.assertEqual(data['priority'], 'medium')
        self.assertEqual(data['user_username'], 'testuser')
        self.assertEqual(data['university_name'], 'Test University')
        self.assertEqual(data['program_name'], 'Computer Science')
    
    def test_application_create_serializer(self):
        """Test ApplicationCreateSerializer."""
        print("Testing ApplicationCreateSerializer")
        data = {
            'university': self.university.id,
            'program': self.program.id,
            'intended_start_date': '2024-09-01',
            'intended_start_semester': 'Fall 2024',
            'academic_year': '2024-2025',
            'personal_statement': 'This is my personal statement.',
            'priority': 'high'
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        application = serializer.save()
        self.assertEqual(application.user, self.user)
        self.assertEqual(application.university, self.university)
        self.assertEqual(application.program, self.program)
        self.assertIsNotNone(application.application_number)
    
    def test_application_document_serializer(self):
        """Test ApplicationDocumentSerializer."""
        print("Testing ApplicationDocumentSerializer")
        document = ApplicationDocument.objects.create(
            application=self.application,
            document_type='transcript',
            document_name='Academic Transcript',
            file=SimpleUploadedFile('transcript.pdf', b'file content'),
            is_required=True
        )
        serializer = ApplicationDocumentSerializer(document)
        data = serializer.data
        
        self.assertEqual(data['document_type'], 'transcript')
        self.assertEqual(data['document_name'], 'Academic Transcript')
        self.assertEqual(data['status'], 'pending')
        self.assertTrue(data['is_required'])
    
    def test_application_status_serializer(self):
        """Test ApplicationStatusSerializer."""
        print("Testing ApplicationStatusSerializer")
        status_entry = ApplicationStatus.objects.create(
            application=self.application,
            status='submitted',
            description='Application submitted successfully',
            changed_by=self.user
        )
        serializer = ApplicationStatusSerializer(status_entry)
        data = serializer.data
        
        self.assertEqual(data['status'], 'submitted')
        self.assertEqual(data['description'], 'Application submitted successfully')
        self.assertEqual(data['changed_by_username'], 'testuser')
    
    def test_application_interview_serializer(self):
        """Test ApplicationInterviewSerializer."""
        print("Testing ApplicationInterviewSerializer")
        from django.utils import timezone
        from datetime import timedelta
        
        interview = ApplicationInterview.objects.create(
            application=self.application,
            interview_type='video',
            status='scheduled',
            scheduled_date=timezone.now() + timedelta(days=7),
            duration_minutes=60,
            interviewer_name='Dr. Smith'
        )
        serializer = ApplicationInterviewSerializer(interview)
        data = serializer.data
        
        self.assertEqual(data['interview_type'], 'video')
        self.assertEqual(data['status'], 'scheduled')
        self.assertEqual(data['interviewer_name'], 'Dr. Smith')
        self.assertEqual(data['duration_minutes'], 60)
    
    def test_application_fee_serializer(self):
        """Test ApplicationFeeSerializer."""
        print("Testing ApplicationFeeSerializer")
        from datetime import date
        
        fee = ApplicationFee.objects.create(
            application=self.application,
            fee_type='application_fee',
            amount=50.00,
            currency='USD',
            due_date=date.today(),
            payment_status='pending'
        )
        serializer = ApplicationFeeSerializer(fee)
        data = serializer.data
        
        self.assertEqual(data['fee_type'], 'application_fee')
        self.assertEqual(data['amount'], '50.00')
        self.assertEqual(data['currency'], 'USD')
        self.assertEqual(data['payment_status'], 'pending')


class ApplicationAPITest(APITestCase):
    """Test cases for Application API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create JWT token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Create university and program
        from universities.models import University, UniversityProgram
        self.university = University.objects.create(
            name='Test University',
            short_name='TU',
            slug='test-university',
            university_type='public',
            country='Test Country',
            city='Test City'
        )
        
        self.program = UniversityProgram.objects.create(
            university=self.university,
            name='Computer Science',
            program_level='undergraduate',
            program_type='full_time',
            duration_years=4
        )
        
        self.application = Application.objects.create(
            user=self.user,
            university=self.university,
            program=self.program,
            application_number='APP-TEST123',
            status='draft',
            priority='medium',
            intended_start_date='2024-09-01',
            intended_start_semester='Fall 2024',
            academic_year='2024-2025'
        )
    
    def test_application_list(self):
        """Test application list endpoint."""
        print("Testing application list endpoint")
        url = reverse('application-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_application_detail(self):
        """Test application detail endpoint."""
        print("Testing application detail endpoint")
        url = reverse('application-detail', args=[self.application.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['application_number'], 'APP-TEST123')
        self.assertEqual(response.data['status'], 'draft')
    
    def test_application_create(self):
        """Test application creation endpoint."""
        print("Testing application creation endpoint")
        url = reverse('application-list')
        data = {
            'university': self.university.id,
            'program': self.program.id,
            'intended_start_date': '2024-09-01',
            'intended_start_semester': 'Fall 2024',
            'academic_year': '2024-2025',
            'personal_statement': 'This is my personal statement.',
            'priority': 'high'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['status'], 'draft')
        self.assertIsNotNone(response.data['data']['application_number'])
    
    def test_application_submit(self):
        """Test application submission endpoint."""
        print("Testing application submission endpoint")
        url = reverse('application-submit', args=[self.application.id])
        data = {
            'confirm_submission': True
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Application submitted successfully')
    
    def test_application_search(self):
        """Test application search endpoint."""
        print("Testing application search endpoint")
        url = reverse('application-search')
        data = {
            'status': 'draft',
            'priority': 'medium'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
    
    def test_application_stats(self):
        """Test application statistics endpoint."""
        print("Testing application statistics endpoint")
        url = reverse('application-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_applications', response.data['data'])
        self.assertIn('submitted_applications', response.data['data'])
    
    def test_application_dashboard(self):
        """Test application dashboard endpoint."""
        print("Testing application dashboard endpoint")
        url = reverse('application-dashboard')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_applications', response.data['data'])
        self.assertIn('application_stats', response.data['data'])
    
    def test_application_document_list(self):
        """Test application document list endpoint."""
        print("Testing application document list endpoint")
        ApplicationDocument.objects.create(
            application=self.application,
            document_type='transcript',
            document_name='Academic Transcript',
            file=SimpleUploadedFile('transcript.pdf', b'file content'),
            is_required=True
        )
        
        url = reverse('application-document-list', args=[self.application.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_application_interview_list(self):
        """Test application interview list endpoint."""
        print("Testing application interview list endpoint")
        from django.utils import timezone
        from datetime import timedelta
        
        ApplicationInterview.objects.create(
            application=self.application,
            interview_type='video',
            status='scheduled',
            scheduled_date=timezone.now() + timedelta(days=7),
            duration_minutes=60,
            interviewer_name='Dr. Smith'
        )
        
        url = reverse('application-interview-list', args=[self.application.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_application_fee_list(self):
        """Test application fee list endpoint."""
        print("Testing application fee list endpoint")
        from datetime import date
        
        ApplicationFee.objects.create(
            application=self.application,
            fee_type='application_fee',
            amount=50.00,
            currency='USD',
            due_date=date.today(),
            payment_status='pending'
        )
        
        url = reverse('application-fee-list', args=[self.application.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)


class ApplicationIntegrationTest(TestCase):
    """Integration tests for application functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        from universities.models import University, UniversityProgram
        self.university = University.objects.create(
            name='Test University',
            short_name='TU',
            slug='test-university',
            university_type='public',
            country='Test Country',
            city='Test City'
        )
        
        self.program = UniversityProgram.objects.create(
            university=self.university,
            name='Computer Science',
            program_level='undergraduate',
            program_type='full_time',
            duration_years=4
        )
    
    def test_complete_application_flow(self):
        """Test complete application flow."""
        print("Testing complete application flow")
        
        # Create application
        application = Application.objects.create(
            user=self.user,
            university=self.university,
            program=self.program,
            application_number='APP-TEST123',
            status='draft',
            priority='medium',
            intended_start_date='2024-09-01',
            intended_start_semester='Fall 2024',
            academic_year='2024-2025'
        )
        
        # Add document
        document = ApplicationDocument.objects.create(
            application=application,
            document_type='transcript',
            document_name='Academic Transcript',
            file=SimpleUploadedFile('transcript.pdf', b'file content'),
            is_required=True
        )
        
        # Add status update
        status_entry = ApplicationStatus.objects.create(
            application=application,
            status='submitted',
            description='Application submitted successfully',
            changed_by=self.user
        )
        
        # Submit application
        application.status = 'submitted'
        application.submitted_at = timezone.now()
        application.save()
        
        # Verify application state
        self.assertEqual(application.status, 'submitted')
        self.assertIsNotNone(application.submitted_at)
        self.assertEqual(application.documents.count(), 1)
        self.assertEqual(application.status_history.count(), 1)
    
    def test_application_with_interview_and_fees(self):
        """Test application with interview and fees."""
        print("Testing application with interview and fees")
        
        application = Application.objects.create(
            user=self.user,
            university=self.university,
            program=self.program,
            application_number='APP-TEST123',
            status='submitted',
            priority='high',
            intended_start_date='2024-09-01',
            intended_start_semester='Fall 2024',
            academic_year='2024-2025'
        )
        
        # Add interview
        from django.utils import timezone
        from datetime import timedelta
        
        interview = ApplicationInterview.objects.create(
            application=application,
            interview_type='video',
            status='scheduled',
            scheduled_date=timezone.now() + timedelta(days=7),
            duration_minutes=60,
            interviewer_name='Dr. Smith'
        )
        
        # Add fee
        from datetime import date
        
        fee = ApplicationFee.objects.create(
            application=application,
            fee_type='application_fee',
            amount=50.00,
            currency='USD',
            due_date=date.today(),
            payment_status='pending'
        )
        
        # Verify relationships
        self.assertEqual(application.interviews.count(), 1)
        self.assertEqual(application.fees.count(), 1)
        self.assertEqual(interview.application, application)
        self.assertEqual(fee.application, application)


class ApplicationPerformanceTest(TestCase):
    """Performance tests for application functionality."""
    
    def setUp(self):
        """Set up test data."""
        # Create multiple applications for performance testing
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        from universities.models import University, UniversityProgram
        self.university = University.objects.create(
            name='Test University',
            short_name='TU',
            slug='test-university',
            university_type='public',
            country='Test Country',
            city='Test City'
        )
        
        self.program = UniversityProgram.objects.create(
            university=self.university,
            name='Computer Science',
            program_level='undergraduate',
            program_type='full_time',
            duration_years=4
        )
        
        # Create multiple applications
        for i in range(100):
            Application.objects.create(
                user=self.user,
                university=self.university,
                program=self.program,
                application_number=f'APP-TEST{i:03d}',
                status='draft' if i % 2 == 0 else 'submitted',
                priority='medium',
                intended_start_date='2024-09-01',
                intended_start_semester='Fall 2024',
                academic_year='2024-2025'
            )
    
    def test_application_list_performance(self):
        """Test application list endpoint performance."""
        print("Testing application list performance")
        
        api_client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        
        url = reverse('application-list')
        
        import time
        start_time = time.time()
        response = api_client.get(url)
        end_time = time.time()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(end_time - start_time, 1.0)  # Should complete within 1 second
    
    def test_application_search_performance(self):
        """Test application search performance."""
        print("Testing application search performance")
        
        api_client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        
        url = reverse('application-search')
        
        import time
        start_time = time.time()
        response = api_client.post(url, {'status': 'draft'}, format='json')
        end_time = time.time()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(end_time - start_time, 1.0)  # Should complete within 1 second


if __name__ == '__main__':
    # Run tests with verbose output
    import django
    django.setup()
    
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'test', 'applications', '--verbosity=2'])
