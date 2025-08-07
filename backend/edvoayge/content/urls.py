from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ContentViewSet, ContentCategoryViewSet, ContentTagViewSet,
    ContentRatingViewSet, ContentCommentViewSet, ContentShareViewSet,
    ContentDownloadViewSet, ContentBookmarkViewSet, ContentAnalyticsViewSet,
    FeedListAPIView,
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'contents', ContentViewSet, basename='content')
router.register(r'categories', ContentCategoryViewSet, basename='content-category')
router.register(r'tags', ContentTagViewSet, basename='content-tag')
router.register(r'ratings', ContentRatingViewSet, basename='content-rating')
router.register(r'comments', ContentCommentViewSet, basename='content-comment')
router.register(r'shares', ContentShareViewSet, basename='content-share')
router.register(r'downloads', ContentDownloadViewSet, basename='content-download')
router.register(r'bookmarks', ContentBookmarkViewSet, basename='content-bookmark')
router.register(r'analytics', ContentAnalyticsViewSet, basename='content-analytics')

# URL patterns for content app
urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Content custom action URLs
    path('contents/<int:pk>/view/', ContentViewSet.as_view({'post': 'view'}), name='content-view'),
    path('contents/<int:pk>/rate/', ContentViewSet.as_view({'post': 'rate'}), name='content-rate'),
    path('contents/<int:pk>/comment/', ContentViewSet.as_view({'post': 'comment'}), name='content-comment'),
    path('contents/<int:pk>/share/', ContentViewSet.as_view({'post': 'share'}), name='content-share'),
    path('contents/<int:pk>/download/', ContentViewSet.as_view({'post': 'download'}), name='content-download'),
    path('contents/<int:pk>/bookmark/', ContentViewSet.as_view({'post': 'bookmark'}), name='content-bookmark'),
    path('contents/<int:pk>/comments/', ContentViewSet.as_view({'get': 'comments'}), name='content-comments'),
    path('contents/<int:pk>/ratings/', ContentViewSet.as_view({'get': 'ratings'}), name='content-ratings'),
    
    # Content list action URLs
    path('contents/search/', ContentViewSet.as_view({'get': 'search'}), name='content-search'),
    path('contents/statistics/', ContentViewSet.as_view({'get': 'statistics'}), name='content-statistics'),
    path('contents/featured/', ContentViewSet.as_view({'get': 'featured'}), name='content-featured'),
    path('contents/recent/', ContentViewSet.as_view({'get': 'recent'}), name='content-recent'),
    path('contents/popular/', ContentViewSet.as_view({'get': 'popular'}), name='content-popular'),
    path('contents/bulk-action/', ContentViewSet.as_view({'post': 'bulk_action'}), name='content-bulk-action'),
    
    # Category action URLs
    path('categories/<int:pk>/contents/', ContentCategoryViewSet.as_view({'get': 'contents'}), name='category-contents'),
    path('categories/<int:pk>/statistics/', ContentCategoryViewSet.as_view({'get': 'statistics'}), name='category-statistics'),
    
    # Tag action URLs
    path('tags/<int:pk>/contents/', ContentTagViewSet.as_view({'get': 'contents'}), name='tag-contents'),
    path('feeds/', FeedListAPIView.as_view(), name='feed-list'),
] 