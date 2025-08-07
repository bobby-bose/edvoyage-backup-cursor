from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers
from .views import (
    BookmarkViewSet,
    BookmarkCategoryViewSet,
    BookmarkNoteViewSet,
    BookmarkCollectionViewSet,
    BookmarkShareViewSet,
    BookmarkAnalyticsViewSet,
    BookmarkTagViewSet,
    BookmarkAccessLogViewSet,
    BookmarkSearchViewSet,
    BookmarkStatsViewSet,
    BookmarkDashboardViewSet,
)

# Create the main router
router = DefaultRouter()
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')
router.register(r'categories', BookmarkCategoryViewSet, basename='bookmarkcategory')
router.register(r'collections', BookmarkCollectionViewSet, basename='bookmarkcollection')
router.register(r'shares', BookmarkShareViewSet, basename='bookmarkshare')
router.register(r'analytics', BookmarkAnalyticsViewSet, basename='bookmarkanalytics')
router.register(r'tags', BookmarkTagViewSet, basename='bookmarktag')
router.register(r'access-logs', BookmarkAccessLogViewSet, basename='bookmarkaccesslog')
router.register(r'search', BookmarkSearchViewSet, basename='bookmarksearch')
router.register(r'stats', BookmarkStatsViewSet, basename='bookmarkstats')
router.register(r'dashboard', BookmarkDashboardViewSet, basename='bookmarkdashboard')

# Create nested routers for related models
bookmarks_router = routers.NestedDefaultRouter(router, r'bookmarks', lookup='bookmark')
bookmarks_router.register(r'notes', BookmarkNoteViewSet, basename='bookmark-notes')
bookmarks_router.register(r'access-logs', BookmarkAccessLogViewSet, basename='bookmark-access-logs')

collections_router = routers.NestedDefaultRouter(router, r'collections', lookup='collection')
collections_router.register(r'bookmarks', BookmarkViewSet, basename='collection-bookmarks')

categories_router = routers.NestedDefaultRouter(router, r'categories', lookup='category')
categories_router.register(r'bookmarks', BookmarkViewSet, basename='category-bookmarks')

# URL patterns
urlpatterns = [
    # Main API endpoints
    path('api/bookmarks/', include(router.urls)),
    
    # Nested endpoints
    path('api/bookmarks/', include(bookmarks_router.urls)),
    path('api/bookmarks/', include(collections_router.urls)),
    path('api/bookmarks/', include(categories_router.urls)),
    
    # Additional endpoints for specific functionality
    path('api/bookmarks/<uuid:bookmark_id>/record-access/', 
         BookmarkViewSet.as_view({'post': 'record_access'}), 
         name='bookmark-record-access'),
    
    path('api/bookmarks/<uuid:bookmark_id>/share/', 
         BookmarkViewSet.as_view({'post': 'share_bookmark'}), 
         name='bookmark-share'),
    
    path('api/bookmarks/<uuid:bookmark_id>/unshare/', 
         BookmarkViewSet.as_view({'post': 'unshare_bookmark'}), 
         name='bookmark-unshare'),
    
    path('api/bookmarks/<uuid:bookmark_id>/toggle-favorite/', 
         BookmarkViewSet.as_view({'post': 'toggle_favorite'}), 
         name='bookmark-toggle-favorite'),
    
    path('api/bookmarks/<uuid:bookmark_id>/add-note/', 
         BookmarkViewSet.as_view({'post': 'add_note'}), 
         name='bookmark-add-note'),
    
    path('api/bookmarks/<uuid:bookmark_id>/remove-note/', 
         BookmarkViewSet.as_view({'delete': 'remove_note'}), 
         name='bookmark-remove-note'),
    
    path('api/bookmarks/<uuid:bookmark_id>/add-tags/', 
         BookmarkViewSet.as_view({'post': 'add_tags'}), 
         name='bookmark-add-tags'),
    
    path('api/bookmarks/<uuid:bookmark_id>/remove-tags/', 
         BookmarkViewSet.as_view({'delete': 'remove_tags'}), 
         name='bookmark-remove-tags'),
    
    path('api/bookmarks/<uuid:bookmark_id>/move-to-collection/', 
         BookmarkViewSet.as_view({'post': 'move_to_collection'}), 
         name='bookmark-move-to-collection'),
    
    path('api/bookmarks/<uuid:bookmark_id>/copy-to-collection/', 
         BookmarkViewSet.as_view({'post': 'copy_to_collection'}), 
         name='bookmark-copy-to-collection'),
    
    # Collection-specific endpoints
    path('api/collections/<uuid:collection_id>/add-bookmark/', 
         BookmarkCollectionViewSet.as_view({'post': 'add_bookmark'}), 
         name='collection-add-bookmark'),
    
    path('api/collections/<uuid:collection_id>/remove-bookmark/', 
         BookmarkCollectionViewSet.as_view({'delete': 'remove_bookmark'}), 
         name='collection-remove-bookmark'),
    
    path('api/collections/<uuid:collection_id>/share/', 
         BookmarkCollectionViewSet.as_view({'post': 'share_collection'}), 
         name='collection-share'),
    
    path('api/collections/<uuid:collection_id>/unshare/', 
         BookmarkCollectionViewSet.as_view({'post': 'unshare_collection'}), 
         name='collection-unshare'),
    
    # Category-specific endpoints
    path('api/categories/<uuid:category_id>/bookmarks/', 
         BookmarkCategoryViewSet.as_view({'get': 'bookmarks'}), 
         name='category-bookmarks'),
    
    path('api/categories/<uuid:category_id>/stats/', 
         BookmarkCategoryViewSet.as_view({'get': 'stats'}), 
         name='category-stats'),
    
    # Search and analytics endpoints
    path('api/bookmarks/search/advanced/', 
         BookmarkSearchViewSet.as_view({'get': 'advanced_search'}), 
         name='bookmark-advanced-search'),
    
    path('api/bookmarks/search/suggestions/', 
         BookmarkSearchViewSet.as_view({'get': 'search_suggestions'}), 
         name='bookmark-search-suggestions'),
    
    path('api/bookmarks/stats/overview/', 
         BookmarkStatsViewSet.as_view({'get': 'overview'}), 
         name='bookmark-stats-overview'),
    
    path('api/bookmarks/stats/trends/', 
         BookmarkStatsViewSet.as_view({'get': 'trends'}), 
         name='bookmark-stats-trends'),
    
    path('api/bookmarks/stats/activity/', 
         BookmarkStatsViewSet.as_view({'get': 'activity'}), 
         name='bookmark-stats-activity'),
    
    # Dashboard endpoints
    path('api/bookmarks/dashboard/recent/', 
         BookmarkDashboardViewSet.as_view({'get': 'recent_bookmarks'}), 
         name='bookmark-dashboard-recent'),
    
    path('api/bookmarks/dashboard/favorites/', 
         BookmarkDashboardViewSet.as_view({'get': 'favorite_bookmarks'}), 
         name='bookmark-dashboard-favorites'),
    
    path('api/bookmarks/dashboard/collections/', 
         BookmarkDashboardViewSet.as_view({'get': 'user_collections'}), 
         name='bookmark-dashboard-collections'),
    
    path('api/bookmarks/dashboard/activity/', 
         BookmarkDashboardViewSet.as_view({'get': 'recent_activity'}), 
         name='bookmark-dashboard-activity'),
    
    path('api/bookmarks/dashboard/suggestions/', 
         BookmarkDashboardViewSet.as_view({'get': 'suggestions'}), 
         name='bookmark-dashboard-suggestions'),
    
    # Share-specific endpoints
    path('api/shares/<uuid:share_id>/access/', 
         BookmarkShareViewSet.as_view({'post': 'record_access'}), 
         name='share-record-access'),
    
    path('api/shares/<uuid:share_id>/revoke/', 
         BookmarkShareViewSet.as_view({'post': 'revoke_access'}), 
         name='share-revoke-access'),
    
    path('api/shares/<uuid:share_id>/extend/', 
         BookmarkShareViewSet.as_view({'post': 'extend_expiry'}), 
         name='share-extend-expiry'),
    
    # Analytics endpoints
    path('api/analytics/bookmarks/<uuid:bookmark_id>/', 
         BookmarkAnalyticsViewSet.as_view({'get': 'bookmark_analytics'}), 
         name='bookmark-analytics-detail'),
    
    path('api/analytics/collections/<uuid:collection_id>/', 
         BookmarkAnalyticsViewSet.as_view({'get': 'collection_analytics'}), 
         name='collection-analytics-detail'),
    
    path('api/analytics/user/<uuid:user_id>/', 
         BookmarkAnalyticsViewSet.as_view({'get': 'user_analytics'}), 
         name='user-analytics-detail'),
    
    path('api/analytics/overview/', 
         BookmarkAnalyticsViewSet.as_view({'get': 'overview'}), 
         name='analytics-overview'),
    
    path('api/analytics/trends/', 
         BookmarkAnalyticsViewSet.as_view({'get': 'trends'}), 
         name='analytics-trends'),
    
    path('api/analytics/export/', 
         BookmarkAnalyticsViewSet.as_view({'get': 'export_data'}), 
         name='analytics-export'),
] 