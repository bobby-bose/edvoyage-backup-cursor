"""
Application views for EdVoyage API.
Handles application-related API endpoints with proper error handling and logging.
"""

import logging
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Avg, Min, Max
from django.utils import timezone
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Application, ApplicationDocument, ApplicationStatus, ApplicationInterview,
    ApplicationFee, ApplicationCommunication
)
from .serializers import (
    ApplicationSerializer, ApplicationCreateSerializer, ApplicationUpdateSerializer,
    ApplicationDocumentSerializer, ApplicationDocumentCreateSerializer,
    ApplicationStatusSerializer, ApplicationStatusUpdateSerializer,
    ApplicationInterviewSerializer, ApplicationInterviewCreateSerializer,
    ApplicationFeeSerializer, ApplicationFeeCreateSerializer,
    ApplicationCommunicationSerializer, ApplicationSubmitSerializer,
    ApplicationSearchSerializer, ApplicationStatsSerializer, ApplicationDashboardSerializer,
    FrontendApplicationSerializer
)

logger = logging.getLogger(__name__)


class ApplicationPagination(PageNumberPagination):
    """Custom pagination for application listings."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for application management.
    Provides CRUD operations for applications with search and filtering.
    """
    serializer_class = ApplicationSerializer
    pagination_class = ApplicationPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'status', 'priority', 'university', 'program', 'is_complete', 
        'is_verified', 'intended_start_semester', 'academic_year'
    ]
    search_fields = [
        'application_number', 'personal_statement', 'research_proposal',
        'university__name', 'program__name'
    ]
    ordering_fields = [
        'created_at', 'submitted_at', 'decision_date', 'priority', 'status'
    ]
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter applications by current user."""
        # Return all applications for now (no authentication required)
        print("Returning all applications (no authentication required)")
        return Application.objects.all().select_related(
            'university', 'program'
        ).prefetch_related(
            'documents', 'status_history', 'interviews', 'fees', 'communications'
        )

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return FrontendApplicationSerializer
        elif self.action == 'create':
            return ApplicationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ApplicationUpdateSerializer
        return ApplicationSerializer

    def list(self, request, *args, **kwargs):
        """List applications with enhanced filtering."""
        print("Entering ApplicationListView")
        
        try:
            response = super().list(request, *args, **kwargs)
            print(f"Application list returned {len(response.data['results'])} applications")
            return response
        except Exception as e:
            logger.error(f"Error in application list: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving applications', 'results': [], 'count': 0},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        """Create a new application."""
        print("Creating new application") if hasattr(request, 'user') else None
        try:
            response = super().create(request, *args, **kwargs)
            print(f"Application created successfully: {response.data.get('application_number')}") if hasattr(request, 'user') else None
            return Response(
                {'success': True, 'data': response.data, 'message': 'Application created successfully'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error creating application: {e}")
            return Response(
                {'success': False, 'message': 'Error creating application'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'], url_path='test-create')
    def test_create(self, request):
        """Test endpoint for creating applications without authentication."""
        print("🔍 DEBUG: Test create endpoint called")
        try:
            # Get or create a test user (ID: 1)
            from django.contrib.auth.models import User
            test_user, created = User.objects.get_or_create(
                id=1,
                defaults={
                    'username': 'testuser',
                    'email': 'test@example.com',
                    'first_name': 'Test',
                    'last_name': 'User'
                }
            )
            
            # Override the request user for this action
            request.user = test_user
            print(f"🔍 DEBUG: Using test user: {test_user.username} (ID: {test_user.id})")
            
            # Call the create method
            return self.create(request)
            
        except Exception as e:
            print(f"🔍 DEBUG: Error in test create: {e}")
            return Response(
                {'success': False, 'message': f'Error creating application: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'], url_path='simple-test')
    def simple_test(self, request):
        """Simple test endpoint for creating applications with minimal validation."""
        print("🔍 DEBUG: Simple test endpoint called")
        try:
            # Get or create a test user (ID: 1)
            from django.contrib.auth.models import User
            test_user, created = User.objects.get_or_create(
                id=1,
                defaults={
                    'username': 'testuser',
                    'email': 'test@example.com',
                    'first_name': 'Test',
                    'last_name': 'User'
                }
            )
            
            # Get or create a test university (ID: 1)
            from universities.models import University
            test_university, created = University.objects.get_or_create(
                id=1,
                defaults={
                    'name': 'Test University',
                    'short_name': 'TU',
                    'slug': 'test-university',
                    'university_type': 'public',
                    'country': 'Test Country',
                    'city': 'Test City'
                }
            )
            
            # Get or create a test program (ID: 1)
            from universities.models import UniversityProgram
            test_program, created = UniversityProgram.objects.get_or_create(
                id=1,
                defaults={
                    'university': test_university,
                    'name': 'Computer Science',
                    'program_level': 'undergraduate',
                    'program_type': 'full_time',
                    'duration_years': 4
                }
            )
            
            # Generate application number
            import uuid
            application_number = f"APP-{uuid.uuid4().hex[:8].upper()}"
            
            # Create application directly
            from .models import Application
            application = Application.objects.create(
                user=test_user,
                university=test_university,
                program=test_program,
                application_number=application_number,
                intended_start_date='2024-09-01',
                intended_start_semester='Fall 2024',
                academic_year='2024',
                personal_statement='Test application created via simple endpoint',
                priority='medium'
            )
            
            print(f"🔍 DEBUG: Application created successfully: {application.application_number}")
            
            return Response({
                'success': True,
                'message': 'Application created successfully',
                'data': {
                    'application_number': application.application_number,
                    'id': application.id,
                    'status': application.status
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"🔍 DEBUG: Error in simple test: {e}")
            return Response(
                {'success': False, 'message': f'Error creating application: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'], url_path='submit')
    def submit(self, request, pk=None):
        """Submit an application."""
        print("Entering ApplicationSubmitView") if hasattr(request, 'user') else None
        try:
            application = self.get_object()
            
            # Check if application can be submitted
            if application.status != 'draft':
                return Response(
                    {'success': False, 'message': 'Application can only be submitted from draft status'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate required documents
            required_documents = application.documents.filter(is_required=True)
            if not required_documents.exists():
                return Response(
                    {'success': False, 'message': 'Please upload all required documents before submitting'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update application status
            application.status = 'submitted'
            application.submitted_at = timezone.now()
            application.save()
            
            # Create status history
            ApplicationStatus.objects.create(
                application=application,
                status='submitted',
                description='Application submitted successfully',
                changed_by=request.user
            )
            
            print(f"Application submitted successfully: {application.application_number}") if hasattr(request, 'user') else None
            return Response({
                'success': True,
                'message': 'Application submitted successfully'
            })
        except Exception as e:
            logger.error(f"Error submitting application: {e}")
            return Response(
                {'success': False, 'message': 'Error submitting application'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='search')
    def search(self, request):
        """Advanced application search."""
        print("Entering ApplicationSearchView") if hasattr(request, 'user') else None
        try:
            serializer = ApplicationSearchSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            queryset = self.get_queryset()
            
            # Apply search filters
            status = serializer.validated_data.get('status')
            if status:
                queryset = queryset.filter(status=status)
            
            priority = serializer.validated_data.get('priority')
            if priority:
                queryset = queryset.filter(priority=priority)
            
            university = serializer.validated_data.get('university')
            if university:
                queryset = queryset.filter(university_id=university)
            
            program = serializer.validated_data.get('program')
            if program:
                queryset = queryset.filter(program_id=program)
            
            is_complete = serializer.validated_data.get('is_complete')
            if is_complete is not None:
                queryset = queryset.filter(is_complete=is_complete)
            
            is_verified = serializer.validated_data.get('is_verified')
            if is_verified is not None:
                queryset = queryset.filter(is_verified=is_verified)
            
            date_from = serializer.validated_data.get('date_from')
            if date_from:
                queryset = queryset.filter(created_at__date__gte=date_from)
            
            date_to = serializer.validated_data.get('date_to')
            if date_to:
                queryset = queryset.filter(created_at__date__lte=date_to)
            
            # Paginate results
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = ApplicationSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = ApplicationSerializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': f'Found {len(serializer.data)} applications'
            })
        except Exception as e:
            logger.error(f"Error in application search: {e}")
            return Response(
                {'success': False, 'message': 'Error searching applications'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        """Get application statistics."""
        print("Entering ApplicationStatsView") if hasattr(request, 'user') else None
        try:
            queryset = self.get_queryset()
            
            # Calculate statistics
            total_applications = queryset.count()
            submitted_applications = queryset.filter(status='submitted').count()
            accepted_applications = queryset.filter(status='accepted').count()
            rejected_applications = queryset.filter(status='rejected').count()
            pending_applications = queryset.filter(status__in=['draft', 'under_review']).count()
            
            # Applications by status
            applications_by_status = queryset.values('status').annotate(
                count=Count('id')
            ).order_by('-count')
            
            # Applications by university
            applications_by_university = queryset.values('university__name').annotate(
                count=Count('id')
            ).order_by('-count')
            
            # Recent applications
            recent_applications = queryset.order_by('-created_at')[:10]
            
            # Overdue applications
            overdue_applications = queryset.filter(
                status__in=['submitted', 'under_review'],
                submitted_at__lt=timezone.now() - timezone.timedelta(days=30)
            )
            
            data = {
                'total_applications': total_applications,
                'submitted_applications': submitted_applications,
                'accepted_applications': accepted_applications,
                'rejected_applications': rejected_applications,
                'pending_applications': pending_applications,
                'applications_by_status': {item['status']: item['count'] for item in applications_by_status},
                'applications_by_university': {item['university__name']: item['count'] for item in applications_by_university},
                'recent_applications': ApplicationSerializer(recent_applications, many=True).data,
                'overdue_applications': ApplicationSerializer(overdue_applications, many=True).data,
            }
            
            print(f"Application stats calculated successfully") if hasattr(request, 'user') else None
            return Response(
                {'success': True, 'data': data, 'message': 'Statistics retrieved successfully'}
            )
        except Exception as e:
            logger.error(f"Error in application stats: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving statistics'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard(self, request):
        """Get application dashboard data."""
        print("Entering ApplicationDashboardView")
        try:
            queryset = self.get_queryset() if hasattr(self, 'get_queryset') else Application.objects.all()
            # Dashboard data (no user filtering)
            user_applications = queryset.order_by('-created_at')[:5]
            recent_status_updates = ApplicationStatus.objects.order_by('-changed_at')[:10]
            upcoming_interviews = ApplicationInterview.objects.filter(status='scheduled', scheduled_date__gte=timezone.now()).order_by('scheduled_date')[:5]
            pending_fees = ApplicationFee.objects.filter(payment_status='pending').order_by('due_date')[:5]
            recent_communications = ApplicationCommunication.objects.order_by('-created_at')[:10]
            # Calculate stats
            stats_data = {
                'total_applications': queryset.count(),
                'submitted_applications': queryset.filter(status='submitted').count(),
                'accepted_applications': queryset.filter(status='accepted').count(),
                'rejected_applications': queryset.filter(status='rejected').count(),
                'pending_applications': queryset.filter(status__in=['draft', 'under_review']).count(),
                'applications_by_status': {},
                'applications_by_university': {},
                'recent_applications': ApplicationSerializer(user_applications, many=True).data,
                'overdue_applications': [],
            }
            data = {
                'user_applications': ApplicationSerializer(user_applications, many=True).data,
                'recent_status_updates': ApplicationStatusSerializer(recent_status_updates, many=True).data,
                'upcoming_interviews': ApplicationInterviewSerializer(upcoming_interviews, many=True).data,
                'pending_fees': ApplicationFeeSerializer(pending_fees, many=True).data,
                'recent_communications': ApplicationCommunicationSerializer(recent_communications, many=True).data,
                'application_stats': stats_data,
            }
            print(f"Application dashboard data retrieved successfully")
            return Response(
                {'success': True, 'data': data, 'message': 'Dashboard data retrieved successfully'}
            )
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            logger.error(f"Error in application dashboard: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving dashboard data'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ApplicationDocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for application document management."""
    serializer_class = ApplicationDocumentSerializer
    pagination_class = ApplicationPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['document_type', 'status', 'is_required', 'is_verified']
    search_fields = ['document_name', 'document_type']
    ordering = ['-uploaded_at']

    def get_queryset(self):
        """Filter documents by current user's applications."""
        return ApplicationDocument.objects.filter(
            application__user=self.request.user
        ).select_related('application')

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return ApplicationDocumentCreateSerializer
        return ApplicationDocumentSerializer

    def perform_create(self, serializer):
        """Create document with application context."""
        application_id = self.kwargs.get('application_pk')
        application = get_object_or_404(Application, id=application_id, user=self.request.user)
        serializer.save(application=application)

    def list(self, request, *args, **kwargs):
        """List documents with enhanced filtering."""
        print("Entering ApplicationDocumentListView") if hasattr(request, 'user') else None
        try:
            response = super().list(request, *args, **kwargs)
            print(f"Document list returned {len(response.data['results'])} documents") if hasattr(request, 'user') else None
            return response
        except Exception as e:
            logger.error(f"Error in document list: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving documents'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ApplicationStatusViewSet(viewsets.ModelViewSet):
    """ViewSet for application status management."""
    serializer_class = ApplicationStatusSerializer
    pagination_class = ApplicationPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'changed_by']
    ordering = ['-changed_at']

    def get_queryset(self):
        """Filter status history by current user's applications."""
        return ApplicationStatus.objects.filter(
            application__user=self.request.user
        ).select_related('application', 'changed_by')

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return ApplicationStatusUpdateSerializer
        return ApplicationStatusSerializer

    def perform_create(self, serializer):
        """Create status update with application context."""
        application_id = self.kwargs.get('application_pk')
        application = get_object_or_404(Application, id=application_id, user=self.request.user)
        serializer.save(application=application)


class ApplicationInterviewViewSet(viewsets.ModelViewSet):
    """ViewSet for application interview management."""
    serializer_class = ApplicationInterviewSerializer
    pagination_class = ApplicationPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['interview_type', 'status', 'interviewer_name']
    search_fields = ['interviewer_name', 'location', 'platform']
    ordering_fields = ['scheduled_date', 'created_at']
    ordering = ['-scheduled_date']

    def get_queryset(self):
        """Filter interviews by current user's applications."""
        return ApplicationInterview.objects.filter(
            application__user=self.request.user
        ).select_related('application')

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return ApplicationInterviewCreateSerializer
        return ApplicationInterviewSerializer

    def perform_create(self, serializer):
        """Create interview with application context."""
        application_id = self.kwargs.get('application_pk')
        application = get_object_or_404(Application, id=application_id, user=self.request.user)
        serializer.save(application=application)

    def list(self, request, *args, **kwargs):
        """List interviews with enhanced filtering."""
        print("Entering ApplicationInterviewListView") if hasattr(request, 'user') else None
        try:
            response = super().list(request, *args, **kwargs)
            print(f"Interview list returned {len(response.data['results'])} interviews") if hasattr(request, 'user') else None
            return response
        except Exception as e:
            logger.error(f"Error in interview list: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving interviews'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ApplicationFeeViewSet(viewsets.ModelViewSet):
    """ViewSet for application fee management."""
    serializer_class = ApplicationFeeSerializer
    pagination_class = ApplicationPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['fee_type', 'payment_status', 'currency']
    ordering_fields = ['due_date', 'amount', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter fees by current user's applications."""
        return ApplicationFee.objects.filter(
            application__user=self.request.user
        ).select_related('application')

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return ApplicationFeeCreateSerializer
        return ApplicationFeeSerializer

    def perform_create(self, serializer):
        """Create fee with application context."""
        application_id = self.kwargs.get('application_pk')
        application = get_object_or_404(Application, id=application_id, user=self.request.user)
        serializer.save(application=application)

    def list(self, request, *args, **kwargs):
        """List fees with enhanced filtering."""
        print("Entering ApplicationFeeListView") if hasattr(request, 'user') else None
        try:
            response = super().list(request, *args, **kwargs)
            print(f"Fee list returned {len(response.data['results'])} fees") if hasattr(request, 'user') else None
            return response
        except Exception as e:
            logger.error(f"Error in fee list: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving fees'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ApplicationCommunicationViewSet(viewsets.ModelViewSet):
    """ViewSet for application communication management."""
    serializer_class = ApplicationCommunicationSerializer
    pagination_class = ApplicationPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['communication_type', 'direction', 'is_sent', 'is_delivered', 'is_read']
    search_fields = ['subject', 'message', 'from_email', 'to_email']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter communications by current user's applications."""
        return ApplicationCommunication.objects.filter(
            application__user=self.request.user
        ).select_related('application')

    def list(self, request, *args, **kwargs):
        """List communications with enhanced filtering."""
        print("Entering ApplicationCommunicationListView") if hasattr(request, 'user') else None
        try:
            response = super().list(request, *args, **kwargs)
            print(f"Communication list returned {len(response.data['results'])} communications") if hasattr(request, 'user') else None
            return response
        except Exception as e:
            logger.error(f"Error in communication list: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving communications'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
