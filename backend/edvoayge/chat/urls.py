from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChatUserViewSet, ChatRoomViewSet, MessageViewSet, 
    MessageStatusViewSet, ContactViewSet, ChatNotificationViewSet,
    SearchViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', ChatUserViewSet, basename='chat-user')
router.register(r'rooms', ChatRoomViewSet, basename='chat-room')
router.register(r'messages', MessageViewSet, basename='chat-message')
router.register(r'message-status', MessageStatusViewSet, basename='chat-message-status')
router.register(r'contacts', ContactViewSet, basename='chat-contact')
router.register(r'notifications', ChatNotificationViewSet, basename='chat-notification')
router.register(r'search', SearchViewSet, basename='chat-search')

app_name = 'chat'

urlpatterns = [
    # Include router URLs
    path('api/', include(router.urls)),
    
    # Additional custom endpoints
    path('api/users/<uuid:pk>/status/', ChatUserViewSet.as_view({'get': 'status', 'put': 'status', 'patch': 'status'}), name='user-status'),
    path('api/users/search/', ChatUserViewSet.as_view({'get': 'search'}), name='user-search'),
    path('api/rooms/<uuid:pk>/participants/', ChatRoomViewSet.as_view({'get': 'participants'}), name='room-participants'),
    path('api/rooms/<uuid:pk>/add-participant/', ChatRoomViewSet.as_view({'post': 'add_participant'}), name='room-add-participant'),
    path('api/rooms/<uuid:pk>/remove-participant/<uuid:user_id>/', ChatRoomViewSet.as_view({'delete': 'remove_participant'}), name='room-remove-participant'),
    path('api/messages/<uuid:pk>/reply/', MessageViewSet.as_view({'post': 'reply'}), name='message-reply'),
    path('api/messages/search/', MessageViewSet.as_view({'get': 'search'}), name='message-search'),
    path('api/message-status/<uuid:pk>/mark-read/', MessageStatusViewSet.as_view({'post': 'mark_read'}), name='message-mark-read'),
    path('api/contacts/<uuid:pk>/favorite/', ContactViewSet.as_view({'post': 'favorite'}), name='contact-favorite'),
    path('api/contacts/<uuid:pk>/block/', ContactViewSet.as_view({'post': 'block'}), name='contact-block'),
    path('api/notifications/<uuid:pk>/read/', ChatNotificationViewSet.as_view({'put': 'read', 'patch': 'read'}), name='notification-read'),
    path('api/notifications/read-all/', ChatNotificationViewSet.as_view({'put': 'read_all'}), name='notifications-read-all'),
    path('api/notifications/unread-count/', ChatNotificationViewSet.as_view({'get': 'unread_count'}), name='notifications-unread-count'),
    path('api/search/users/', SearchViewSet.as_view({'get': 'users'}), name='search-users'),
    path('api/search/messages/', SearchViewSet.as_view({'get': 'messages'}), name='search-messages'),
] 