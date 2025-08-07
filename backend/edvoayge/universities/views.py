"""
University views for EdVoyage API.
Handles university-related API endpoints with proper error handling and logging.
"""

import logging
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Avg, Min, Max
from django.utils import timezone
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    University, Campus, UniversityRanking, UniversityProgram,
    UniversityFaculty, UniversityResearch, UniversityPartnership, UniversityGallery
)
from .serializers import (
    UniversitySerializer, UniversityCreateSerializer, UniversityUpdateSerializer,
    CampusSerializer, CampusCreateSerializer, CampusUpdateSerializer,
    UniversityRankingSerializer, UniversityRankingCreateSerializer,
    UniversityProgramSerializer, UniversityProgramCreateSerializer,
    UniversityFacultySerializer, UniversityFacultyCreateSerializer,
    UniversityResearchSerializer, UniversityResearchCreateSerializer,
    UniversityPartnershipSerializer, UniversityPartnershipCreateSerializer,
    UniversitySearchSerializer, UniversityStatsSerializer, UniversityComparisonSerializer,
    UniversityGallerySerializer
)

logger = logging.getLogger(__name__)


class UniversityPagination(PageNumberPagination):
    """Custom pagination for university listings."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class UniversityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for university management.
    Provides CRUD operations for universities with search and filtering.
    """
    queryset = University.objects.select_related('gallery').prefetch_related(
        'campuses', 'rankings', 'programs', 'faculties', 'research', 'partnerships'
    )
    serializer_class = UniversitySerializer
    pagination_class = UniversityPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'university_type', 'country', 'state', 'city', 'is_active', 
        'is_featured', 'is_verified', 'founded_year'
    ]
    search_fields = [
        'name', 'short_name', 'description', 'country', 'city', 'state'
    ]
    ordering_fields = [
        'name', 'founded_year', 'total_students', 'international_students',
        'faculty_count', 'created_at', 'updated_at'
    ]
    ordering = ['name']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return UniversityCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UniversityUpdateSerializer
        return UniversitySerializer

    def get_queryset(self):
        """Filter queryset based on request parameters."""
        queryset = super().get_queryset()
        
        # Only show active universities in listing
        if self.action == 'list':
            queryset = queryset.filter(is_active=True)
        
        return queryset

    def list(self, request, *args, **kwargs):
        """List universities with enhanced filtering."""
        print("Entering UniversityListView") if hasattr(request, 'user') else None
        try:
            response = super().list(request, *args, **kwargs)
            print(f"[DEBUG] Response data: {response.data}")
            print(f"University list returned {len(response.data['results'])} universities") if hasattr(request, 'user') else None
            return response
        except Exception as e:
            logger.error(f"Error in university list: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving universities'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific university with all related data including gallery."""
        print(f"Entering UniversityRetrieveView for university ID: {kwargs.get('pk')}") if hasattr(request, 'user') else None
        try:
            university = self.get_object()
            serializer = self.get_serializer(university)
            
            # Add debug information about gallery
            if hasattr(university, 'gallery'):
                print(f"🔍 DEBUG: University {university.name} has gallery with images: {[getattr(university.gallery, f'image{i}', None) for i in range(1, 7)]}")
            else:
                print(f"🔍 DEBUG: University {university.name} has no gallery")
            
            print(f"University detail retrieved successfully: {university.name}") if hasattr(request, 'user') else None
            return Response({
                'success': True,
                'data': serializer.data,
                'message': f'University {university.name} retrieved successfully'
            })
        except Exception as e:
            logger.error(f"Error in university retrieve: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving university'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        """Create a new university."""
        print("Creating new university") if hasattr(request, 'user') else None
        try:
            response = super().create(request, *args, **kwargs)
            print(f"University created successfully: {response.data.get('name')}") if hasattr(request, 'user') else None
            return Response(
                {'success': True, 'data': response.data, 'message': 'University created successfully'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error creating university: {e}")
            return Response(
                {'success': False, 'message': 'Error creating university'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'], url_path='gallery')
    def gallery(self, request, pk=None):
        """Get university gallery images."""
        print(f"Entering UniversityGalleryView for university ID: {pk}") if hasattr(request, 'user') else None
        try:
            university = self.get_object()
            
            # Check if university has a gallery
            try:
                gallery = university.gallery
                serializer = UniversityGallerySerializer(gallery, context={'request': request})
                print(f"🔍 DEBUG: Gallery found for {university.name} with images: {[getattr(gallery, f'image{i}', None) for i in range(1, 7)]}")
                
                return Response({
                    'success': True,
                    'data': serializer.data,
                    'message': f'Gallery for {university.name}'
                })
            except UniversityGallery.DoesNotExist:
                print(f"🔍 DEBUG: No gallery found for {university.name}")
                return Response({
                    'success': True,
                    'data': None,
                    'message': f'No gallery found for {university.name}'
                })
                
        except Exception as e:
            logger.error(f"Error in university gallery: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving gallery'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='search')
    def search(self, request):
        """Advanced university search."""
        print("Entering UniversitySearchView") if hasattr(request, 'user') else None
        try:
            serializer = UniversitySearchSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            queryset = University.objects.filter(is_active=True)
            
            # Apply search filters
            query = serializer.validated_data.get('query')
            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) |
                    Q(short_name__icontains=query) |
                    Q(description__icontains=query) |
                    Q(country__icontains=query) |
                    Q(city__icontains=query)
                )
            
            country = serializer.validated_data.get('country')
            if country:
                queryset = queryset.filter(country__iexact=country)
            
            university_type = serializer.validated_data.get('university_type')
            if university_type:
                queryset = queryset.filter(university_type=university_type)
            
            # Ranking filters
            min_rank = serializer.validated_data.get('min_rank')
            max_rank = serializer.validated_data.get('max_rank')
            
            if min_rank or max_rank:
                ranking_filter = Q(rankings__isnull=False)
                if min_rank:
                    ranking_filter &= Q(rankings__rank__gte=min_rank)
                if max_rank:
                    ranking_filter &= Q(rankings__rank__lte=max_rank)
                queryset = queryset.filter(ranking_filter)
            
            # Program filters
            has_programs = serializer.validated_data.get('has_programs')
            if has_programs:
                queryset = queryset.filter(programs__isnull=False).distinct()
            
            # Status filters
            is_featured = serializer.validated_data.get('is_featured')
            if is_featured is not None:
                queryset = queryset.filter(is_featured=is_featured)
            
            is_verified = serializer.validated_data.get('is_verified')
            if is_verified is not None:
                queryset = queryset.filter(is_verified=is_verified)
            
            # Paginate results
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = UniversitySerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = UniversitySerializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': f'Found {len(serializer.data)} universities'
            })
        except Exception as e:
            logger.error(f"Error in university search: {e}")
            return Response(
                {'success': False, 'message': 'Error searching universities'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        """Get university statistics."""
        print("Entering UniversityStatsView") if hasattr(request, 'user') else None
        try:
            # Calculate statistics
            total_universities = University.objects.count()
            active_universities = University.objects.filter(is_active=True).count()
            featured_universities = University.objects.filter(is_featured=True).count()
            verified_universities = University.objects.filter(is_verified=True).count()
            
            # Universities by country
            universities_by_country = University.objects.values('country').annotate(
                count=Count('id')
            ).order_by('-count')
            
            # Universities by type
            universities_by_type = University.objects.values('university_type').annotate(
                count=Count('id')
            ).order_by('-count')
            
            # Top ranked universities
            top_ranked_universities = University.objects.filter(
                rankings__isnull=False
            ).annotate(
                min_rank=Min('rankings__rank')
            ).order_by('min_rank')[:10]
            
            # Recent universities
            recent_universities = University.objects.order_by('-created_at')[:10]
            
            data = {
                'total_universities': total_universities,
                'active_universities': active_universities,
                'featured_universities': featured_universities,
                'verified_universities': verified_universities,
                'universities_by_country': {item['country']: item['count'] for item in universities_by_country},
                'universities_by_type': {item['university_type']: item['count'] for item in universities_by_type},
                'top_ranked_universities': UniversitySerializer(top_ranked_universities, many=True).data,
                'recent_universities': UniversitySerializer(recent_universities, many=True).data,
            }
            
            print(f"University stats calculated successfully") if hasattr(request, 'user') else None
            return Response(
                {'success': True, 'data': data, 'message': 'Statistics retrieved successfully'}
            )
        except Exception as e:
            logger.error(f"Error in university stats: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving statistics'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='compare')
    def compare(self, request):
        """Compare multiple universities."""
        print("Entering UniversityCompareView") if hasattr(request, 'user') else None
        try:
            university_ids = request.data.get('university_ids', [])
            if len(university_ids) < 2 or len(university_ids) > 5:
                return Response(
                    {'success': False, 'message': 'Please select 2-5 universities to compare'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            universities = University.objects.filter(id__in=university_ids)
            if len(universities) != len(university_ids):
                return Response(
                    {'success': False, 'message': 'Some universities not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Prepare comparison data
            comparison_data = {
                'total_count': len(universities),
                'countries': list(set(uni.country for uni in universities)),
                'types': list(set(uni.university_type for uni in universities)),
            }
            
            # Ranking comparison
            ranking_comparison = []
            for university in universities:
                rankings = university.rankings.all()
                ranking_data = {
                    'university_id': university.id,
                    'university_name': university.name,
                    'rankings': UniversityRankingSerializer(rankings, many=True).data
                }
                ranking_comparison.append(ranking_data)
            
            # Program comparison
            program_comparison = []
            for university in universities:
                programs = university.programs.all()
                program_data = {
                    'university_id': university.id,
                    'university_name': university.name,
                    'programs': UniversityProgramSerializer(programs, many=True).data
                }
                program_comparison.append(program_data)
            
            data = {
                'universities': UniversitySerializer(universities, many=True).data,
                'comparison_data': comparison_data,
                'ranking_comparison': ranking_comparison,
                'program_comparison': program_comparison,
            }
            
            print(f"University comparison completed for {len(universities)} universities") if hasattr(request, 'user') else None
            return Response(
                {'success': True, 'data': data, 'message': 'Comparison completed successfully'}
            )
        except Exception as e:
            logger.error(f"Error in university comparison: {e}")
            return Response(
                {'success': False, 'message': 'Error comparing universities'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'], url_path='rankings')
    def rankings(self, request, pk=None):
        """Get university rankings."""
        print("Entering UniversityRankingsView") if hasattr(request, 'user') else None
        try:
            university = self.get_object()
            rankings = university.rankings.all().order_by('-year', 'ranking_type')
            
            serializer = UniversityRankingSerializer(rankings, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': f'Rankings for {university.name}'
            })
        except Exception as e:
            logger.error(f"Error in university rankings: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving rankings'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'], url_path='programs')
    def programs(self, request, pk=None):
        """Get university programs."""
        print("Entering UniversityProgramsView") if hasattr(request, 'user') else None
        try:
            university = self.get_object()
            programs = university.programs.filter(is_active=True).order_by('program_level', 'name')
            
            serializer = UniversityProgramSerializer(programs, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': f'Programs for {university.name}'
            })
        except Exception as e:
            logger.error(f"Error in university programs: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving programs'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CampusViewSet(viewsets.ModelViewSet):
    """ViewSet for campus management."""
    queryset = Campus.objects.select_related('university')
    serializer_class = CampusSerializer
    pagination_class = UniversityPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['campus_type', 'country', 'state', 'city', 'is_active', 'is_main_campus']
    search_fields = ['name', 'university__name', 'city', 'country']
    ordering = ['university__name', 'name']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return CampusCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CampusUpdateSerializer
        return CampusSerializer

    def get_queryset(self):
        """Filter queryset based on request parameters."""
        queryset = super().get_queryset()
        
        # Only show active campuses in listing
        if self.action == 'list':
            queryset = queryset.filter(is_active=True)
        
        return queryset

    def list(self, request, *args, **kwargs):
        """List campuses with enhanced filtering."""
        print("Entering CampusListView") if hasattr(request, 'user') else None
        try:
            response = super().list(request, *args, **kwargs)
            print(f"Campus list returned {len(response.data['results'])} campuses") if hasattr(request, 'user') else None
            return response
        except Exception as e:
            logger.error(f"Error in campus list: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving campuses'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UniversityRankingViewSet(viewsets.ModelViewSet):
    """ViewSet for university ranking management."""
    queryset = UniversityRanking.objects.select_related('university')
    serializer_class = UniversityRankingSerializer
    pagination_class = UniversityPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ranking_type', 'ranking_source', 'year', 'university']
    ordering_fields = ['rank', 'year', 'score']
    ordering = ['-year', 'rank']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return UniversityRankingCreateSerializer
        return UniversityRankingSerializer

    def list(self, request, *args, **kwargs):
        """List rankings with enhanced filtering."""
        print("Entering UniversityRankingListView") if hasattr(request, 'user') else None
        try:
            response = super().list(request, *args, **kwargs)
            print(f"Ranking list returned {len(response.data['results'])} rankings") if hasattr(request, 'user') else None
            return response
        except Exception as e:
            logger.error(f"Error in ranking list: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving rankings'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UniversityProgramViewSet(viewsets.ModelViewSet):
    """ViewSet for university program management."""
    queryset = UniversityProgram.objects.select_related('university')
    serializer_class = UniversityProgramSerializer
    pagination_class = UniversityPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['program_level', 'program_type', 'is_active', 'is_featured', 'university']
    search_fields = ['name', 'description', 'university__name']
    ordering_fields = ['name', 'duration_years', 'total_credits']
    ordering = ['university__name', 'program_level', 'name']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return UniversityProgramCreateSerializer
        return UniversityProgramSerializer

    def get_queryset(self):
        """Filter queryset based on request parameters."""
        queryset = super().get_queryset()
        
        # Only show active programs in listing
        if self.action == 'list':
            queryset = queryset.filter(is_active=True)
        
        return queryset

    def list(self, request, *args, **kwargs):
        """List programs with enhanced filtering."""
        print("Entering UniversityProgramListView") if hasattr(request, 'user') else None
        try:
            response = super().list(request, *args, **kwargs)
            print(f"Program list returned {len(response.data['results'])} programs") if hasattr(request, 'user') else None
            return response
        except Exception as e:
            logger.error(f"Error in program list: {e}")
            return Response(
                {'success': False, 'message': 'Error retrieving programs'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UniversityFacultyViewSet(viewsets.ModelViewSet):
    """ViewSet for university faculty management."""
    queryset = UniversityFaculty.objects.select_related('university')
    serializer_class = UniversityFacultySerializer
    pagination_class = UniversityPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active', 'university']
    search_fields = ['name', 'short_name', 'description', 'university__name']
    ordering = ['university__name', 'name']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return UniversityFacultyCreateSerializer
        return UniversityFacultySerializer

    def get_queryset(self):
        """Filter queryset based on request parameters."""
        queryset = super().get_queryset()
        
        # Only show active faculties in listing
        if self.action == 'list':
            queryset = queryset.filter(is_active=True)
        
        return queryset


class UniversityResearchViewSet(viewsets.ModelViewSet):
    """ViewSet for university research management."""
    queryset = UniversityResearch.objects.select_related('university')
    serializer_class = UniversityResearchSerializer
    pagination_class = UniversityPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['research_area', 'status', 'university']
    search_fields = ['title', 'description', 'university__name']
    ordering_fields = ['start_date', 'end_date', 'funding_amount']
    ordering = ['-start_date', 'title']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return UniversityResearchCreateSerializer
        return UniversityResearchSerializer


class UniversityPartnershipViewSet(viewsets.ModelViewSet):
    """ViewSet for university partnership management."""
    queryset = UniversityPartnership.objects.select_related('university')
    serializer_class = UniversityPartnershipSerializer
    pagination_class = UniversityPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['partnership_type', 'status', 'university']
    search_fields = ['partner_name', 'description', 'university__name']
    ordering_fields = ['start_date', 'end_date', 'partner_name']
    ordering = ['-start_date', 'partner_name']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return UniversityPartnershipCreateSerializer
        return UniversityPartnershipSerializer
