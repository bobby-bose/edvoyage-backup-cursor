from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, PostViewSet, CommentViewSet, 
    NotificationViewSet, SearchViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'search', SearchViewSet, basename='search')

app_name = 'cavity'

urlpatterns = [
    # Include router URLs
    path('api/', include(router.urls)),
    
    # Additional custom endpoints
    path('api/auth/profile/', UserViewSet.as_view({'get': 'profile', 'put': 'update_profile', 'patch': 'update_profile'}), name='auth-profile'),
    path('api/users/<uuid:pk>/posts/', UserViewSet.as_view({'get': 'posts'}), name='user-posts'),
    path('api/users/<uuid:pk>/likes/', UserViewSet.as_view({'get': 'likes'}), name='user-likes'),
    path('api/users/<uuid:pk>/follow/', UserViewSet.as_view({'post': 'follow', 'delete': 'follow'}), name='user-follow'),
    path('api/posts/<uuid:pk>/comments/', PostViewSet.as_view({'get': 'comments'}), name='post-comments'),
    path('api/posts/<uuid:pk>/likes/', PostViewSet.as_view({'get': 'likes'}), name='post-likes'),
    path('api/posts/<uuid:pk>/like/', PostViewSet.as_view({'post': 'like', 'delete': 'like'}), name='post-like'),
    path('api/posts/<uuid:pk>/share/', PostViewSet.as_view({'post': 'share'}), name='post-share'),
    path('api/comments/<uuid:pk>/replies/', CommentViewSet.as_view({'get': 'replies'}), name='comment-replies'),
    path('api/comments/<uuid:pk>/likes/', CommentViewSet.as_view({'get': 'likes'}), name='comment-likes'),
    path('api/comments/<uuid:pk>/like/', CommentViewSet.as_view({'post': 'like', 'delete': 'like'}), name='comment-like'),
    path('api/notifications/<uuid:pk>/read/', NotificationViewSet.as_view({'put': 'read', 'patch': 'read'}), name='notification-read'),
    path('api/notifications/read-all/', NotificationViewSet.as_view({'put': 'read_all'}), name='notifications-read-all'),
    path('api/notifications/unread-count/', NotificationViewSet.as_view({'get': 'unread_count'}), name='notifications-unread-count'),
    path('api/search/posts/', SearchViewSet.as_view({'get': 'posts'}), name='search-posts'),
    path('api/search/users/', SearchViewSet.as_view({'get': 'users'}), name='search-users'),
] 