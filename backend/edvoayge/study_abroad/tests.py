from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from decimal import Decimal
import uuid

from .models import (
    StudyAbroadProgram, StudyAbroadApplication, StudyAbroadExperience,
    StudyAbroadResource, StudyAbroadEvent, StudyAbroadEventRegistration
)
from .serializers import (
    StudyAbroadProgramSerializer, StudyAbroadApplicationSerializer, StudyAbroadExperienceSerializer,
    StudyAbroadResourceSerializer, StudyAbroadEventSerializer, StudyAbroadEventRegistrationSerializer
)

User = get_user_model()

class StudyAbroadProgramModelTest(TestCase):
    """Test cases for StudyAbroadProgram model"""
    
    def setUp(self):
        """Set up test data"""
        self.program = StudyAbroadProgram.objects.create(
            name="Test Study Abroad Program",
            description="A test study abroad program",
            program_type="semester",
            status="active",
            country="United States",
            city="New York",
            institution="Test University",
            start_date=timezone.now().date(),
            end_date=timezone.now().date().replace(month=timezone.now().date().month + 4),
            application_deadline=timezone.now().date().replace(day=timezone.now().date().day - 30),
            tuition_cost=Decimal('5000.00'),
            accommodation_cost=Decimal('2000.00'),
            max_participants=20
        )

    def test_program_creation(self):
        """Test program creation"""
        self.assertEqual(self.program.name, "Test Study Abroad Program")
        self.assertEqual(self.program.program_type, "semester")
        self.assertEqual(self.program.country, "United States")

    def test_program_str(self):
        """Test string representation"""
        expected = "Test Study Abroad Program - New York, United States"
        self.assertEqual(str(self.program), expected)

    def test_total_cost_calculation(self):
        """Test total cost calculation"""
        expected_total = Decimal('7000.00')  # 5000 + 2000
        self.assertEqual(self.program.total_cost, expected_total)

    def test_duration_calculation(self):
        """Test duration calculation"""
        self.assertGreater(self.program.duration_days, 0)

    def test_application_open_status(self):
        """Test application open status"""
        # Should be open since deadline is in the future
        self.assertTrue(self.program.is_application_open)

    def test_available_spots(self):
        """Test available spots calculation"""
        self.assertEqual(self.program.available_spots, 20)

class StudyAbroadApplicationModelTest(TestCase):
    """Test cases for StudyAbroadApplication model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.program = StudyAbroadProgram.objects.create(
            name="Test Program",
            description="Test description",
            program_type="semester",
            country="United States",
            city="New York",
            institution="Test University",
            start_date=timezone.now().date(),
            end_date=timezone.now().date().replace(month=timezone.now().date().month + 4),
            application_deadline=timezone.now().date().replace(day=timezone.now().date().day + 30)
        )
        self.application = StudyAbroadApplication.objects.create(
            user=self.user,
            program=self.program,
            current_institution="Current University",
            current_major="Computer Science",
            current_gpa=Decimal('3.5'),
            academic_goals="Learn new skills",
            personal_statement="I want to study abroad"
        )

    def test_application_creation(self):
        """Test application creation"""
        self.assertEqual(self.application.user, self.user)
        self.assertEqual(self.application.program, self.program)
        self.assertEqual(self.application.status, "draft")

    def test_application_str(self):
        """Test string representation"""
        expected = f"{self.user.username} - {self.program.name}"
        self.assertEqual(str(self.application), expected)

    def test_status_change_timestamps(self):
        """Test timestamps on status change"""
        # Test review date
        self.application.status = "under_review"
        self.application.save()
        self.assertIsNotNone(self.application.review_date)

        # Test decision date
        self.application.status = "accepted"
        self.application.save()
        self.assertIsNotNone(self.application.decision_date)

class StudyAbroadExperienceModelTest(TestCase):
    """Test cases for StudyAbroadExperience model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.program = StudyAbroadProgram.objects.create(
            name="Test Program",
            description="Test description",
            program_type="semester",
            country="United States",
            city="New York",
            institution="Test University",
            start_date=timezone.now().date(),
            end_date=timezone.now().date().replace(month=timezone.now().date().month + 4),
            application_deadline=timezone.now().date().replace(day=timezone.now().date().day - 30)
        )
        self.experience = StudyAbroadExperience.objects.create(
            user=self.user,
            program=self.program,
            title="Amazing Experience",
            experience_type="academic",
            content="This was an amazing experience",
            rating=5
        )

    def test_experience_creation(self):
        """Test experience creation"""
        self.assertEqual(self.experience.title, "Amazing Experience")
        self.assertEqual(self.experience.rating, 5)
        self.assertEqual(self.experience.experience_type, "academic")

    def test_experience_str(self):
        """Test string representation"""
        expected = f"Amazing Experience - {self.user.username}"
        self.assertEqual(str(self.experience), expected)

class StudyAbroadResourceModelTest(TestCase):
    """Test cases for StudyAbroadResource model"""
    
    def setUp(self):
        """Set up test data"""
        self.resource = StudyAbroadResource.objects.create(
            title="Test Resource",
            resource_type="guide",
            description="A test resource",
            content="This is the content of the resource",
            categories="Study Abroad, Preparation",
            tags="guide, preparation, tips"
        )

    def test_resource_creation(self):
        """Test resource creation"""
        self.assertEqual(self.resource.title, "Test Resource")
        self.assertEqual(self.resource.resource_type, "guide")

    def test_resource_str(self):
        """Test string representation"""
        self.assertEqual(str(self.resource), "Test Resource")

    def test_view_count_increment(self):
        """Test view count increment"""
        initial_count = self.resource.view_count
        self.resource.increment_view_count()
        self.assertEqual(self.resource.view_count, initial_count + 1)

    def test_download_count_increment(self):
        """Test download count increment"""
        initial_count = self.resource.download_count
        self.resource.increment_download_count()
        self.assertEqual(self.resource.download_count, initial_count + 1)

class StudyAbroadEventModelTest(TestCase):
    """Test cases for StudyAbroadEvent model"""
    
    def setUp(self):
        """Set up test data"""
        self.event = StudyAbroadEvent.objects.create(
            title="Test Event",
            event_type="info_session",
            description="A test event",
            start_datetime=timezone.now() + timezone.timedelta(days=7),
            end_datetime=timezone.now() + timezone.timedelta(days=7, hours=2),
            location="Test Location",
            max_attendees=50
        )

    def test_event_creation(self):
        """Test event creation"""
        self.assertEqual(self.event.title, "Test Event")
        self.assertEqual(self.event.event_type, "info_session")

    def test_event_str(self):
        """Test string representation"""
        expected = f"Test Event - {self.event.start_datetime.strftime('%Y-%m-%d %H:%M')}"
        self.assertEqual(str(self.event), expected)

    def test_registration_open_status(self):
        """Test registration open status"""
        self.assertTrue(self.event.is_registration_open)

    def test_available_spots(self):
        """Test available spots calculation"""
        self.assertEqual(self.event.available_spots, 50)

class StudyAbroadEventRegistrationModelTest(TestCase):
    """Test cases for StudyAbroadEventRegistration model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.event = StudyAbroadEvent.objects.create(
            title="Test Event",
            event_type="info_session",
            description="A test event",
            start_datetime=timezone.now() + timezone.timedelta(days=7),
            end_datetime=timezone.now() + timezone.timedelta(days=7, hours=2),
            location="Test Location"
        )
        self.registration = StudyAbroadEventRegistration.objects.create(
            user=self.user,
            event=self.event,
            dietary_restrictions="Vegetarian"
        )

    def test_registration_creation(self):
        """Test registration creation"""
        self.assertEqual(self.registration.user, self.user)
        self.assertEqual(self.registration.event, self.event)
        self.assertEqual(self.registration.status, "registered")

    def test_registration_str(self):
        """Test string representation"""
        expected = f"{self.user.username} - {self.event.title}"
        self.assertEqual(str(self.registration), expected)

    def test_mark_attended(self):
        """Test marking registration as attended"""
        self.registration.mark_attended()
        self.assertEqual(self.registration.status, "attended")
        self.assertIsNotNone(self.registration.attendance_date)

class StudyAbroadSerializerTest(TestCase):
    """Test cases for study abroad serializers"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.program = StudyAbroadProgram.objects.create(
            name="Test Program",
            description="Test description",
            program_type="semester",
            country="United States",
            city="New York",
            institution="Test University",
            start_date=timezone.now().date(),
            end_date=timezone.now().date().replace(month=timezone.now().date().month + 4),
            application_deadline=timezone.now().date().replace(day=timezone.now().date().day + 30)
        )

    def test_program_serializer(self):
        """Test StudyAbroadProgramSerializer"""
        data = {
            'name': 'New Program',
            'description': 'A new program',
            'program_type': 'summer',
            'country': 'Canada',
            'city': 'Toronto',
            'institution': 'New University',
            'start_date': timezone.now().date(),
            'end_date': timezone.now().date().replace(month=timezone.now().date().month + 2),
            'application_deadline': timezone.now().date().replace(day=timezone.now().date().day + 15)
        }
        serializer = StudyAbroadProgramSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        program = serializer.save()
        self.assertEqual(program.name, 'New Program')

    def test_application_serializer(self):
        """Test StudyAbroadApplicationSerializer"""
        data = {
            'user': self.user.id,
            'program': self.program.id,
            'current_institution': 'Current University',
            'current_major': 'Physics',
            'current_gpa': '3.8',
            'academic_goals': 'Learn physics abroad'
        }
        serializer = StudyAbroadApplicationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        application = serializer.save()
        self.assertEqual(application.current_institution, 'Current University')

    def test_serializer_validation(self):
        """Test serializer validation"""
        # Test invalid GPA
        data = {
            'user': self.user.id,
            'program': self.program.id,
            'current_institution': 'Current University',
            'current_major': 'Physics',
            'current_gpa': '5.0',  # Invalid GPA
            'academic_goals': 'Learn physics abroad'
        }
        serializer = StudyAbroadApplicationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('current_gpa', serializer.errors)

class StudyAbroadViewSetTest(APITestCase):
    """Test cases for study abroad ViewSets"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpass123")
        
        self.program = StudyAbroadProgram.objects.create(
            name="Test Program",
            description="Test description",
            program_type="semester",
            status="active",
            country="United States",
            city="New York",
            institution="Test University",
            start_date=timezone.now().date(),
            end_date=timezone.now().date().replace(month=timezone.now().date().month + 4),
            application_deadline=timezone.now().date().replace(day=timezone.now().date().day + 30),
            is_active=True
        )

    def test_program_list(self):
        """Test program list endpoint"""
        self.client.force_authenticate(user=self.user)
        url = reverse('study-abroad-program-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_active_programs(self):
        """Test active programs endpoint"""
        self.client.force_authenticate(user=self.user)
        url = reverse('study-abroad-programs-active')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_featured_programs(self):
        """Test featured programs endpoint"""
        self.program.is_featured = True
        self.program.save()
        
        self.client.force_authenticate(user=self.user)
        url = reverse('study-abroad-programs-featured')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_programs_by_country(self):
        """Test programs by country endpoint"""
        self.client.force_authenticate(user=self.user)
        url = reverse('study-abroad-programs-by-country')
        response = self.client.get(url, {'country': 'United States'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_application_create(self):
        """Test application creation"""
        self.client.force_authenticate(user=self.user)
        url = reverse('study-abroad-application-list')
        data = {
            'program': self.program.id,
            'current_institution': 'Current University',
            'current_major': 'Computer Science',
            'current_gpa': '3.5',
            'academic_goals': 'Learn new skills'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StudyAbroadApplication.objects.count(), 1)

    def test_my_applications(self):
        """Test my applications endpoint"""
        # Create application
        application = StudyAbroadApplication.objects.create(
            user=self.user,
            program=self.program,
            current_institution='Current University',
            current_major='Computer Science',
            academic_goals='Learn new skills'
        )
        
        self.client.force_authenticate(user=self.user)
        url = reverse('study-abroad-applications-my-applications')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_review_application_admin_only(self):
        """Test that only admins can review applications"""
        application = StudyAbroadApplication.objects.create(
            user=self.user,
            program=self.program,
            current_institution='Current University',
            current_major='Computer Science',
            academic_goals='Learn new skills'
        )
        
        # Test with regular user
        self.client.force_authenticate(user=self.user)
        url = reverse('study-abroad-application-review-application', kwargs={'pk': application.id})
        response = self.client.post(url, {'status': 'accepted'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test with admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, {'status': 'accepted'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify application was updated
        application.refresh_from_db()
        self.assertEqual(application.status, 'accepted')

class StudyAbroadIntegrationTest(APITestCase):
    """Integration tests for study abroad workflow"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpass123")
        
        self.program = StudyAbroadProgram.objects.create(
            name="Test Program",
            description="Test description",
            program_type="semester",
            status="active",
            country="United States",
            city="New York",
            institution="Test University",
            start_date=timezone.now().date(),
            end_date=timezone.now().date().replace(month=timezone.now().date().month + 4),
            application_deadline=timezone.now().date().replace(day=timezone.now().date().day + 30),
            is_active=True
        )

    def test_complete_study_abroad_workflow(self):
        """Test complete study abroad workflow"""
        self.client.force_authenticate(user=self.user)
        
        # 1. Create application
        application_data = {
            'program': self.program.id,
            'current_institution': 'Current University',
            'current_major': 'Computer Science',
            'current_gpa': '3.5',
            'academic_goals': 'Learn new skills'
        }
        application_response = self.client.post(reverse('study-abroad-application-list'), application_data)
        self.assertEqual(application_response.status_code, status.HTTP_201_CREATED)
        application_id = application_response.data['id']
        
        # 2. Admin reviews and accepts application
        self.client.force_authenticate(user=self.admin_user)
        review_url = reverse('study-abroad-application-review-application', kwargs={'pk': application_id})
        review_response = self.client.post(review_url, {'status': 'accepted'})
        self.assertEqual(review_response.status_code, status.HTTP_200_OK)
        
        # 3. User creates experience
        self.client.force_authenticate(user=self.user)
        experience_data = {
            'program': self.program.id,
            'title': 'Amazing Experience',
            'experience_type': 'academic',
            'content': 'This was an amazing experience',
            'rating': 5
        }
        experience_response = self.client.post(reverse('study-abroad-experience-list'), experience_data)
        self.assertEqual(experience_response.status_code, status.HTTP_201_CREATED)
        
        # 4. Admin approves experience
        self.client.force_authenticate(user=self.admin_user)
        experience_id = experience_response.data['id']
        approve_url = reverse('study-abroad-experience-approve-experience', kwargs={'pk': experience_id})
        approve_response = self.client.post(approve_url)
        self.assertEqual(approve_response.status_code, status.HTTP_200_OK)
        
        # 5. Verify all records exist
        application = StudyAbroadApplication.objects.get(id=application_id)
        self.assertEqual(application.status, 'accepted')
        
        experience = StudyAbroadExperience.objects.get(id=experience_id)
        self.assertTrue(experience.is_approved)

    def test_event_registration_workflow(self):
        """Test event registration workflow"""
        # Create event
        event = StudyAbroadEvent.objects.create(
            title="Test Event",
            event_type="info_session",
            description="A test event",
            start_datetime=timezone.now() + timezone.timedelta(days=7),
            end_datetime=timezone.now() + timezone.timedelta(days=7, hours=2),
            location="Test Location",
            max_attendees=50
        )
        
        self.client.force_authenticate(user=self.user)
        
        # Register for event
        registration_data = {
            'event': event.id,
            'dietary_restrictions': 'Vegetarian'
        }
        registration_response = self.client.post(reverse('study-abroad-event-registration-list'), registration_data)
        self.assertEqual(registration_response.status_code, status.HTTP_201_CREATED)
        
        # Mark as attended
        registration_id = registration_response.data['id']
        attended_url = reverse('study-abroad-event-registration-mark-attended', kwargs={'pk': registration_id})
        attended_response = self.client.post(attended_url)
        self.assertEqual(attended_response.status_code, status.HTTP_200_OK)
        
        # Verify registration was updated
        registration = StudyAbroadEventRegistration.objects.get(id=registration_id)
        self.assertEqual(registration.status, 'attended')
        self.assertIsNotNone(registration.attendance_date)
