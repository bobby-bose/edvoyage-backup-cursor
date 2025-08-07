"""
Course views for EdVoyage API.
Handles course-related API endpoints with proper error handling and logging.
"""

import logging
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count, F
from django.utils import timezone
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Course, Subject, CourseSubject, FeeStructure, 
    CourseRequirement, CourseApplication, CourseRating
)
from .serializers import (
    CourseListSerializer, CourseDetailSerializer, CourseCreateSerializer, CourseUpdateSerializer,
    SubjectSerializer, FeeStructureSerializer, CourseRequirementSerializer, CourseRatingSerializer,
    CourseApplicationSerializer, CourseApplicationCreateSerializer, CourseSearchSerializer,
    CourseFilterSerializer, CourseStatsSerializer
)

logger = logging.getLogger(__name__)


class CoursePagination(PageNumberPagination):
    """Custom pagination for course listings."""
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for course management.
    Provides CRUD operations for courses with filtering and search capabilities.
    """
    queryset = Course.objects.select_related('university').prefetch_related('subjects', 'ratings')
    serializer_class = CourseListSerializer
    pagination_class = CoursePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['university', 'level', 'duration', 'status', 'is_featured', 'is_popular']
    search_fields = ['name', 'code', 'description', 'university__name']
    ordering_fields = ['name', 'tuition_fee', 'created_at', 'average_rating']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'retrieve':
            return CourseDetailSerializer
        elif self.action == 'create':
            return CourseCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CourseUpdateSerializer
        return CourseListSerializer

    def get_queryset(self):
        """Filter queryset based on request parameters."""
        queryset = super().get_queryset()
        
        # Add custom filtering
        if self.action == 'list':
            # Only show active courses in listing
            queryset = queryset.filter(status='active')
            
            # Filter by rating if provided
            min_rating = self.request.query_params.get('min_rating')
            if min_rating:
                queryset = queryset.annotate(avg_rating=Avg('ratings__rating')).filter(
                    avg_rating__gte=float(min_rating)
                )
            
            # Filter by fee range
            min_fee = self.request.query_params.get('min_fee')
            max_fee = self.request.query_params.get('max_fee')
            if min_fee:
                queryset = queryset.filter(tuition_fee__gte=float(min_fee))
            if max_fee:
                queryset = queryset.filter(tuition_fee__lte=float(max_fee))
        
        return queryset

    def list(self, request, *args, **kwargs):
        """List courses with enhanced filtering."""
        print("Entering CourseListView") if hasattr(request, 'user') else None
        try:
            response = super().list(request, *args, **kwargs)
            print(f"Course list returned {len(response.data['results'])} courses") if hasattr(request, 'user') else None
            return response
        except Exception as e:
            logger.error(f"Error in course list: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving courses'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        """Retrieve detailed course information."""
        print(f"Entering CourseDetailView for course {kwargs.get('pk')}") if hasattr(request, 'user') else None
        try:
            response = super().retrieve(request, *args, **kwargs)
            print(f"Course detail retrieved successfully") if hasattr(request, 'user') else None
            return response
        except Exception as e:
            logger.error(f"Error retrieving course detail: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving course details'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        """Create a new course."""
        print("Creating new course") if hasattr(request, 'user') else None
        try:
            response = super().create(request, *args, **kwargs)
            print(f"Course created successfully: {response.data.get('name')}") if hasattr(request, 'user') else None
            return Response(
                {'success': True, 'data': response.data, 'message': 'Course created successfully'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error creating course: {e}")
            return Response(
                {'success': False, 'message': 'Error creating course'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        """Search courses with advanced filtering."""
        print("Entering CourseSearchView") if hasattr(request, 'user') else None
        try:
            serializer = CourseSearchSerializer(data=request.query_params)
            serializer.is_valid(raise_exception=True)
            
            queryset = self.get_queryset()
            
            # Apply search filters
            query = serializer.validated_data.get('query')
            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) |
                    Q(description__icontains=query) |
                    Q(university__name__icontains=query) |
                    Q(subjects__name__icontains=query)
                ).distinct()
            
            # Apply other filters
            if serializer.validated_data.get('featured_only'):
                queryset = queryset.filter(is_featured=True)
            
            if serializer.validated_data.get('popular_only'):
                queryset = queryset.filter(is_popular=True)
            
            # Paginate results
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = CourseListSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = CourseListSerializer(queryset, many=True)
            print(f"Course search returned {len(serializer.data)} results") if hasattr(request, 'user') else None
            return Response(
                {'success': True, 'data': serializer.data, 'message': 'Search completed successfully'}
            )
        except Exception as e:
            logger.error(f"Error in course search: {e}")
            return Response(
                {'success': False, 'message': 'Error searching courses'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='filter')
    def filter(self, request):
        """Advanced course filtering."""
        print("Entering CourseFilterView") if hasattr(request, 'user') else None
        try:
            serializer = CourseFilterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            queryset = self.get_queryset()
            
            # Apply filters
            filters = serializer.validated_data
            
            if filters.get('universities'):
                queryset = queryset.filter(university_id__in=filters['universities'])
            
            if filters.get('levels'):
                queryset = queryset.filter(level__in=filters['levels'])
            
            if filters.get('durations'):
                queryset = queryset.filter(duration__in=filters['durations'])
            
            if filters.get('subjects'):
                queryset = queryset.filter(subjects__name__in=filters['subjects']).distinct()
            
            if filters.get('countries'):
                queryset = queryset.filter(university__country__in=filters['countries'])
            
            if filters.get('fee_range'):
                fee_range = filters['fee_range']
                if 'min' in fee_range:
                    queryset = queryset.filter(tuition_fee__gte=fee_range['min'])
                if 'max' in fee_range:
                    queryset = queryset.filter(tuition_fee__lte=fee_range['max'])
            
            if filters.get('rating_min'):
                queryset = queryset.annotate(avg_rating=Avg('ratings__rating')).filter(
                    avg_rating__gte=filters['rating_min']
                )
            
            if filters.get('status'):
                queryset = queryset.filter(status=filters['status'])
            
            # Paginate results
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = CourseListSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = CourseListSerializer(queryset, many=True)
            print(f"Course filter returned {len(serializer.data)} results") if hasattr(request, 'user') else None
            return Response(
                {'success': True, 'data': serializer.data, 'message': 'Filter applied successfully'}
            )
        except Exception as e:
            logger.error(f"Error in course filter: {e}")
            return Response(
                {'success': False, 'message': 'Error filtering courses'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'], url_path='apply')
    def apply(self, request, pk=None):
        """Apply to a course."""
        print(f"Entering CourseApplicationView for course {pk}") if hasattr(request, 'user') else None
        try:
            course = self.get_object()
            serializer = CourseApplicationCreateSerializer(
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            
            # Create application
            application = serializer.save(user=request.user, course=course)
            
            print(f"Application created for course {course.name} by user {request.user.username}") if hasattr(request, 'user') else None
            
            return Response(
                {
                    'success': True,
                    'data': CourseApplicationSerializer(application).data,
                    'message': 'Application submitted successfully'
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error in course application: {e}")
            return Response(
                {'success': False, 'message': 'Error submitting application'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'], url_path='rate')
    def rate(self, request, pk=None):
        """Rate a course."""
        print(f"Entering CourseRatingView for course {pk}") if hasattr(request, 'user') else None
        try:
            course = self.get_object()
            serializer = CourseRatingSerializer(
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            
            # Create or update rating
            rating, created = CourseRating.objects.update_or_create(
                user=request.user,
                course=course,
                defaults=serializer.validated_data
            )
            
            action = 'created' if created else 'updated'
            print(f"Course rating {action} for course {course.name} by user {request.user.username}") if hasattr(request, 'user') else None
            
            return Response(
                {
                    'success': True,
                    'data': CourseRatingSerializer(rating).data,
                    'message': f'Rating {action} successfully'
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error in course rating: {e}")
            return Response(
                {'success': False, 'message': 'Error submitting rating'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        """Get course statistics."""
        print("Entering CourseStatsView") if hasattr(request, 'user') else None
        try:
            # Calculate statistics
            total_courses = Course.objects.count()
            total_applications = CourseApplication.objects.count()
            
            # Average rating across all courses
            avg_rating = CourseRating.objects.aggregate(avg=Avg('rating'))['avg'] or 0
            total_ratings = CourseRating.objects.count()
            
            # Courses by level
            courses_by_level = dict(
                Course.objects.values('level').annotate(count=Count('id')).values_list('level', 'count')
            )
            
            # Courses by duration
            courses_by_duration = dict(
                Course.objects.values('duration').annotate(count=Count('id')).values_list('duration', 'count')
            )
            
            # Top courses by rating
            top_courses = Course.objects.annotate(
                avg_rating=Avg('ratings__rating')
            ).filter(avg_rating__isnull=False).order_by('-avg_rating')[:10]
            
            # Featured and popular courses
            featured_courses = Course.objects.filter(is_featured=True, status='active')[:10]
            popular_courses = Course.objects.filter(is_popular=True, status='active')[:10]
            
            data = {
                'total_courses': total_courses,
                'total_applications': total_applications,
                'average_rating': round(avg_rating, 2),
                'total_ratings': total_ratings,
                'courses_by_level': courses_by_level,
                'courses_by_duration': courses_by_duration,
                'top_courses': CourseListSerializer(top_courses, many=True).data,
                'featured_courses': CourseListSerializer(featured_courses, many=True).data,
                'popular_courses': CourseListSerializer(popular_courses, many=True).data,
            }
            
            print(f"Course stats calculated successfully") if hasattr(request, 'user') else None
            return Response(
                {'success': True, 'data': data, 'message': 'Statistics retrieved successfully'}
            )
        except Exception as e:
            logger.error(f"Error in course stats: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving statistics'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SubjectViewSet(viewsets.ModelViewSet):
    """ViewSet for subject management."""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    pagination_class = CoursePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_core']
    search_fields = ['name', 'code', 'description']

    def list(self, request, *args, **kwargs):
        """List subjects."""
        print("Entering SubjectListView") if hasattr(request, 'user') else None
        try:
            response = super().list(request, *args, **kwargs)
            print(f"Subject list returned {len(response.data['results'])} subjects") if hasattr(request, 'user') else None
            return response
        except Exception as e:
            logger.error(f"Error in subject list: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving subjects'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CourseApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for course applications (read-only for users)."""
    serializer_class = CourseApplicationSerializer
    pagination_class = CoursePagination

    def get_queryset(self):
        """Filter applications by current user."""
        return CourseApplication.objects.filter(user=self.request.user).select_related(
            'course', 'course__university'
        )

    def list(self, request, *args, **kwargs):
        """List user's applications."""
        print("Entering CourseApplicationListView") if hasattr(request, 'user') else None
        try:
            response = super().list(request, *args, **kwargs)
            print(f"Application list returned {len(response.data['results'])} applications") if hasattr(request, 'user') else None
            return response
        except Exception as e:
            logger.error(f"Error in application list: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving applications'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
