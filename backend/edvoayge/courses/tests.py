"""
Test cases for courses app.
Provides comprehensive testing for all course-related functionality.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from .models import (
    Course, Subject, CourseSubject, FeeStructure, 
    CourseRequirement, CourseApplication, CourseRating
)


class CourseModelTest(TestCase):
    """Test cases for Course model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a mock university (you'll need to import University model)
        # self.university = University.objects.create(
        #     name='Test University',
        #     country='Test Country'
        # )
        
        self.course = Course.objects.create(
            name='Test Course',
            code='TC001',
            description='Test course description',
            short_description='Short test description',
            # university=self.university,
            level='undergraduate',
            duration='4_years',
            credits=120,
            tuition_fee=Decimal('15000.00'),
            currency='USD',
            minimum_gpa=Decimal('3.0'),
            language_requirements='IELTS 6.5',
            status='active',
            is_featured=True,
            is_popular=False
        )
    
    def test_course_creation(self):
        """Test course creation."""
        self.assertEqual(self.course.name, 'Test Course')
        self.assertEqual(self.course.code, 'TC001')
        self.assertEqual(self.course.level, 'undergraduate')
        self.assertEqual(self.course.status, 'active')
        self.assertTrue(self.course.is_featured)
        self.assertFalse(self.course.is_popular)
    
    def test_course_str_representation(self):
        """Test string representation of course."""
        expected = f"{self.course.name} - {self.course.university.name if hasattr(self.course, 'university') else 'No University'}"
        self.assertEqual(str(self.course), expected)
    
    def test_course_average_rating(self):
        """Test average rating calculation."""
        # Initially no ratings
        self.assertEqual(self.course.average_rating, 0)
        
        # Add ratings
        CourseRating.objects.create(
            user=self.user,
            course=self.course,
            rating=4
        )
        CourseRating.objects.create(
            user=User.objects.create_user(username='user2', password='pass'),
            course=self.course,
            rating=5
        )
        
        # Refresh from database
        self.course.refresh_from_db()
        self.assertEqual(self.course.average_rating, 4.5)
    
    def test_course_total_applications(self):
        """Test total applications count."""
        # Initially no applications
        self.assertEqual(self.course.total_applications, 0)
        
        # Add application
        CourseApplication.objects.create(
            user=self.user,
            course=self.course,
            status='submitted'
        )
        
        # Refresh from database
        self.course.refresh_from_db()
        self.assertEqual(self.course.total_applications, 1)


class SubjectModelTest(TestCase):
    """Test cases for Subject model."""
    
    def setUp(self):
        """Set up test data."""
        self.subject = Subject.objects.create(
            name='Mathematics',
            code='MATH101',
            description='Basic mathematics course',
            credits=3,
            is_core=True
        )
    
    def test_subject_creation(self):
        """Test subject creation."""
        self.assertEqual(self.subject.name, 'Mathematics')
        self.assertEqual(self.subject.code, 'MATH101')
        self.assertEqual(self.subject.credits, 3)
        self.assertTrue(self.subject.is_core)
    
    def test_subject_str_representation(self):
        """Test string representation of subject."""
        expected = f"{self.subject.name} ({self.subject.code})"
        self.assertEqual(str(self.subject), expected)


class FeeStructureModelTest(TestCase):
    """Test cases for FeeStructure model."""
    
    def setUp(self):
        """Set up test data."""
        # Create course first
        self.course = Course.objects.create(
            name='Test Course',
            code='TC001',
            description='Test course',
            tuition_fee=Decimal('15000.00'),
            currency='USD'
        )
        
        self.fee_structure = FeeStructure.objects.create(
            course=self.course,
            tuition_fee=Decimal('15000.00'),
            accommodation_fee=Decimal('5000.00'),
            meal_plan_fee=Decimal('3000.00'),
            transportation_fee=Decimal('1000.00'),
            health_insurance_fee=Decimal('800.00'),
            books_materials_fee=Decimal('500.00'),
            other_fees=Decimal('200.00'),
            currency='USD',
            payment_terms='Payment in installments'
        )
    
    def test_fee_structure_creation(self):
        """Test fee structure creation."""
        self.assertEqual(self.fee_structure.course, self.course)
        self.assertEqual(self.fee_structure.tuition_fee, Decimal('15000.00'))
        self.assertEqual(self.fee_structure.currency, 'USD')
    
    def test_total_fees_calculation(self):
        """Test total fees calculation."""
        expected_total = (15000 + 5000 + 3000 + 1000 + 800 + 500 + 200)
        self.assertEqual(self.fee_structure.total_fees, Decimal(str(expected_total)))
    
    def test_fee_structure_str_representation(self):
        """Test string representation of fee structure."""
        expected = f"Fee Structure - {self.course.name}"
        self.assertEqual(str(self.fee_structure), expected)


class CourseRequirementModelTest(TestCase):
    """Test cases for CourseRequirement model."""
    
    def setUp(self):
        """Set up test data."""
        self.course = Course.objects.create(
            name='Test Course',
            code='TC001',
            description='Test course',
            tuition_fee=Decimal('15000.00')
        )
        
        self.requirement = CourseRequirement.objects.create(
            course=self.course,
            requirement_type='academic',
            title='High School Diploma',
            description='Must have completed high school',
            is_mandatory=True,
            order=1
        )
    
    def test_requirement_creation(self):
        """Test requirement creation."""
        self.assertEqual(self.requirement.course, self.course)
        self.assertEqual(self.requirement.requirement_type, 'academic')
        self.assertEqual(self.requirement.title, 'High School Diploma')
        self.assertTrue(self.requirement.is_mandatory)
        self.assertEqual(self.requirement.order, 1)
    
    def test_requirement_str_representation(self):
        """Test string representation of requirement."""
        expected = f"{self.requirement.title} - {self.course.name}"
        self.assertEqual(str(self.requirement), expected)


class CourseApplicationModelTest(TestCase):
    """Test cases for CourseApplication model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.course = Course.objects.create(
            name='Test Course',
            code='TC001',
            description='Test course',
            tuition_fee=Decimal('15000.00')
        )
        
        self.application = CourseApplication.objects.create(
            user=self.user,
            course=self.course,
            status='submitted',
            personal_statement='I am interested in this course',
            expected_start_date='2024-09-01'
        )
    
    def test_application_creation(self):
        """Test application creation."""
        self.assertEqual(self.application.user, self.user)
        self.assertEqual(self.application.course, self.course)
        self.assertEqual(self.application.status, 'submitted')
        self.assertEqual(self.application.personal_statement, 'I am interested in this course')
    
    def test_application_str_representation(self):
        """Test string representation of application."""
        expected = f"{self.user.username} - {self.course.name} (submitted)"
        self.assertEqual(str(self.application), expected)


class CourseRatingModelTest(TestCase):
    """Test cases for CourseRating model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.course = Course.objects.create(
            name='Test Course',
            code='TC001',
            description='Test course',
            tuition_fee=Decimal('15000.00')
        )
        
        self.rating = CourseRating.objects.create(
            user=self.user,
            course=self.course,
            rating=4,
            review='Great course!',
            is_verified=False
        )
    
    def test_rating_creation(self):
        """Test rating creation."""
        self.assertEqual(self.rating.user, self.user)
        self.assertEqual(self.rating.course, self.course)
        self.assertEqual(self.rating.rating, 4)
        self.assertEqual(self.rating.review, 'Great course!')
        self.assertFalse(self.rating.is_verified)
    
    def test_rating_str_representation(self):
        """Test string representation of rating."""
        expected = f"{self.user.username} - {self.course.name} (4/5)"
        self.assertEqual(str(self.rating), expected)


class CourseAPITest(APITestCase):
    """Test cases for Course API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test course
        self.course = Course.objects.create(
            name='Test Course',
            code='TC001',
            description='Test course description',
            short_description='Short test description',
            level='undergraduate',
            duration='4_years',
            credits=120,
            tuition_fee=Decimal('15000.00'),
            currency='USD',
            status='active',
            is_featured=True
        )
    
    def test_course_list_endpoint(self):
        """Test course list endpoint."""
        url = reverse('courses-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_course_detail_endpoint(self):
        """Test course detail endpoint."""
        url = reverse('courses-detail', args=[self.course.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Course')
        self.assertEqual(response.data['code'], 'TC001')
    
    def test_course_search_endpoint(self):
        """Test course search endpoint."""
        url = reverse('courses-search')
        response = self.client.get(url, {'query': 'Test'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
    
    def test_course_filter_endpoint(self):
        """Test course filter endpoint."""
        url = reverse('courses-filter')
        data = {
            'levels': ['undergraduate'],
            'featured_only': True
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
    
    def test_course_application_endpoint(self):
        """Test course application endpoint."""
        self.client.force_authenticate(user=self.user)
        url = reverse('courses-apply', args=[self.course.id])
        data = {
            'personal_statement': 'I am interested in this course',
            'expected_start_date': '2024-09-01'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('success', response.data)
        self.assertTrue(response.data['success'])
    
    def test_course_rating_endpoint(self):
        """Test course rating endpoint."""
        self.client.force_authenticate(user=self.user)
        url = reverse('courses-rate', args=[self.course.id])
        data = {
            'rating': 4,
            'review': 'Great course!'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('success', response.data)
        self.assertTrue(response.data['success'])
    
    def test_course_stats_endpoint(self):
        """Test course stats endpoint."""
        url = reverse('courses-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('total_courses', response.data['data'])


class SubjectAPITest(APITestCase):
    """Test cases for Subject API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.subject = Subject.objects.create(
            name='Mathematics',
            code='MATH101',
            description='Basic mathematics course',
            credits=3,
            is_core=True
        )
    
    def test_subject_list_endpoint(self):
        """Test subject list endpoint."""
        url = reverse('subjects-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_subject_detail_endpoint(self):
        """Test subject detail endpoint."""
        url = reverse('subjects-detail', args=[self.subject.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Mathematics')
        self.assertEqual(response.data['code'], 'MATH101')


class CourseApplicationAPITest(APITestCase):
    """Test cases for CourseApplication API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.course = Course.objects.create(
            name='Test Course',
            code='TC001',
            description='Test course',
            tuition_fee=Decimal('15000.00')
        )
        
        self.application = CourseApplication.objects.create(
            user=self.user,
            course=self.course,
            status='submitted',
            personal_statement='I am interested in this course'
        )
    
    def test_application_list_endpoint(self):
        """Test application list endpoint."""
        self.client.force_authenticate(user=self.user)
        url = reverse('applications-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_application_detail_endpoint(self):
        """Test application detail endpoint."""
        self.client.force_authenticate(user=self.user)
        url = reverse('applications-detail', args=[self.application.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['course_name'], 'Test Course')
        self.assertEqual(response.data['status'], 'submitted')
