"""
Tests for universities app.
Comprehensive test suite for university models, serializers, and views.
"""

import logging
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import (
    University, Campus, UniversityRanking, UniversityProgram,
    UniversityFaculty, UniversityResearch, UniversityPartnership
)
from .serializers import (
    UniversitySerializer, UniversityCreateSerializer, CampusSerializer,
    UniversityRankingSerializer, UniversityProgramSerializer
)

logger = logging.getLogger(__name__)


class UniversityModelTest(TestCase):
    """Test cases for University models."""
    
    def setUp(self):
        """Set up test data."""
        self.university = University.objects.create(
            name='Test University',
            short_name='TU',
            slug='test-university',
            description='A test university for testing purposes',
            university_type='public',
            founded_year=1950,
            country='Test Country',
            city='Test City',
            total_students=10000,
            international_students=1000,
            faculty_count=500
        )
    
    def test_university_creation(self):
        """Test university creation."""
        print("Testing university creation")
        self.assertEqual(self.university.name, 'Test University')
        self.assertEqual(self.university.short_name, 'TU')
        self.assertEqual(self.university.university_type, 'public')
        self.assertEqual(self.university.founded_year, 1950)
    
    def test_university_age_calculation(self):
        """Test university age calculation."""
        print("Testing university age calculation")
        self.assertIsNotNone(self.university.age)
        self.assertTrue(self.university.age > 0)
    
    def test_international_student_percentage(self):
        """Test international student percentage calculation."""
        print("Testing international student percentage")
        self.assertEqual(self.university.international_student_percentage, 10.0)
    
    def test_campus_creation(self):
        """Test campus creation."""
        print("Testing campus creation")
        campus = Campus.objects.create(
            university=self.university,
            name='Main Campus',
            campus_type='main',
            address='123 Test Street',
            city='Test City',
            country='Test Country',
            is_main_campus=True
        )
        self.assertEqual(campus.university, self.university)
        self.assertEqual(campus.name, 'Main Campus')
        self.assertTrue(campus.is_main_campus)
    
    def test_university_ranking_creation(self):
        """Test university ranking creation."""
        print("Testing university ranking creation")
        ranking = UniversityRanking.objects.create(
            university=self.university,
            ranking_type='world',
            ranking_source='Test Rankings',
            rank=100,
            year=2023,
            score=85.5
        )
        self.assertEqual(ranking.university, self.university)
        self.assertEqual(ranking.ranking_type, 'world')
        self.assertEqual(ranking.rank, 100)
    
    def test_university_program_creation(self):
        """Test university program creation."""
        print("Testing university program creation")
        program = UniversityProgram.objects.create(
            university=self.university,
            name='Computer Science',
            program_level='undergraduate',
            program_type='full_time',
            duration_years=4,
            total_credits=120
        )
        self.assertEqual(program.university, self.university)
        self.assertEqual(program.name, 'Computer Science')
        self.assertEqual(program.program_level, 'undergraduate')
    
    def test_university_faculty_creation(self):
        """Test university faculty creation."""
        print("Testing university faculty creation")
        faculty = UniversityFaculty.objects.create(
            university=self.university,
            name='Faculty of Engineering',
            short_name='FE',
            student_count=2000,
            faculty_count=100
        )
        self.assertEqual(faculty.university, self.university)
        self.assertEqual(faculty.name, 'Faculty of Engineering')
        self.assertEqual(faculty.student_count, 2000)
    
    def test_university_research_creation(self):
        """Test university research creation."""
        print("Testing university research creation")
        research = UniversityResearch.objects.create(
            university=self.university,
            title='AI Research Project',
            research_area='technology',
            description='Research on artificial intelligence',
            start_date='2023-01-01',
            status='ongoing'
        )
        self.assertEqual(research.university, self.university)
        self.assertEqual(research.title, 'AI Research Project')
        self.assertEqual(research.research_area, 'technology')
    
    def test_university_partnership_creation(self):
        """Test university partnership creation."""
        print("Testing university partnership creation")
        partnership = UniversityPartnership.objects.create(
            university=self.university,
            partner_name='Partner University',
            partnership_type='academic',
            description='Academic partnership',
            start_date='2023-01-01',
            status='active'
        )
        self.assertEqual(partnership.university, self.university)
        self.assertEqual(partnership.partner_name, 'Partner University')
        self.assertEqual(partnership.partnership_type, 'academic')


class UniversitySerializerTest(TestCase):
    """Test cases for University serializers."""
    
    def setUp(self):
        """Set up test data."""
        self.university = University.objects.create(
            name='Test University',
            short_name='TU',
            slug='test-university',
            description='A test university',
            university_type='public',
            founded_year=1950,
            country='Test Country',
            city='Test City'
        )
    
    def test_university_serializer(self):
        """Test UniversitySerializer."""
        print("Testing UniversitySerializer")
        serializer = UniversitySerializer(self.university)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Test University')
        self.assertEqual(data['short_name'], 'TU')
        self.assertEqual(data['university_type'], 'public')
        self.assertEqual(data['country'], 'Test Country')
        self.assertIn('age', data)
    
    def test_university_create_serializer(self):
        """Test UniversityCreateSerializer."""
        print("Testing UniversityCreateSerializer")
        data = {
            'name': 'New University',
            'short_name': 'NU',
            'slug': 'new-university',
            'description': 'A new university',
            'university_type': 'private',
            'founded_year': 2000,
            'country': 'New Country',
            'city': 'New City'
        }
        serializer = UniversityCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        university = serializer.save()
        self.assertEqual(university.name, 'New University')
        self.assertEqual(university.slug, 'new-university')
    
    def test_campus_serializer(self):
        """Test CampusSerializer."""
        print("Testing CampusSerializer")
        campus = Campus.objects.create(
            university=self.university,
            name='Main Campus',
            campus_type='main',
            address='123 Test Street',
            city='Test City',
            country='Test Country'
        )
        serializer = CampusSerializer(campus)
        data = serializer.data
        
        self.assertEqual(data['university_name'], 'Test University')
        self.assertEqual(data['name'], 'Main Campus')
        self.assertEqual(data['campus_type'], 'main')
    
    def test_university_ranking_serializer(self):
        """Test UniversityRankingSerializer."""
        print("Testing UniversityRankingSerializer")
        ranking = UniversityRanking.objects.create(
            university=self.university,
            ranking_type='world',
            ranking_source='Test Rankings',
            rank=100,
            year=2023
        )
        serializer = UniversityRankingSerializer(ranking)
        data = serializer.data
        
        self.assertEqual(data['university_name'], 'Test University')
        self.assertEqual(data['ranking_type'], 'world')
        self.assertEqual(data['rank'], 100)
        self.assertEqual(data['year'], 2023)
    
    def test_university_program_serializer(self):
        """Test UniversityProgramSerializer."""
        print("Testing UniversityProgramSerializer")
        program = UniversityProgram.objects.create(
            university=self.university,
            name='Computer Science',
            program_level='undergraduate',
            program_type='full_time',
            duration_years=4
        )
        serializer = UniversityProgramSerializer(program)
        data = serializer.data
        
        self.assertEqual(data['university_name'], 'Test University')
        self.assertEqual(data['name'], 'Computer Science')
        self.assertEqual(data['program_level'], 'undergraduate')
        self.assertEqual(data['duration_years'], 4)


class UniversityAPITest(APITestCase):
    """Test cases for University API endpoints."""
    
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
        
        self.university = University.objects.create(
            name='Test University',
            short_name='TU',
            slug='test-university',
            description='A test university',
            university_type='public',
            founded_year=1950,
            country='Test Country',
            city='Test City'
        )
    
    def test_university_list(self):
        """Test university list endpoint."""
        print("Testing university list endpoint")
        url = reverse('university-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_university_detail(self):
        """Test university detail endpoint."""
        print("Testing university detail endpoint")
        url = reverse('university-detail', args=[self.university.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test University')
        self.assertEqual(response.data['short_name'], 'TU')
    
    def test_university_create(self):
        """Test university creation endpoint."""
        print("Testing university creation endpoint")
        url = reverse('university-list')
        data = {
            'name': 'New University',
            'short_name': 'NU',
            'slug': 'new-university',
            'description': 'A new university',
            'university_type': 'private',
            'founded_year': 2000,
            'country': 'New Country',
            'city': 'New City'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], 'New University')
    
    def test_university_search(self):
        """Test university search endpoint."""
        print("Testing university search endpoint")
        url = reverse('university-search')
        data = {
            'query': 'Test',
            'country': 'Test Country'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
    
    def test_university_stats(self):
        """Test university statistics endpoint."""
        print("Testing university statistics endpoint")
        url = reverse('university-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_universities', response.data['data'])
        self.assertIn('active_universities', response.data['data'])
    
    def test_university_compare(self):
        """Test university comparison endpoint."""
        print("Testing university comparison endpoint")
        # Create another university for comparison
        university2 = University.objects.create(
            name='Test University 2',
            short_name='TU2',
            slug='test-university-2',
            university_type='private',
            country='Test Country',
            city='Test City 2'
        )
        
        url = reverse('university-compare')
        data = {
            'university_ids': [self.university.id, university2.id]
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('universities', response.data['data'])
    
    def test_university_rankings(self):
        """Test university rankings endpoint."""
        print("Testing university rankings endpoint")
        # Create a ranking
        UniversityRanking.objects.create(
            university=self.university,
            ranking_type='world',
            ranking_source='Test Rankings',
            rank=100,
            year=2023
        )
        
        url = reverse('university-rankings', args=[self.university.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
    
    def test_university_programs(self):
        """Test university programs endpoint."""
        print("Testing university programs endpoint")
        # Create a program
        UniversityProgram.objects.create(
            university=self.university,
            name='Computer Science',
            program_level='undergraduate',
            program_type='full_time',
            duration_years=4
        )
        
        url = reverse('university-programs', args=[self.university.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
    
    def test_campus_list(self):
        """Test campus list endpoint."""
        print("Testing campus list endpoint")
        Campus.objects.create(
            university=self.university,
            name='Main Campus',
            campus_type='main',
            address='123 Test Street',
            city='Test City',
            country='Test Country'
        )
        
        url = reverse('campus-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_ranking_list(self):
        """Test ranking list endpoint."""
        print("Testing ranking list endpoint")
        UniversityRanking.objects.create(
            university=self.university,
            ranking_type='world',
            ranking_source='Test Rankings',
            rank=100,
            year=2023
        )
        
        url = reverse('ranking-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_program_list(self):
        """Test program list endpoint."""
        print("Testing program list endpoint")
        UniversityProgram.objects.create(
            university=self.university,
            name='Computer Science',
            program_level='undergraduate',
            program_type='full_time',
            duration_years=4
        )
        
        url = reverse('program-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)


class UniversityIntegrationTest(TestCase):
    """Integration tests for university functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.university = University.objects.create(
            name='Test University',
            short_name='TU',
            slug='test-university',
            university_type='public',
            country='Test Country',
            city='Test City'
        )
    
    def test_university_with_campus_and_programs(self):
        """Test university with campus and programs."""
        print("Testing university with campus and programs")
        
        # Create campus
        campus = Campus.objects.create(
            university=self.university,
            name='Main Campus',
            campus_type='main',
            address='123 Test Street',
            city='Test City',
            country='Test Country'
        )
        
        # Create program
        program = UniversityProgram.objects.create(
            university=self.university,
            name='Computer Science',
            program_level='undergraduate',
            program_type='full_time',
            duration_years=4
        )
        
        # Create ranking
        ranking = UniversityRanking.objects.create(
            university=self.university,
            ranking_type='world',
            ranking_source='Test Rankings',
            rank=100,
            year=2023
        )
        
        # Test relationships
        self.assertEqual(self.university.campuses.count(), 1)
        self.assertEqual(self.university.programs.count(), 1)
        self.assertEqual(self.university.rankings.count(), 1)
        
        self.assertEqual(campus.university, self.university)
        self.assertEqual(program.university, self.university)
        self.assertEqual(ranking.university, self.university)
    
    def test_university_search_functionality(self):
        """Test university search functionality."""
        print("Testing university search functionality")
        
        # Create multiple universities
        University.objects.create(
            name='Engineering University',
            short_name='EU',
            slug='engineering-university',
            university_type='technical',
            country='Test Country',
            city='Test City'
        )
        
        University.objects.create(
            name='Medical University',
            short_name='MU',
            slug='medical-university',
            university_type='medical',
            country='Test Country',
            city='Test City'
        )
        
        # Test search by name
        results = University.objects.filter(name__icontains='Engineering')
        self.assertEqual(results.count(), 1)
        
        # Test search by type
        results = University.objects.filter(university_type='medical')
        self.assertEqual(results.count(), 1)
        
        # Test search by country
        results = University.objects.filter(country='Test Country')
        self.assertEqual(results.count(), 3)


class UniversityPerformanceTest(TestCase):
    """Performance tests for university functionality."""
    
    def setUp(self):
        """Set up test data."""
        # Create multiple universities for performance testing
        for i in range(100):
            University.objects.create(
                name=f'University {i}',
                short_name=f'U{i}',
                slug=f'university-{i}',
                university_type='public' if i % 2 == 0 else 'private',
                country=f'Country {i % 10}',
                city=f'City {i}',
                total_students=1000 + i * 100,
                international_students=100 + i * 10
            )
    
    def test_university_list_performance(self):
        """Test university list endpoint performance."""
        print("Testing university list performance")
        
        api_client = APIClient()
        url = reverse('university-list')
        
        import time
        start_time = time.time()
        response = api_client.get(url)
        end_time = time.time()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(end_time - start_time, 1.0)  # Should complete within 1 second
    
    def test_university_search_performance(self):
        """Test university search performance."""
        print("Testing university search performance")
        
        api_client = APIClient()
        url = reverse('university-search')
        
        import time
        start_time = time.time()
        response = api_client.post(url, {'query': 'University'}, format='json')
        end_time = time.time()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(end_time - start_time, 1.0)  # Should complete within 1 second


if __name__ == '__main__':
    # Run tests with verbose output
    import django
    django.setup()
    
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'test', 'universities', '--verbosity=2'])
