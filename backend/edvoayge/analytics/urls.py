from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import (
    EventTypeViewSet, PageTypeViewSet, SessionTypeViewSet,
    AnalyticsEventViewSet, PageViewViewSet, UserSessionViewSet,
    AnalyticsAPIViewSet
)

# Create main router
router = DefaultRouter()
# router.register(r'event-types', EventTypeViewSet, basename='event-type')
# router.register(r'page-types', PageTypeViewSet, basename='page-type')
# router.register(r'session-types', SessionTypeViewSet, basename='session-type')
# router.register(r'events', AnalyticsEventViewSet, basename='analytics-event')
# router.register(r'page-views', PageViewViewSet, basename='page-view')
# router.register(r'sessions', UserSessionViewSet, basename='user-session')

# Analytics API endpoints
analytics_api_router = SimpleRouter()
analytics_api_router.register(r'api', AnalyticsAPIViewSet, basename='analytics-api')

# Custom URL patterns for analytics
analytics_urlpatterns = [
    # path('track/event/', AnalyticsEventViewSet.as_view({'post': 'track_event'}), name='track-event'),
    # path('track/page-view/', PageViewViewSet.as_view({'post': 'track_page_view'}), name='track-page-view'),
    # path('sessions/start/', UserSessionViewSet.as_view({'post': 'start_session'}), name='start-session'),
    # path('sessions/<uuid:pk>/end/', UserSessionViewSet.as_view({'post': 'end_session'}), name='end-session'),
    # path('events/stats/', AnalyticsEventViewSet.as_view({'get': 'stats'}), name='event-stats'),
    # path('page-views/stats/', PageViewViewSet.as_view({'get': 'stats'}), name='page-view-stats'),
    # path('sessions/stats/', UserSessionViewSet.as_view({'get': 'stats'}), name='session-stats'),
    # path('overview/', AnalyticsAPIViewSet.as_view({'get': 'overview'}), name='analytics-overview'),
    # path('real-time/', AnalyticsAPIViewSet.as_view({'get': 'real_time'}), name='analytics-real-time'),
    # path('user-engagement/', AnalyticsAPIViewSet.as_view({'get': 'user_engagement'}), name='analytics-user-engagement'),
    # path('conversion-funnel/', AnalyticsAPIViewSet.as_view({'get': 'conversion_funnel'}), name='analytics-conversion-funnel'),
]

# Include all URL patterns
urlpatterns = [
    path('api/', include(router.urls)),
]
urlpatterns += analytics_urlpatterns 