from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Q
from django.utils import timezone
from django.contrib.auth import get_user_model
import logging

from .models import (
    StudyAbroadProgram, StudyAbroadApplication, StudyAbroadExperience,
    StudyAbroadResource, StudyAbroadEvent, StudyAbroadEventRegistration
)
from .serializers import (
    StudyAbroadProgramSerializer, StudyAbroadApplicationSerializer, StudyAbroadExperienceSerializer,
    StudyAbroadResourceSerializer, StudyAbroadEventSerializer, StudyAbroadEventRegistrationSerializer,
    DetailedStudyAbroadProgramSerializer, DetailedStudyAbroadApplicationSerializer, StudyAbroadStatisticsSerializer
)

User = get_user_model()
logger = logging.getLogger(__name__)

class StudyAbroadProgramViewSet(viewsets.ModelViewSet):
    """ViewSet for StudyAbroadProgram model"""
    queryset = StudyAbroadProgram.objects.all()
    serializer_class = StudyAbroadProgramSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['program_type', 'status', 'country', 'city', 'is_active', 'is_featured']
    search_fields = ['name', 'description', 'institution', 'field_of_study']
    ordering_fields = ['name', 'start_date', 'end_date', 'application_deadline', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Use detailed serializer for retrieve action"""
        if self.action == 'retrieve':
            return DetailedStudyAbroadProgramSerializer
        return StudyAbroadProgramSerializer

    @action(detail=False, methods=['get'])
    def active_programs(self, request):
        """Get only active programs"""
        try:
            programs = self.queryset.filter(is_active=True, status='active')
            serializer = self.get_serializer(programs, many=True)
            logger.info(f"Retrieved {programs.count()} active study abroad programs")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving active programs: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve active programs'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def featured_programs(self, request):
        """Get featured programs"""
        try:
            featured = self.queryset.filter(is_featured=True, is_active=True)
            serializer = self.get_serializer(featured, many=True)
            logger.info(f"Retrieved {featured.count()} featured study abroad programs")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving featured programs: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve featured programs'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def by_country(self, request):
        """Get programs by country"""
        try:
            country = request.query_params.get('country')
            if country:
                programs = self.queryset.filter(country__icontains=country, is_active=True)
                serializer = self.get_serializer(programs, many=True)
                logger.info(f"Retrieved {programs.count()} programs for country: {country}")
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'Country parameter is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Error retrieving programs by country: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve programs by country'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get programs by type"""
        try:
            program_type = request.query_params.get('type')
            if program_type:
                programs = self.queryset.filter(program_type=program_type, is_active=True)
                serializer = self.get_serializer(programs, many=True)
                logger.info(f"Retrieved {programs.count()} programs of type: {program_type}")
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'Type parameter is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Error retrieving programs by type: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve programs by type'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def toggle_featured(self, request, pk=None):
        """Toggle program featured status (admin only)"""
        try:
            program = self.get_object()
            program.is_featured = not program.is_featured
            program.save()
            logger.info(f"Toggled program {program.name} featured status to {program.is_featured}")
            return Response({'message': f'Program {program.name} {"featured" if program.is_featured else "unfeatured"}'})
        except Exception as e:
            logger.error(f"Error toggling program featured status: {str(e)}")
            return Response(
                {'error': 'Failed to toggle program featured status'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StudyAbroadApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for StudyAbroadApplication model"""
    serializer_class = StudyAbroadApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'program', 'status']
    search_fields = ['current_institution', 'current_major', 'academic_goals']
    ordering_fields = ['application_date', 'review_date', 'decision_date', 'created_at']
    ordering = ['-application_date']

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_staff:
            return StudyAbroadApplication.objects.all()
        return StudyAbroadApplication.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """Use detailed serializer for retrieve action"""
        if self.action == 'retrieve':
            return DetailedStudyAbroadApplicationSerializer
        return StudyAbroadApplicationSerializer

    def perform_create(self, serializer):
        """Set user to current user when creating"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_applications(self, request):
        """Get current user's applications"""
        try:
            applications = self.get_queryset().filter(user=request.user)
            serializer = self.get_serializer(applications, many=True)
            logger.info(f"Retrieved {applications.count()} applications for user {request.user.username}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving user applications: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve applications'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Get applications by status"""
        try:
            status_filter = request.query_params.get('status')
            if status_filter:
                applications = self.get_queryset().filter(status=status_filter)
                serializer = self.get_serializer(applications, many=True)
                logger.info(f"Retrieved {applications.count()} applications with status: {status_filter}")
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'Status parameter is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Error retrieving applications by status: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve applications by status'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def review_application(self, request, pk=None):
        """Review application (admin only)"""
        try:
            application = self.get_object()
            new_status = request.data.get('status')
            reviewer_notes = request.data.get('reviewer_notes', '')
            
            if new_status not in ['accepted', 'rejected', 'waitlisted', 'under_review']:
                return Response(
                    {'error': 'Invalid status'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            application.status = new_status
            application.reviewer_notes = reviewer_notes
            application.reviewer = request.user
            application.save()
            
            logger.info(f"Application {application.id} reviewed by {request.user.username} with status: {new_status}")
            return Response({'message': f'Application {new_status} successfully'})
        except Exception as e:
            logger.error(f"Error reviewing application: {str(e)}")
            return Response(
                {'error': 'Failed to review application'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StudyAbroadExperienceViewSet(viewsets.ModelViewSet):
    """ViewSet for StudyAbroadExperience model"""
    serializer_class = StudyAbroadExperienceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'program', 'experience_type', 'is_approved', 'is_featured']
    search_fields = ['title', 'content']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_staff:
            return StudyAbroadExperience.objects.all()
        return StudyAbroadExperience.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set user to current user when creating"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_experiences(self, request):
        """Get current user's experiences"""
        try:
            experiences = self.get_queryset().filter(user=request.user)
            serializer = self.get_serializer(experiences, many=True)
            logger.info(f"Retrieved {experiences.count()} experiences for user {request.user.username}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving user experiences: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve experiences'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def approved_experiences(self, request):
        """Get approved experiences"""
        try:
            approved = StudyAbroadExperience.objects.filter(is_approved=True, is_public=True)
            serializer = self.get_serializer(approved, many=True)
            logger.info(f"Retrieved {approved.count()} approved experiences")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving approved experiences: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve approved experiences'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def featured_experiences(self, request):
        """Get featured experiences"""
        try:
            featured = StudyAbroadExperience.objects.filter(is_featured=True, is_approved=True, is_public=True)
            serializer = self.get_serializer(featured, many=True)
            logger.info(f"Retrieved {featured.count()} featured experiences")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving featured experiences: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve featured experiences'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve_experience(self, request, pk=None):
        """Approve experience (admin only)"""
        try:
            experience = self.get_object()
            experience.is_approved = True
            experience.save()
            logger.info(f"Experience {experience.id} approved by {request.user.username}")
            return Response({'message': 'Experience approved successfully'})
        except Exception as e:
            logger.error(f"Error approving experience: {str(e)}")
            return Response(
                {'error': 'Failed to approve experience'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StudyAbroadResourceViewSet(viewsets.ModelViewSet):
    """ViewSet for StudyAbroadResource model"""
    queryset = StudyAbroadResource.objects.all()
    serializer_class = StudyAbroadResourceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['resource_type', 'is_active', 'is_featured', 'requires_authentication']
    search_fields = ['title', 'description', 'content', 'categories', 'tags']
    ordering_fields = ['title', 'download_count', 'view_count', 'created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def active_resources(self, request):
        """Get only active resources"""
        try:
            resources = self.queryset.filter(is_active=True)
            serializer = self.get_serializer(resources, many=True)
            logger.info(f"Retrieved {resources.count()} active resources")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving active resources: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve active resources'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def featured_resources(self, request):
        """Get featured resources"""
        try:
            featured = self.queryset.filter(is_featured=True, is_active=True)
            serializer = self.get_serializer(featured, many=True)
            logger.info(f"Retrieved {featured.count()} featured resources")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving featured resources: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve featured resources'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def increment_view(self, request, pk=None):
        """Increment view count"""
        try:
            resource = self.get_object()
            resource.increment_view_count()
            logger.info(f"Incremented view count for resource {resource.id}")
            return Response({'message': 'View count incremented'})
        except Exception as e:
            logger.error(f"Error incrementing view count: {str(e)}")
            return Response(
                {'error': 'Failed to increment view count'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def increment_download(self, request, pk=None):
        """Increment download count"""
        try:
            resource = self.get_object()
            resource.increment_download_count()
            logger.info(f"Incremented download count for resource {resource.id}")
            return Response({'message': 'Download count incremented'})
        except Exception as e:
            logger.error(f"Error incrementing download count: {str(e)}")
            return Response(
                {'error': 'Failed to increment download count'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StudyAbroadEventViewSet(viewsets.ModelViewSet):
    """ViewSet for StudyAbroadEvent model"""
    queryset = StudyAbroadEvent.objects.all()
    serializer_class = StudyAbroadEventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['event_type', 'is_active', 'is_featured', 'is_virtual']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['start_datetime', 'end_datetime', 'created_at']
    ordering = ['start_datetime']

    @action(detail=False, methods=['get'])
    def upcoming_events(self, request):
        """Get upcoming events"""
        try:
            upcoming = self.queryset.filter(
                start_datetime__gte=timezone.now(),
                is_active=True
            )
            serializer = self.get_serializer(upcoming, many=True)
            logger.info(f"Retrieved {upcoming.count()} upcoming events")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving upcoming events: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve upcoming events'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def featured_events(self, request):
        """Get featured events"""
        try:
            featured = self.queryset.filter(is_featured=True, is_active=True)
            serializer = self.get_serializer(featured, many=True)
            logger.info(f"Retrieved {featured.count()} featured events")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving featured events: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve featured events'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get events by type"""
        try:
            event_type = request.query_params.get('type')
            if event_type:
                events = self.queryset.filter(event_type=event_type, is_active=True)
                serializer = self.get_serializer(events, many=True)
                logger.info(f"Retrieved {events.count()} events of type: {event_type}")
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'Type parameter is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Error retrieving events by type: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve events by type'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StudyAbroadEventRegistrationViewSet(viewsets.ModelViewSet):
    """ViewSet for StudyAbroadEventRegistration model"""
    serializer_class = StudyAbroadEventRegistrationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'event', 'status']
    search_fields = ['dietary_restrictions', 'special_accommodations', 'questions']
    ordering_fields = ['registration_date', 'attendance_date', 'created_at']
    ordering = ['-registration_date']

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_staff:
            return StudyAbroadEventRegistration.objects.all()
        return StudyAbroadEventRegistration.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set user to current user when creating"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_registrations(self, request):
        """Get current user's event registrations"""
        try:
            registrations = self.get_queryset().filter(user=request.user)
            serializer = self.get_serializer(registrations, many=True)
            logger.info(f"Retrieved {registrations.count()} registrations for user {request.user.username}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving user registrations: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve registrations'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def mark_attended(self, request, pk=None):
        """Mark registration as attended"""
        try:
            registration = self.get_object()
            registration.mark_attended()
            logger.info(f"Registration {registration.id} marked as attended")
            return Response({'message': 'Registration marked as attended'})
        except Exception as e:
            logger.error(f"Error marking registration as attended: {str(e)}")
            return Response(
                {'error': 'Failed to mark registration as attended'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
