from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg, Count, Sum
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import logging

from .models import (
    Quiz, QuizCategory, Question, Option, QuizAttempt, 
    QuizResult, QuizAnalytics, QuizShare, QuizTimer
)
from .serializers import (
    QuizSerializer, QuizListSerializer, QuizCreateSerializer, QuizUpdateSerializer,
    QuizCategorySerializer, QuizCategoryListSerializer,
    QuestionSerializer, QuestionListSerializer,
    OptionSerializer, OptionListSerializer,
    QuizAttemptSerializer, QuizAttemptCreateSerializer,
    QuizResultSerializer, QuizAnalyticsSerializer,
    QuizShareSerializer, QuizShareCreateSerializer,
    QuizTimerSerializer, QuizSearchSerializer,
    QuizStatisticsSerializer, QuizAttemptSubmitSerializer,
    QuizExportSerializer, QuizImportSerializer, QuizBulkActionSerializer
)

# Set up logging
logger = logging.getLogger(__name__)

class QuizCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for quiz categories"""
    queryset = QuizCategory.objects.all()
    serializer_class = QuizCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'quiz_count']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return QuizCategoryListSerializer
        return QuizCategorySerializer

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            # Show user's categories and public categories
            queryset = queryset.filter(
                Q(user=self.request.user) | Q(is_active=True)
            )
        else:
            # Show only public categories
            queryset = queryset.filter(is_active=True)
        return queryset.select_related('user').prefetch_related('quizzes')

    @action(detail=True, methods=['get'])
    def quizzes(self, request, pk=None):
        """Get quizzes in a category"""
        category = self.get_object()
        quizzes = category.quizzes.filter(is_active=True)
        
        # Apply pagination
        paginator = Paginator(quizzes, 25)
        page_number = request.query_params.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        serializer = QuizListSerializer(page_obj, many=True)
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'next': page_obj.has_next(),
            'previous': page_obj.has_previous(),
            'page': page_obj.number,
            'pages': paginator.num_pages
        })

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get category statistics"""
        category = self.get_object()
        quizzes = category.quizzes.all()
        
        stats = {
            'total_quizzes': quizzes.count(),
            'total_attempts': sum(quiz.total_attempts for quiz in quizzes),
            'average_score': quizzes.aggregate(avg=Avg('average_score'))['avg'] or 0,
            'completion_rate': quizzes.aggregate(avg=Avg('completion_rate'))['avg'] or 0,
        }
        
        return Response(stats)

    @action(detail=False, methods=['post'])
    def reorder(self, request):
        """Reorder categories"""
        category_ids = request.data.get('category_ids', [])
        
        for index, category_id in enumerate(category_ids):
            QuizCategory.objects.filter(id=category_id).update(order=index)
        
        return Response({'message': 'Categories reordered successfully'})

class QuizViewSet(viewsets.ModelViewSet):
    """ViewSet for quizzes"""
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'difficulty', 'is_public', 'is_featured', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'total_attempts', 'average_score']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return QuizListSerializer
        elif self.action == 'create':
            return QuizCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return QuizUpdateSerializer
        return QuizSerializer

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = super().get_queryset()
        
        # Apply filters
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        is_public = self.request.query_params.get('is_public')
        if is_public is not None:
            queryset = queryset.filter(is_public=is_public.lower() == 'true')
        
        is_featured = self.request.query_params.get('is_featured')
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')
        
        # Time limit filters
        time_limit_min = self.request.query_params.get('time_limit_min')
        if time_limit_min:
            queryset = queryset.filter(time_limit__gte=time_limit_min)
        
        time_limit_max = self.request.query_params.get('time_limit_max')
        if time_limit_max:
            queryset = queryset.filter(time_limit__lte=time_limit_max)
        
        if self.request.user.is_authenticated:
            # Show user's quizzes and public quizzes
            queryset = queryset.filter(
                Q(creator=self.request.user) | Q(is_public=True, status='published')
            )
        else:
            # Show only public published quizzes
            queryset = queryset.filter(is_public=True, status='published')
        
        return queryset.select_related('category', 'creator').prefetch_related('questions')

    def perform_create(self, serializer):
        """Create quiz with current user as creator"""
        serializer.save(creator=self.request.user)
        logger.info(f"Quiz created: {serializer.instance.title} by {self.request.user.username}")

    def perform_update(self, serializer):
        """Update quiz with logging"""
        old_title = self.get_object().title
        serializer.save()
        logger.info(f"Quiz updated: {old_title} -> {serializer.instance.title} by {self.request.user.username}")

    def perform_destroy(self, instance):
        """Delete quiz with logging"""
        title = instance.title
        super().perform_destroy(instance)
        logger.info(f"Quiz deleted: {title} by {self.request.user.username}")

    @action(detail=True, methods=['post'])
    def start_quiz(self, request, pk=None):
        """Start a quiz attempt"""
        quiz = self.get_object()
        
        # Check if user can attempt this quiz
        if not quiz.is_active:
            return Response(
                {'error': 'Quiz is not available'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check attempt limit
        attempts_count = QuizAttempt.objects.filter(quiz=quiz, user=request.user).count()
        if attempts_count >= quiz.max_attempts:
            return Response(
                {'error': f'Maximum attempts ({quiz.max_attempts}) reached'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create attempt
        attempt = QuizAttempt.objects.create(
            quiz=quiz,
            user=request.user,
            status='in_progress'
        )
        
        # Create timer if quiz has time limit
        if quiz.time_limit > 0:
            QuizTimer.objects.create(
                attempt=attempt,
                time_limit=quiz.time_limit * 60,  # Convert to seconds
                time_remaining=quiz.time_limit * 60
            )
        
        # Track analytics
        QuizAnalytics.objects.create(
            quiz=quiz,
            user=request.user,
            action_type='start',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        serializer = QuizAttemptSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def submit_quiz(self, request, pk=None):
        """Submit quiz answers"""
        quiz = self.get_object()
        answers = request.data.get('answers', {})
        
        # Get current attempt
        try:
            attempt = QuizAttempt.objects.get(
                quiz=quiz,
                user=request.user,
                status='in_progress'
            )
        except QuizAttempt.DoesNotExist:
            return Response(
                {'error': 'No active attempt found'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate results
        total_points = 0
        earned_points = 0
        questions_attempted = 0
        questions_correct = 0
        
        for question in quiz.questions.filter(is_active=True):
            total_points += question.points
            user_answer = answers.get(str(question.id))
            
            if user_answer is not None:
                questions_attempted += 1
                
                # Check if answer is correct
                correct_options = question.correct_options
                is_correct = False
                
                if question.question_type == 'multiple_choice':
                    # For multiple choice, check if user selected correct options
                    if isinstance(user_answer, list):
                        selected_options = set(user_answer)
                        correct_option_ids = set(correct_options.values_list('id', flat=True))
                        is_correct = selected_options == correct_option_ids
                    else:
                        # Single choice
                        is_correct = user_answer in correct_options.values_list('id', flat=True)
                elif question.question_type == 'true_false':
                    is_correct = str(user_answer).lower() == str(correct_options.first().option_text).lower()
                else:
                    # For other types, simple text comparison
                    correct_answer = correct_options.first().option_text if correct_options.exists() else ''
                    is_correct = str(user_answer).strip().lower() == correct_answer.strip().lower()
                
                if is_correct:
                    earned_points += question.points
                    questions_correct += 1
                
                # Create result record
                QuizResult.objects.create(
                    attempt=attempt,
                    question=question,
                    user_answer=str(user_answer),
                    is_correct=is_correct,
                    points_earned=question.points if is_correct else 0
                )
        
        # Calculate final score
        percentage = (earned_points / total_points * 100) if total_points > 0 else 0
        passed = percentage >= quiz.passing_score
        
        # Update attempt
        attempt.score = earned_points
        attempt.percentage = percentage
        attempt.passed = passed
        attempt.status = 'completed'
        attempt.questions_attempted = questions_attempted
        attempt.questions_correct = questions_correct
        attempt.answers = answers
        attempt.save()
        
        # Update quiz analytics
        quiz.total_attempts += 1
        quiz.average_score = (
            (quiz.average_score * (quiz.total_attempts - 1) + percentage) / quiz.total_attempts
        )
        quiz.save()
        
        # Track analytics
        QuizAnalytics.objects.create(
            quiz=quiz,
            user=request.user,
            action_type='complete',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        serializer = QuizAttemptSerializer(attempt)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get quiz results for current user"""
        quiz = self.get_object()
        attempts = QuizAttempt.objects.filter(
            quiz=quiz,
            user=request.user,
            status='completed'
        ).order_by('-completed_at')
        
        serializer = QuizAttemptSerializer(attempts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def leaderboard(self, request, pk=None):
        """Get quiz leaderboard"""
        quiz = self.get_object()
        attempts = QuizAttempt.objects.filter(
            quiz=quiz,
            status='completed'
        ).select_related('user').order_by('-percentage', 'time_taken')[:10]
        
        leaderboard_data = []
        for attempt in attempts:
            leaderboard_data.append({
                'user': {
                    'id': attempt.user.id,
                    'username': attempt.user.username,
                    'first_name': attempt.user.first_name,
                    'last_name': attempt.user.last_name
                },
                'percentage': attempt.percentage,
                'time_taken': attempt.time_taken,
                'completed_at': attempt.completed_at
            })
        
        return Response(leaderboard_data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search quizzes"""
        serializer = QuizSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        queryset = self.get_queryset()
        
        # Apply search filters
        q = serializer.validated_data.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | 
                Q(description__icontains=q) |
                Q(category__name__icontains=q)
            )
        
        category = serializer.validated_data.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        difficulty = serializer.validated_data.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        status_filter = serializer.validated_data.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        is_public = serializer.validated_data.get('is_public')
        if is_public is not None:
            queryset = queryset.filter(is_public=is_public)
        
        is_featured = serializer.validated_data.get('is_featured')
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured)
        
        time_limit_min = serializer.validated_data.get('time_limit_min')
        if time_limit_min:
            queryset = queryset.filter(time_limit__gte=time_limit_min)
        
        time_limit_max = serializer.validated_data.get('time_limit_max')
        if time_limit_max:
            queryset = queryset.filter(time_limit__lte=time_limit_max)
        
        # Apply pagination
        paginator = Paginator(queryset, 25)
        page_number = request.query_params.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        serializer = QuizListSerializer(page_obj, many=True)
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'next': page_obj.has_next(),
            'previous': page_obj.has_previous(),
            'page': page_obj.number,
            'pages': paginator.num_pages
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get overall quiz statistics"""
        queryset = self.get_queryset()
        
        stats = {
            'total_quizzes': queryset.count(),
            'total_attempts': queryset.aggregate(total=Sum('total_attempts'))['total'] or 0,
            'average_score': queryset.aggregate(avg=Avg('average_score'))['avg'] or 0,
            'completion_rate': queryset.aggregate(avg=Avg('completion_rate'))['avg'] or 0,
            'popular_quizzes': QuizListSerializer(
                queryset.order_by('-total_attempts')[:5], many=True
            ).data,
            'recent_quizzes': QuizListSerializer(
                queryset.order_by('-created_at')[:5], many=True
            ).data,
            'category_stats': []
        }
        
        # Category statistics
        categories = QuizCategory.objects.annotate(
            quiz_count=Count('quizzes'),
            total_attempts=Sum('quizzes__total_attempts'),
            avg_score=Avg('quizzes__average_score')
        )
        
        for category in categories:
            stats['category_stats'].append({
                'id': category.id,
                'name': category.name,
                'quiz_count': category.quiz_count,
                'total_attempts': category.total_attempts or 0,
                'average_score': category.avg_score or 0
            })
        
        return Response(stats)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured quizzes"""
        queryset = self.get_queryset().filter(is_featured=True)
        serializer = QuizListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent quizzes"""
        queryset = self.get_queryset().order_by('-created_at')[:10]
        serializer = QuizListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular quizzes"""
        queryset = self.get_queryset().order_by('-total_attempts')[:10]
        serializer = QuizListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """Share a quiz"""
        quiz = self.get_object()
        serializer = QuizShareCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        share = serializer.save()
        
        # Track analytics
        QuizAnalytics.objects.create(
            quiz=quiz,
            user=request.user,
            action_type='share',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({'message': 'Quiz shared successfully'})

    @action(detail=False, methods=['post'])
    def bulk_action(self, request):
        """Perform bulk actions on quizzes"""
        serializer = QuizBulkActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        quiz_ids = serializer.validated_data['quiz_ids']
        action = serializer.validated_data['action']
        
        quizzes = Quiz.objects.filter(id__in=quiz_ids, creator=request.user)
        
        if action == 'publish':
            quizzes.update(status='published')
        elif action == 'archive':
            quizzes.update(status='archived')
        elif action == 'delete':
            quizzes.delete()
        elif action == 'feature':
            quizzes.update(is_featured=True)
        elif action == 'unfeature':
            quizzes.update(is_featured=False)
        
        return Response({'message': f'{quizzes.count()} quizzes {action}ed successfully'})

class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for questions"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['quiz', 'question_type', 'is_active']
    search_fields = ['question_text']
    ordering_fields = ['order', 'created_at']
    ordering = ['order', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return QuestionListSerializer
        return QuestionSerializer

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = super().get_queryset()
        
        # Only show questions for quizzes created by user
        if self.request.user.is_authenticated:
            queryset = queryset.filter(quiz__creator=self.request.user)
        
        return queryset.select_related('quiz').prefetch_related('options')

class OptionViewSet(viewsets.ModelViewSet):
    """ViewSet for question options"""
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['question']
    ordering_fields = ['order', 'created_at']
    ordering = ['order', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return OptionListSerializer
        return OptionSerializer

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = super().get_queryset()
        
        # Only show options for questions in quizzes created by user
        if self.request.user.is_authenticated:
            queryset = queryset.filter(question__quiz__creator=self.request.user)
        
        return queryset.select_related('question')

class QuizAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for quiz attempts (read-only)"""
    serializer_class = QuizAttemptSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['quiz', 'status', 'passed']
    ordering_fields = ['started_at', 'completed_at', 'percentage']
    ordering = ['-started_at']

    def get_queryset(self):
        """Filter queryset to show only user's attempts"""
        return QuizAttempt.objects.filter(user=self.request.user).select_related('quiz', 'user')

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get detailed results for an attempt"""
        attempt = self.get_object()
        results = QuizResult.objects.filter(attempt=attempt).select_related('question')
        serializer = QuizResultSerializer(results, many=True)
        return Response(serializer.data)

class QuizAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for quiz analytics (read-only)"""
    serializer_class = QuizAnalyticsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['quiz', 'action_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter queryset to show only analytics for user's quizzes"""
        return QuizAnalytics.objects.filter(quiz__creator=self.request.user).select_related('quiz', 'user')

class QuizShareViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for quiz shares (read-only)"""
    serializer_class = QuizShareSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['quiz', 'share_type', 'is_viewed']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter queryset to show only shares by user"""
        return QuizShare.objects.filter(shared_by=self.request.user).select_related('quiz', 'shared_by', 'shared_with')

class QuizTimerViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for quiz timers (read-only)"""
    serializer_class = QuizTimerSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['attempt']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter queryset to show only user's timers"""
        return QuizTimer.objects.filter(attempt__user=self.request.user).select_related('attempt')

    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        """Pause timer"""
        timer = self.get_object()
        timer.pause()
        serializer = self.get_serializer(timer)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def resume(self, request, pk=None):
        """Resume timer"""
        timer = self.get_object()
        timer.resume()
        serializer = self.get_serializer(timer)
        return Response(serializer.data)
