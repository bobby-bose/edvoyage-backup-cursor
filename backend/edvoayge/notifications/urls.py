from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NotificationTemplateViewSet,
    NotificationChannelViewSet,
    NotificationViewSet,
    NotificationPreferenceViewSet,
    NotificationBatchViewSet,
    NotificationLogViewSet,
    NotificationScheduleViewSet,
    NotificationStatsViewSet,
)

# Create the main router
router = DefaultRouter()
router.register(r'templates', NotificationTemplateViewSet, basename='notificationtemplate')
router.register(r'channels', NotificationChannelViewSet, basename='notificationchannel')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'preferences', NotificationPreferenceViewSet, basename='notificationpreference')
router.register(r'batches', NotificationBatchViewSet, basename='notificationbatch')
router.register(r'logs', NotificationLogViewSet, basename='notificationlog')
router.register(r'schedules', NotificationScheduleViewSet, basename='notificationschedule')
router.register(r'stats', NotificationStatsViewSet, basename='notificationstats')

# URL patterns
urlpatterns = [
    # Main API endpoints
    path('api/notifications/', include(router.urls)),
    
    # Template specific endpoints
    path('api/notifications/templates/<uuid:pk>/test/',
         NotificationTemplateViewSet.as_view({'post': 'test_template'}),
         name='template-test'),
    
    path('api/notifications/templates/<uuid:pk>/duplicate/',
         NotificationTemplateViewSet.as_view({'post': 'duplicate_template'}),
         name='template-duplicate'),
    
    path('api/notifications/templates/by-category/',
         NotificationTemplateViewSet.as_view({'get': 'by_category'}),
         name='template-by-category'),
    
    path('api/notifications/templates/by-type/',
         NotificationTemplateViewSet.as_view({'get': 'by_type'}),
         name='template-by-type'),
    
    # Channel specific endpoints
    path('api/notifications/channels/<uuid:pk>/test/',
         NotificationChannelViewSet.as_view({'post': 'test_channel'}),
         name='channel-test'),
    
    path('api/notifications/channels/<uuid:pk>/set-default/',
         NotificationChannelViewSet.as_view({'post': 'set_default'}),
         name='channel-set-default'),
    
    path('api/notifications/channels/defaults/',
         NotificationChannelViewSet.as_view({'get': 'defaults'}),
         name='channel-defaults'),
    
    path('api/notifications/channels/by-type/',
         NotificationChannelViewSet.as_view({'get': 'by_type'}),
         name='channel-by-type'),
    
    # Notification specific endpoints
    path('api/notifications/notifications/<uuid:pk>/mark-read/',
         NotificationViewSet.as_view({'post': 'mark_as_read'}),
         name='notification-mark-read'),
    
    path('api/notifications/notifications/<uuid:pk>/mark-unread/',
         NotificationViewSet.as_view({'post': 'mark_as_unread'}),
         name='notification-mark-unread'),
    
    path('api/notifications/notifications/<uuid:pk>/archive/',
         NotificationViewSet.as_view({'post': 'archive'}),
         name='notification-archive'),
    
    path('api/notifications/notifications/<uuid:pk>/unarchive/',
         NotificationViewSet.as_view({'post': 'unarchive'}),
         name='notification-unarchive'),
    
    path('api/notifications/notifications/<uuid:pk>/resend/',
         NotificationViewSet.as_view({'post': 'resend'}),
         name='notification-resend'),
    
    path('api/notifications/notifications/mark-all-read/',
         NotificationViewSet.as_view({'post': 'mark_all_read'}),
         name='notification-mark-all-read'),
    
    path('api/notifications/notifications/unread/',
         NotificationViewSet.as_view({'get': 'unread'}),
         name='notification-unread'),
    
    path('api/notifications/notifications/recent/',
         NotificationViewSet.as_view({'get': 'recent'}),
         name='notification-recent'),
    
    path('api/notifications/notifications/stats/',
         NotificationViewSet.as_view({'get': 'stats'}),
         name='notification-stats'),
    
    # Preference specific endpoints
    path('api/notifications/preferences/<uuid:pk>/toggle/',
         NotificationPreferenceViewSet.as_view({'post': 'toggle_enabled'}),
         name='preference-toggle'),
    
    path('api/notifications/preferences/by-category/',
         NotificationPreferenceViewSet.as_view({'get': 'by_category'}),
         name='preference-by-category'),
    
    path('api/notifications/preferences/by-channel/',
         NotificationPreferenceViewSet.as_view({'get': 'by_channel'}),
         name='preference-by-channel'),
    
    path('api/notifications/preferences/bulk-update/',
         NotificationPreferenceViewSet.as_view({'post': 'bulk_update'}),
         name='preference-bulk-update'),
    
    # Batch specific endpoints
    path('api/notifications/batches/<uuid:pk>/start/',
         NotificationBatchViewSet.as_view({'post': 'start_batch'}),
         name='batch-start'),
    
    path('api/notifications/batches/<uuid:pk>/cancel/',
         NotificationBatchViewSet.as_view({'post': 'cancel_batch'}),
         name='batch-cancel'),
    
    path('api/notifications/batches/stats/',
         NotificationBatchViewSet.as_view({'get': 'stats'}),
         name='batch-stats'),
    
    # Log specific endpoints
    path('api/notifications/logs/errors/',
         NotificationLogViewSet.as_view({'get': 'errors'}),
         name='log-errors'),
    
    path('api/notifications/logs/by-level/',
         NotificationLogViewSet.as_view({'get': 'by_level'}),
         name='log-by-level'),
    
    # Schedule specific endpoints
    path('api/notifications/schedules/<uuid:pk>/activate/',
         NotificationScheduleViewSet.as_view({'post': 'activate_schedule'}),
         name='schedule-activate'),
    
    path('api/notifications/schedules/<uuid:pk>/deactivate/',
         NotificationScheduleViewSet.as_view({'post': 'deactivate_schedule'}),
         name='schedule-deactivate'),
    
    path('api/notifications/schedules/<uuid:pk>/run-now/',
         NotificationScheduleViewSet.as_view({'post': 'run_now'}),
         name='schedule-run-now'),
    
    path('api/notifications/schedules/active/',
         NotificationScheduleViewSet.as_view({'get': 'active'}),
         name='schedule-active'),
    
    path('api/notifications/schedules/due/',
         NotificationScheduleViewSet.as_view({'get': 'due'}),
         name='schedule-due'),
    
    # Stats specific endpoints
    path('api/notifications/stats/overview/',
         NotificationStatsViewSet.as_view({'get': 'overview'}),
         name='notificationstats-overview'),
    
    path('api/notifications/stats/trends/',
         NotificationStatsViewSet.as_view({'get': 'trends'}),
         name='notificationstats-trends'),
    
    # Additional notification endpoints
    path('api/notifications/send/',
         NotificationViewSet.as_view({'post': 'create'}),
         name='notification-send'),
    
    path('api/notifications/send-bulk/',
         NotificationBatchViewSet.as_view({'post': 'create'}),
         name='notification-send-bulk'),
    
    path('api/notifications/schedule/',
         NotificationScheduleViewSet.as_view({'post': 'create'}),
         name='notification-schedule'),
    
    # Notification management endpoints
    path('api/notifications/management/templates/',
         NotificationTemplateViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='management-templates'),
    
    path('api/notifications/management/channels/',
         NotificationChannelViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='management-channels'),
    
    path('api/notifications/management/batches/',
         NotificationBatchViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='management-batches'),
    
    path('api/notifications/management/schedules/',
         NotificationScheduleViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='management-schedules'),
    
    # Notification delivery endpoints
    path('api/notifications/delivery/email/',
         NotificationViewSet.as_view({'post': 'create'}),
         name='delivery-email'),
    
    path('api/notifications/delivery/sms/',
         NotificationViewSet.as_view({'post': 'create'}),
         name='delivery-sms'),
    
    path('api/notifications/delivery/push/',
         NotificationViewSet.as_view({'post': 'create'}),
         name='delivery-push'),
    
    path('api/notifications/delivery/in-app/',
         NotificationViewSet.as_view({'post': 'create'}),
         name='delivery-in-app'),
    
    # Notification webhook endpoints
    path('api/notifications/webhook/email/',
         NotificationViewSet.as_view({'post': 'create'}),
         name='webhook-email'),
    
    path('api/notifications/webhook/sms/',
         NotificationViewSet.as_view({'post': 'create'}),
         name='webhook-sms'),
    
    path('api/notifications/webhook/push/',
         NotificationViewSet.as_view({'post': 'create'}),
         name='webhook-push'),
    
    # Notification analytics endpoints
    path('api/notifications/analytics/delivery-rates/',
         NotificationStatsViewSet.as_view({'get': 'overview'}),
         name='analytics-delivery-rates'),
    
    path('api/notifications/analytics/channel-performance/',
         NotificationStatsViewSet.as_view({'get': 'overview'}),
         name='analytics-channel-performance'),
    
    path('api/notifications/analytics/user-engagement/',
         NotificationStatsViewSet.as_view({'get': 'overview'}),
         name='analytics-user-engagement'),
    
    # Notification support endpoints
    path('api/notifications/support/delivery-issues/',
         NotificationViewSet.as_view({'get': 'list'}),
         name='support-delivery-issues'),
    
    path('api/notifications/support/template-errors/',
         NotificationTemplateViewSet.as_view({'get': 'list'}),
         name='support-template-errors'),
    
    path('api/notifications/support/channel-problems/',
         NotificationChannelViewSet.as_view({'get': 'list'}),
         name='support-channel-problems'),
] 