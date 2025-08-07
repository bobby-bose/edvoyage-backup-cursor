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
    Content, ContentCategory, ContentTag, ContentView, ContentRating,
    ContentComment, ContentShare, ContentDownload, ContentBookmark, ContentAnalytics
)
from .serializers import (
    ContentSerializer, ContentListSerializer, ContentCreateSerializer, ContentUpdateSerializer,
    ContentCategorySerializer, ContentCategoryListSerializer,
    ContentTagSerializer, ContentTagListSerializer,
    ContentViewSerializer, ContentRatingSerializer, ContentRatingCreateSerializer,
    ContentCommentSerializer, ContentCommentCreateSerializer,
    ContentShareSerializer, ContentShareCreateSerializer,
    ContentDownloadSerializer, ContentDownloadCreateSerializer,
    ContentBookmarkSerializer, ContentBookmarkCreateSerializer,
    ContentAnalyticsSerializer, ContentSearchSerializer,
    ContentStatisticsSerializer, ContentViewCreateSerializer,
    ContentBulkActionSerializer, ContentExportSerializer, ContentImportSerializer
)

from rest_framework import generics
from .models import Feed
from .serializers import FeedSerializer

# Set up logging
logger = logging.getLogger(__name__)

class ContentCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for content categories"""
    queryset = ContentCategory.objects.all()
    serializer_class = ContentCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'content_count']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return ContentCategoryListSerializer
        return ContentCategorySerializer

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            # Show user's categories and public categories
            queryset = queryset.filter(
                Q(is_active=True)
            )
        else:
            # Show only public categories
            queryset = queryset.filter(is_active=True)
        return queryset.prefetch_related('contents')

    @action(detail=True, methods=['get'])
    def contents(self, request, pk=None):
        """Get contents in a category"""
        category = self.get_object()
        contents = category.contents.filter(is_active=True)
        
        # Apply pagination
        paginator = Paginator(contents, 25)
        page_number = request.query_params.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        serializer = ContentListSerializer(page_obj, many=True)
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
        contents = category.contents.all()
        
        stats = {
            'total_contents': contents.count(),
            'total_views': sum(content.view_count for content in contents),
            'total_downloads': sum(content.download_count for content in contents),
            'total_shares': sum(content.share_count for content in contents),
            'average_rating': contents.aggregate(avg=Avg('average_rating'))['avg'] or 0,
        }
        
        return Response(stats)

class ContentTagViewSet(viewsets.ModelViewSet):
    """ViewSet for content tags"""
    queryset = ContentTag.objects.all()
    serializer_class = ContentTagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'content_count']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return ContentTagListSerializer
        return ContentTagSerializer

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = super().get_queryset()
        return queryset.prefetch_related('contents')

    @action(detail=True, methods=['get'])
    def contents(self, request, pk=None):
        """Get contents with this tag"""
        tag = self.get_object()
        contents = tag.contents.filter(is_active=True)
        
        # Apply pagination
        paginator = Paginator(contents, 25)
        page_number = request.query_params.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        serializer = ContentListSerializer(page_obj, many=True)
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'next': page_obj.has_next(),
            'previous': page_obj.has_previous(),
            'page': page_obj.number,
            'pages': paginator.num_pages
        })

class ContentViewSet(viewsets.ModelViewSet):
    """ViewSet for content"""
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'content_type', 'is_public', 'is_featured', 'is_premium', 'category']
    search_fields = ['title', 'description', 'meta_title', 'meta_description', 'keywords']
    ordering_fields = ['created_at', 'updated_at', 'view_count', 'download_count', 'share_count', 'average_rating']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ContentListSerializer
        elif self.action == 'create':
            return ContentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ContentUpdateSerializer
        return ContentSerializer

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = super().get_queryset()
        
        # Apply filters
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        content_type = self.request.query_params.get('content_type')
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        is_public = self.request.query_params.get('is_public')
        if is_public is not None:
            queryset = queryset.filter(is_public=is_public.lower() == 'true')
        
        is_featured = self.request.query_params.get('is_featured')
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')
        
        is_premium = self.request.query_params.get('is_premium')
        if is_premium is not None:
            queryset = queryset.filter(is_premium=is_premium.lower() == 'true')
        
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author_id=author)
        
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__id__in=tags)
        
        if self.request.user.is_authenticated:
            # Show user's contents and public contents
            queryset = queryset.filter(
                Q(author=self.request.user) | Q(is_public=True, status='published')
            )
        else:
            # Show only public published contents
            queryset = queryset.filter(is_public=True, status='published')
        
        return queryset.select_related('category', 'author').prefetch_related('tags')

    def perform_create(self, serializer):
        """Create content with current user as author"""
        serializer.save(author=self.request.user)
        logger.info(f"Content created: {serializer.instance.title} by {self.request.user.username}")

    def perform_update(self, serializer):
        """Update content with logging"""
        old_title = self.get_object().title
        serializer.save()
        logger.info(f"Content updated: {old_title} -> {serializer.instance.title} by {self.request.user.username}")

    def perform_destroy(self, instance):
        """Delete content with logging"""
        title = instance.title
        super().perform_destroy(instance)
        logger.info(f"Content deleted: {title} by {self.request.user.username}")

    @action(detail=True, methods=['post'])
    def view(self, request, pk=None):
        """Track content view"""
        content = self.get_object()
        
        # Create view record
        view_data = {
            'content': content,
            'user': request.user if request.user.is_authenticated else None,
            'ip_address': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'referrer': request.META.get('HTTP_REFERER', ''),
            'session_id': request.session.session_key or '',
        }
        
        view = ContentView.objects.create(**view_data)
        
        # Update content view count
        content.view_count += 1
        content.save()
        
        # Track analytics
        ContentAnalytics.objects.create(
            content=content,
            user=request.user if request.user.is_authenticated else None,
            action_type='view',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            referrer=request.META.get('HTTP_REFERER', '')
        )
        
        serializer = ContentViewSerializer(view)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        """Rate content"""
        content = self.get_object()
        serializer = ContentRatingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if user already rated this content
        existing_rating = ContentRating.objects.filter(
            content=content,
            user=request.user
        ).first()
        
        if existing_rating:
            # Update existing rating
            existing_rating.rating = serializer.validated_data['rating']
            existing_rating.review = serializer.validated_data.get('review', '')
            existing_rating.is_helpful = serializer.validated_data.get('is_helpful', False)
            existing_rating.save()
            rating = existing_rating
        else:
            # Create new rating
            rating = serializer.save()
        
        # Track analytics
        ContentAnalytics.objects.create(
            content=content,
            user=request.user,
            action_type='rate',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            metadata={'rating': rating.rating}
        )
        
        return Response({'message': 'Content rated successfully'})

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        """Add comment to content"""
        content = self.get_object()
        serializer = ContentCommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        comment = serializer.save()
        
        # Track analytics
        ContentAnalytics.objects.create(
            content=content,
            user=request.user,
            action_type='comment',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            metadata={'comment_id': comment.id}
        )
        
        return Response({'message': 'Comment added successfully'})

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """Share content"""
        content = self.get_object()
        serializer = ContentShareCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        share = serializer.save()
        
        # Update content share count
        content.share_count += 1
        content.save()
        
        # Track analytics
        ContentAnalytics.objects.create(
            content=content,
            user=request.user,
            action_type='share',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            metadata={'share_type': share.share_type}
        )
        
        return Response({'message': 'Content shared successfully'})

    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        """Track content download"""
        content = self.get_object()
        serializer = ContentDownloadCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        download = serializer.save()
        
        # Update content download count
        content.download_count += 1
        content.save()
        
        # Track analytics
        ContentAnalytics.objects.create(
            content=content,
            user=request.user,
            action_type='download',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            metadata={'download_url': download.download_url}
        )
        
        return Response({'message': 'Download tracked successfully'})

    @action(detail=True, methods=['post'])
    def bookmark(self, request, pk=None):
        """Bookmark content"""
        content = self.get_object()
        serializer = ContentBookmarkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        bookmark = serializer.save()
        
        # Track analytics
        ContentAnalytics.objects.create(
            content=content,
            user=request.user,
            action_type='bookmark',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({'message': 'Content bookmarked successfully'})

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get content comments"""
        content = self.get_object()
        comments = content.comments.filter(is_approved=True, parent=None).order_by('-created_at')
        
        # Apply pagination
        paginator = Paginator(comments, 25)
        page_number = request.query_params.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        serializer = ContentCommentSerializer(page_obj, many=True)
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'next': page_obj.has_next(),
            'previous': page_obj.has_previous(),
            'page': page_obj.number,
            'pages': paginator.num_pages
        })

    @action(detail=True, methods=['get'])
    def ratings(self, request, pk=None):
        """Get content ratings"""
        content = self.get_object()
        ratings = content.ratings.all().order_by('-created_at')
        
        # Apply pagination
        paginator = Paginator(ratings, 25)
        page_number = request.query_params.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        serializer = ContentRatingSerializer(page_obj, many=True)
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'next': page_obj.has_next(),
            'previous': page_obj.has_previous(),
            'page': page_obj.number,
            'pages': paginator.num_pages
        })

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search contents"""
        serializer = ContentSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        queryset = self.get_queryset()
        
        # Apply search filters
        q = serializer.validated_data.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | 
                Q(description__icontains=q) |
                Q(meta_title__icontains=q) |
                Q(meta_description__icontains=q) |
                Q(keywords__icontains=q) |
                Q(category__name__icontains=q) |
                Q(author__username__icontains=q)
            )
        
        category = serializer.validated_data.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        content_type = serializer.validated_data.get('content_type')
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        
        status_filter = serializer.validated_data.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        is_public = serializer.validated_data.get('is_public')
        if is_public is not None:
            queryset = queryset.filter(is_public=is_public)
        
        is_featured = serializer.validated_data.get('is_featured')
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured)
        
        is_premium = serializer.validated_data.get('is_premium')
        if is_premium is not None:
            queryset = queryset.filter(is_premium=is_premium)
        
        author = serializer.validated_data.get('author')
        if author:
            queryset = queryset.filter(author_id=author)
        
        tags = serializer.validated_data.get('tags')
        if tags:
            queryset = queryset.filter(tags__id__in=tags)
        
        # Apply pagination
        paginator = Paginator(queryset, 25)
        page_number = request.query_params.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        serializer = ContentListSerializer(page_obj, many=True)
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
        """Get overall content statistics"""
        queryset = self.get_queryset()
        
        stats = {
            'total_content': queryset.count(),
            'total_views': queryset.aggregate(total=Sum('view_count'))['total'] or 0,
            'total_downloads': queryset.aggregate(total=Sum('download_count'))['total'] or 0,
            'total_shares': queryset.aggregate(total=Sum('share_count'))['total'] or 0,
            'average_rating': queryset.aggregate(avg=Avg('average_rating'))['avg'] or 0,
            'popular_content': ContentListSerializer(
                queryset.order_by('-view_count')[:5], many=True
            ).data,
            'recent_content': ContentListSerializer(
                queryset.order_by('-created_at')[:5], many=True
            ).data,
            'category_stats': []
        }
        
        # Category statistics
        categories = ContentCategory.objects.annotate(
            content_count=Count('contents'),
            total_views=Sum('contents__view_count'),
            total_downloads=Sum('contents__download_count'),
            avg_rating=Avg('contents__average_rating')
        )
        
        for category in categories:
            stats['category_stats'].append({
                'id': category.id,
                'name': category.name,
                'content_count': category.content_count,
                'total_views': category.total_views or 0,
                'total_downloads': category.total_downloads or 0,
                'average_rating': category.avg_rating or 0
            })
        
        return Response(stats)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured contents"""
        queryset = self.get_queryset().filter(is_featured=True)
        serializer = ContentListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent contents"""
        queryset = self.get_queryset().order_by('-created_at')[:10]
        serializer = ContentListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular contents"""
        queryset = self.get_queryset().order_by('-view_count')[:10]
        serializer = ContentListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def bulk_action(self, request):
        """Perform bulk actions on contents"""
        serializer = ContentBulkActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        content_ids = serializer.validated_data['content_ids']
        action = serializer.validated_data['action']
        
        contents = Content.objects.filter(id__in=content_ids, author=request.user)
        
        if action == 'publish':
            contents.update(status='published')
        elif action == 'archive':
            contents.update(status='archived')
        elif action == 'delete':
            contents.delete()
        elif action == 'feature':
            contents.update(is_featured=True)
        elif action == 'unfeature':
            contents.update(is_featured=False)
        elif action == 'make_public':
            contents.update(is_public=True)
        elif action == 'make_private':
            contents.update(is_public=False)
        
        return Response({'message': f'{contents.count()} contents {action}ed successfully'})

class ContentRatingViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for content ratings (read-only)"""
    serializer_class = ContentRatingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['content', 'rating', 'is_helpful']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter queryset to show only user's ratings"""
        return ContentRating.objects.filter(user=self.request.user).select_related('content', 'user')

class ContentCommentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for content comments (read-only)"""
    serializer_class = ContentCommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['content', 'is_approved', 'parent']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter queryset to show only user's comments"""
        return ContentComment.objects.filter(user=self.request.user).select_related('content', 'user', 'parent')

class ContentShareViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for content shares (read-only)"""
    serializer_class = ContentShareSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['content', 'share_type', 'is_viewed']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter queryset to show only shares by user"""
        return ContentShare.objects.filter(shared_by=self.request.user).select_related('content', 'shared_by', 'shared_with')

class ContentDownloadViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for content downloads (read-only)"""
    serializer_class = ContentDownloadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter queryset to show only user's downloads"""
        return ContentDownload.objects.filter(user=self.request.user).select_related('content', 'user')

class ContentBookmarkViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for content bookmarks (read-only)"""
    serializer_class = ContentBookmarkSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter queryset to show only user's bookmarks"""
        return ContentBookmark.objects.filter(user=self.request.user).select_related('content', 'user')

class ContentAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for content analytics (read-only)"""
    serializer_class = ContentAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['content', 'action_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter queryset to show only analytics for user's contents"""
        return ContentAnalytics.objects.filter(content__author=self.request.user).select_related('content', 'user')

class FeedListAPIView(generics.ListAPIView):
    queryset = Feed.objects.all().order_by('-date_posted')
    serializer_class = FeedSerializer
