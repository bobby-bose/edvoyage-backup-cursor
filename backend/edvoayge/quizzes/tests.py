from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import (
    Quiz, QuizCategory, Question, Option, QuizAttempt, 
    QuizResult, QuizAnalytics, QuizShare, QuizTimer
)
from .serializers import (
    QuizSerializer, QuizListSerializer, QuizCreateSerializer,
    QuizCategorySerializer, QuestionSerializer, OptionSerializer
)
import json
from datetime import datetime, timedelta
from decimal import Decimal

User = get_user_model()

class QuizCategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_category_creation(self):
        """Test quiz category creation"""
        category = QuizCategory.objects.create(
            name='Test Category',
            description='Test Description',
            color='#FF5733',
            icon='test-icon'
        )
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.description, 'Test Description')
        self.assertEqual(category.color, '#FF5733')
        self.assertEqual(category.icon, 'test-icon')
        self.assertTrue(category.is_active)

    def test_category_str_representation(self):
        """Test category string representation"""
        category = QuizCategory.objects.create(name='Test Category')
        self.assertEqual(str(category), 'Test Category')

    def test_category_quiz_count(self):
        """Test category quiz count property"""
        category = QuizCategory.objects.create(name='Test Category')
        quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test Description',
            category=category,
            creator=self.user
        )
        self.assertEqual(category.quiz_count, 1)

class QuizModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = QuizCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )

    def test_quiz_creation(self):
        """Test quiz creation with all required fields"""
        quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test Description',
            category=self.category,
            creator=self.user,
            time_limit=30,
            passing_score=70,
            max_attempts=3,
            difficulty='medium',
            status='draft',
            is_public=False,
            is_featured=False
        )
        self.assertEqual(quiz.title, 'Test Quiz')
        self.assertEqual(quiz.category, self.category)
        self.assertEqual(quiz.creator, self.user)
        self.assertEqual(quiz.time_limit, 30)
        self.assertEqual(quiz.passing_score, 70)
        self.assertEqual(quiz.max_attempts, 3)
        self.assertEqual(quiz.difficulty, 'medium')
        self.assertEqual(quiz.status, 'draft')
        self.assertFalse(quiz.is_public)
        self.assertFalse(quiz.is_featured)

    def test_quiz_str_representation(self):
        """Test quiz string representation"""
        quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test Description',
            category=self.category,
            creator=self.user
        )
        self.assertEqual(str(quiz), 'Test Quiz')

    def test_quiz_question_count(self):
        """Test quiz question count property"""
        quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test Description',
            category=self.category,
            creator=self.user
        )
        question = Question.objects.create(
            quiz=quiz,
            question_text='Test Question',
            question_type='multiple_choice',
            points=1
        )
        self.assertEqual(quiz.question_count, 1)

    def test_quiz_is_active(self):
        """Test quiz is_active property"""
        quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test Description',
            category=self.category,
            creator=self.user,
            status='published',
            is_public=True
        )
        self.assertTrue(quiz.is_active)

    def test_quiz_publish(self):
        """Test quiz publishing sets published_at"""
        quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test Description',
            category=self.category,
            creator=self.user,
            status='draft'
        )
        self.assertIsNone(quiz.published_at)
        
        quiz.status = 'published'
        quiz.save()
        self.assertIsNotNone(quiz.published_at)

class QuestionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = QuizCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )
        self.quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test Description',
            category=self.category,
            creator=self.user
        )

    def test_question_creation(self):
        """Test question creation"""
        question = Question.objects.create(
            quiz=self.quiz,
            question_text='What is 2 + 2?',
            question_type='multiple_choice',
            points=1,
            order=1,
            explanation='Basic arithmetic'
        )
        self.assertEqual(question.quiz, self.quiz)
        self.assertEqual(question.question_text, 'What is 2 + 2?')
        self.assertEqual(question.question_type, 'multiple_choice')
        self.assertEqual(question.points, 1)
        self.assertEqual(question.order, 1)
        self.assertEqual(question.explanation, 'Basic arithmetic')
        self.assertTrue(question.is_active)

    def test_question_str_representation(self):
        """Test question string representation"""
        question = Question.objects.create(
            quiz=self.quiz,
            question_text='What is 2 + 2?',
            question_type='multiple_choice'
        )
        self.assertEqual(str(question), f'{self.quiz.title} - What is 2 + 2?')

    def test_question_correct_options(self):
        """Test question correct options property"""
        question = Question.objects.create(
            quiz=self.quiz,
            question_text='What is 2 + 2?',
            question_type='multiple_choice'
        )
        correct_option = Option.objects.create(
            question=question,
            option_text='4',
            is_correct=True
        )
        wrong_option = Option.objects.create(
            question=question,
            option_text='3',
            is_correct=False
        )
        correct_options = question.correct_options
        self.assertIn(correct_option, correct_options)
        self.assertNotIn(wrong_option, correct_options)

class OptionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = QuizCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )
        self.quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test Description',
            category=self.category,
            creator=self.user
        )
        self.question = Question.objects.create(
            quiz=self.quiz,
            question_text='What is 2 + 2?',
            question_type='multiple_choice'
        )

    def test_option_creation(self):
        """Test option creation"""
        option = Option.objects.create(
            question=self.question,
            option_text='4',
            is_correct=True,
            order=1
        )
        self.assertEqual(option.question, self.question)
        self.assertEqual(option.option_text, '4')
        self.assertTrue(option.is_correct)
        self.assertEqual(option.order, 1)

    def test_option_str_representation(self):
        """Test option string representation"""
        option = Option.objects.create(
            question=self.question,
            option_text='4',
            is_correct=True
        )
        self.assertEqual(str(option), f'{self.question.question_text[:30]} - 4')

class QuizAttemptModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = QuizCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )
        self.quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test Description',
            category=self.category,
            creator=self.user
        )

    def test_attempt_creation(self):
        """Test quiz attempt creation"""
        attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            user=self.user,
            status='in_progress'
        )
        self.assertEqual(attempt.quiz, self.quiz)
        self.assertEqual(attempt.user, self.user)
        self.assertEqual(attempt.status, 'in_progress')
        self.assertIsNone(attempt.score)
        self.assertIsNone(attempt.percentage)
        self.assertIsNone(attempt.passed)

    def test_attempt_str_representation(self):
        """Test attempt string representation"""
        attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            user=self.user,
            status='in_progress'
        )
        self.assertEqual(str(attempt), f'{self.user.username} - {self.quiz.title} (in_progress)')

    def test_attempt_completion(self):
        """Test attempt completion sets completed_at"""
        attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            user=self.user,
            status='in_progress'
        )
        self.assertIsNone(attempt.completed_at)
        
        attempt.status = 'completed'
        attempt.save()
        self.assertIsNotNone(attempt.completed_at)

    def test_attempt_is_passed(self):
        """Test attempt is_passed property"""
        self.quiz.passing_score = 70
        self.quiz.save()
        
        attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            user=self.user,
            status='completed',
            percentage=Decimal('75.0')
        )
        self.assertTrue(attempt.is_passed)

class QuizResultModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = QuizCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )
        self.quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test Description',
            category=self.category,
            creator=self.user
        )
        self.question = Question.objects.create(
            quiz=self.quiz,
            question_text='What is 2 + 2?',
            question_type='multiple_choice'
        )
        self.attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            user=self.user,
            status='completed'
        )

    def test_result_creation(self):
        """Test quiz result creation"""
        result = QuizResult.objects.create(
            attempt=self.attempt,
            question=self.question,
            user_answer='4',
            is_correct=True,
            points_earned=1
        )
        self.assertEqual(result.attempt, self.attempt)
        self.assertEqual(result.question, self.question)
        self.assertEqual(result.user_answer, '4')
        self.assertTrue(result.is_correct)
        self.assertEqual(result.points_earned, 1)

    def test_result_str_representation(self):
        """Test result string representation"""
        result = QuizResult.objects.create(
            attempt=self.attempt,
            question=self.question,
            user_answer='4',
            is_correct=True
        )
        self.assertEqual(str(result), f'{self.user.username} - {self.question.question_text[:30]}')

class QuizAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = QuizCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )
        self.quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test Description',
            category=self.category,
            creator=self.user,
            status='published',
            is_public=True
        )
        self.client.force_authenticate(user=self.user)

    def test_get_quizzes_list(self):
        """Test getting list of quizzes"""
        url = reverse('quiz-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_quiz_detail(self):
        """Test getting quiz detail"""
        url = reverse('quiz-detail', args=[self.quiz.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Quiz')

    def test_create_quiz(self):
        """Test creating a new quiz"""
        url = reverse('quiz-list')
        data = {
            'title': 'New Quiz',
            'description': 'New Description',
            'category_id': self.category.id,
            'time_limit': 30,
            'passing_score': 70,
            'max_attempts': 3,
            'difficulty': 'medium',
            'status': 'draft',
            'is_public': False,
            'is_featured': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 2)

    def test_update_quiz(self):
        """Test updating a quiz"""
        url = reverse('quiz-detail', args=[self.quiz.id])
        data = {
            'title': 'Updated Quiz',
            'description': 'Updated Description',
            'category_id': self.category.id,
            'time_limit': 45,
            'passing_score': 80,
            'max_attempts': 5,
            'difficulty': 'hard',
            'status': 'published',
            'is_public': True,
            'is_featured': True
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.title, 'Updated Quiz')

    def test_delete_quiz(self):
        """Test deleting a quiz"""
        url = reverse('quiz-detail', args=[self.quiz.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Quiz.objects.count(), 0)

    def test_start_quiz(self):
        """Test starting a quiz attempt"""
        url = reverse('quiz-start', args=[self.quiz.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(QuizAttempt.objects.count(), 1)

    def test_search_quizzes(self):
        """Test searching quizzes"""
        url = reverse('quiz-search')
        response = self.client.get(url, {'q': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_quiz_statistics(self):
        """Test getting quiz statistics"""
        url = reverse('quiz-statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_quizzes', response.data)

    def test_featured_quizzes(self):
        """Test getting featured quizzes"""
        url = reverse('quiz-featured')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recent_quizzes(self):
        """Test getting recent quizzes"""
        url = reverse('quiz-recent')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_popular_quizzes(self):
        """Test getting popular quizzes"""
        url = reverse('quiz-popular')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class QuizCategoryAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = QuizCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_categories_list(self):
        """Test getting list of categories"""
        url = reverse('quiz-category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_category_detail(self):
        """Test getting category detail"""
        url = reverse('quiz-category-detail', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Category')

    def test_create_category(self):
        """Test creating a new category"""
        url = reverse('quiz-category-list')
        data = {
            'name': 'New Category',
            'description': 'New Description',
            'color': '#33FF57',
            'icon': 'new-icon',
            'is_active': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(QuizCategory.objects.count(), 2)

    def test_update_category(self):
        """Test updating a category"""
        url = reverse('quiz-category-detail', args=[self.category.id])
        data = {
            'name': 'Updated Category',
            'description': 'Updated Description',
            'color': '#FF3357',
            'icon': 'updated-icon',
            'is_active': True
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')

    def test_delete_category(self):
        """Test deleting a category"""
        url = reverse('quiz-category-detail', args=[self.category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(QuizCategory.objects.count(), 0)

    def test_category_quizzes(self):
        """Test getting quizzes in a category"""
        url = reverse('category-quizzes', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_statistics(self):
        """Test getting category statistics"""
        url = reverse('category-statistics', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class QuestionAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = QuizCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )
        self.quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test Description',
            category=self.category,
            creator=self.user
        )
        self.question = Question.objects.create(
            quiz=self.quiz,
            question_text='What is 2 + 2?',
            question_type='multiple_choice',
            points=1
        )
        self.client.force_authenticate(user=self.user)

    def test_get_questions_list(self):
        """Test getting list of questions"""
        url = reverse('question-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_question_detail(self):
        """Test getting question detail"""
        url = reverse('question-detail', args=[self.question.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question_text'], 'What is 2 + 2?')

    def test_create_question(self):
        """Test creating a new question"""
        url = reverse('question-list')
        data = {
            'quiz': self.quiz.id,
            'question_text': 'What is 3 + 3?',
            'question_type': 'multiple_choice',
            'points': 2,
            'order': 2,
            'explanation': 'Basic arithmetic',
            'is_active': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)

    def test_update_question(self):
        """Test updating a question"""
        url = reverse('question-detail', args=[self.question.id])
        data = {
            'quiz': self.quiz.id,
            'question_text': 'Updated question text',
            'question_type': 'true_false',
            'points': 3,
            'order': 1,
            'explanation': 'Updated explanation',
            'is_active': True
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.question.refresh_from_db()
        self.assertEqual(self.question.question_text, 'Updated question text')

    def test_delete_question(self):
        """Test deleting a question"""
        url = reverse('question-detail', args=[self.question.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.count(), 0)

class OptionAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = QuizCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )
        self.quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test Description',
            category=self.category,
            creator=self.user
        )
        self.question = Question.objects.create(
            quiz=self.quiz,
            question_text='What is 2 + 2?',
            question_type='multiple_choice'
        )
        self.option = Option.objects.create(
            question=self.question,
            option_text='4',
            is_correct=True,
            order=1
        )
        self.client.force_authenticate(user=self.user)

    def test_get_options_list(self):
        """Test getting list of options"""
        url = reverse('option-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_option_detail(self):
        """Test getting option detail"""
        url = reverse('option-detail', args=[self.option.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['option_text'], '4')

    def test_create_option(self):
        """Test creating a new option"""
        url = reverse('option-list')
        data = {
            'question': self.question.id,
            'option_text': '5',
            'is_correct': False,
            'order': 2
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Option.objects.count(), 2)

    def test_update_option(self):
        """Test updating an option"""
        url = reverse('option-detail', args=[self.option.id])
        data = {
            'question': self.question.id,
            'option_text': 'Updated option',
            'is_correct': False,
            'order': 3
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.option.refresh_from_db()
        self.assertEqual(self.option.option_text, 'Updated option')

    def test_delete_option(self):
        """Test deleting an option"""
        url = reverse('option-detail', args=[self.option.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Option.objects.count(), 0)

class QuizSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = QuizCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )
        self.quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test Description',
            category=self.category,
            creator=self.user
        )

    def test_quiz_serializer(self):
        """Test quiz serializer"""
        serializer = QuizSerializer(self.quiz)
        data = serializer.data
        self.assertEqual(data['title'], 'Test Quiz')
        self.assertEqual(data['description'], 'Test Description')
        self.assertEqual(data['category']['name'], 'Test Category')

    def test_category_serializer(self):
        """Test category serializer"""
        serializer = QuizCategorySerializer(self.category)
        data = serializer.data
        self.assertEqual(data['name'], 'Test Category')
        self.assertEqual(data['color'], '#FF5733')

    def test_question_serializer(self):
        """Test question serializer"""
        question = Question.objects.create(
            quiz=self.quiz,
            question_text='What is 2 + 2?',
            question_type='multiple_choice'
        )
        serializer = QuestionSerializer(question)
        data = serializer.data
        self.assertEqual(data['question_text'], 'What is 2 + 2?')
        self.assertEqual(data['question_type'], 'multiple_choice')

    def test_option_serializer(self):
        """Test option serializer"""
        question = Question.objects.create(
            quiz=self.quiz,
            question_text='What is 2 + 2?',
            question_type='multiple_choice'
        )
        option = Option.objects.create(
            question=question,
            option_text='4',
            is_correct=True
        )
        serializer = OptionSerializer(option)
        data = serializer.data
        self.assertEqual(data['option_text'], '4')
        self.assertTrue(data['is_correct'])

class QuizIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = QuizCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )

    def test_quiz_workflow(self):
        """Test complete quiz workflow"""
        # Create quiz
        quiz = Quiz.objects.create(
            title='Integration Test Quiz',
            description='Integration Test Description',
            category=self.category,
            creator=self.user,
            status='published',
            is_public=True
        )
        
        # Create question
        question = Question.objects.create(
            quiz=quiz,
            question_text='What is 2 + 2?',
            question_type='multiple_choice',
            points=1
        )
        
        # Create options
        correct_option = Option.objects.create(
            question=question,
            option_text='4',
            is_correct=True,
            order=1
        )
        wrong_option = Option.objects.create(
            question=question,
            option_text='3',
            is_correct=False,
            order=2
        )
        
        # Create attempt
        attempt = QuizAttempt.objects.create(
            quiz=quiz,
            user=self.user,
            status='in_progress'
        )
        
        # Create result
        result = QuizResult.objects.create(
            attempt=attempt,
            question=question,
            user_answer='4',
            is_correct=True,
            points_earned=1
        )
        
        # Verify workflow
        self.assertEqual(Quiz.objects.count(), 1)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Option.objects.count(), 2)
        self.assertEqual(QuizAttempt.objects.count(), 1)
        self.assertEqual(QuizResult.objects.count(), 1)
        
        # Test relationships
        self.assertEqual(quiz.questions.first(), question)
        self.assertEqual(question.options.count(), 2)
        self.assertEqual(attempt.results.first(), result)

class QuizPerformanceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = QuizCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )

    def test_bulk_quiz_creation(self):
        """Test bulk quiz creation performance"""
        quizzes = []
        for i in range(100):
            quiz = Quiz(
                title=f'Quiz {i}',
                description=f'Description {i}',
                category=self.category,
                creator=self.user,
                status='draft'
            )
            quizzes.append(quiz)
        
        Quiz.objects.bulk_create(quizzes)
        self.assertEqual(Quiz.objects.count(), 100)

    def test_quiz_query_performance(self):
        """Test quiz query performance with select_related"""
        # Create multiple quizzes
        for i in range(50):
            Quiz.objects.create(
                title=f'Quiz {i}',
                description=f'Description {i}',
                category=self.category,
                creator=self.user,
                status='published'
            )
        
        # Test query performance
        with self.assertNumQueries(1):  # Should use select_related
            quizzes = Quiz.objects.select_related('category', 'creator').all()
            for quiz in quizzes:
                _ = quiz.category.name
                _ = quiz.creator.username
