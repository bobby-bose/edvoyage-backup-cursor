from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg, Sum, Q, F, ExpressionWrapper, fields, Max
from django.utils import timezone
from datetime import timedelta
import logging

from .models import (
    AnalyticsEvent, PageView, UserSession, EventType, PageType, SessionType
)
from .serializers import (
    AnalyticsEventSerializer, PageViewSerializer, UserSessionSerializer,
    EventTypeSerializer, PageTypeSerializer, SessionTypeSerializer,
    AnalyticsStatsSerializer, EventStatsSerializer, PageViewStatsSerializer,
    SessionStatsSerializer, UserEngagementSerializer, ConversionFunnelSerializer,
    RealTimeMetricsSerializer
)

logger = logging.getLogger(__name__)


class EventTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for EventType model"""
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'category', 'is_active']
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['name', 'category', 'created_at']
    ordering = ['name']


class PageTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for PageType model"""
    queryset = PageType.objects.all()
    serializer_class = PageTypeSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'category', 'is_active']
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['name', 'category', 'created_at']
    ordering = ['name']


class SessionTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for SessionType model"""
    queryset = SessionType.objects.all()
    serializer_class = SessionTypeSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'category', 'is_active']
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['name', 'category', 'created_at']
    ordering = ['name']


class AnalyticsEventViewSet(viewsets.ModelViewSet):
    """ViewSet for AnalyticsEvent model"""
    queryset = AnalyticsEvent.objects.select_related('user', 'event_type').all()
    serializer_class = AnalyticsEventSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'event_type', 'session_id', 'created_at']
    search_fields = ['event_name', 'event_type__name', 'user__email']
    ordering_fields = ['created_at', 'session_start', 'session_end', 'event_name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get event statistics"""
        try:
            # Get date range from query params
            days = int(request.query_params.get('days', 30))
            start_date = timezone.now() - timedelta(days=days)
            
            events = self.get_queryset().filter(created_at__gte=start_date)
            
            # Calculate stats
            total_events = events.count()
            unique_users = events.values('user').distinct().count()
            avg_duration = events.aggregate(
                avg_duration=Avg(
                    ExpressionWrapper(
                        F('session_end') - F('session_start'),
                        output_field=fields.DurationField()
                    )
                )
            )['avg_duration']
            
            # Top event types
            top_events = events.values('event_type__name').annotate(
                count=Count('id')
            ).order_by('-count')[:10]
            
            # Events by hour
            events_by_hour = events.extra(
                select={'hour': "EXTRACT(hour FROM created_at)"}
            ).values('hour').annotate(count=Count('id')).order_by('hour')
            
            stats = {
                'total_events': total_events,
                'unique_users': unique_users,
                'avg_duration_seconds': avg_duration.total_seconds() if avg_duration else 0,
                'top_events': list(top_events),
                'events_by_hour': list(events_by_hour)
            }
            
            serializer = EventStatsSerializer(stats, many=False)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error getting event stats: {e}")
            return Response(
                {'error': 'Failed to get event statistics'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def track_event(self, request):
        """Track a new analytics event"""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error tracking event: {e}")
            return Response(
                {'error': 'Failed to track event'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PageViewViewSet(viewsets.ModelViewSet):
    """ViewSet for PageView model"""
    queryset = PageView.objects.select_related('user', 'page_type').all()
    serializer_class = PageViewSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'page_type', 'session_id', 'created_at']
    search_fields = ['page_url', 'page_title', 'page_type__name', 'user__email']
    ordering_fields = ['created_at', 'session_start', 'session_end', 'page_url']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get page view statistics"""
        try:
            # Get date range from query params
            days = int(request.query_params.get('days', 30))
            start_date = timezone.now() - timedelta(days=days)
            
            page_views = self.get_queryset().filter(created_at__gte=start_date)
            
            # Calculate stats
            total_views = page_views.count()
            unique_views = page_views.values('user').distinct().count()
            avg_time_on_page = page_views.aggregate(
                avg_time=Avg(
                    ExpressionWrapper(
                        F('session_end') - F('session_start'),
                        output_field=fields.DurationField()
                    )
                )
            )['avg_time']
            
            # Top pages
            top_pages = page_views.values('page_url', 'page_title').annotate(
                views=Count('id'),
                unique_views=Count('user', distinct=True)
            ).order_by('-views')[:10]
            
            # Bounce rate calculation
            single_page_sessions = page_views.values('session_id').annotate(
                page_count=Count('id')
            ).filter(page_count=1).count()
            
            total_sessions = page_views.values('session_id').distinct().count()
            bounce_rate = (single_page_sessions / total_sessions * 100) if total_sessions > 0 else 0
            
            stats = {
                'total_views': total_views,
                'unique_views': unique_views,
                'avg_time_on_page_seconds': avg_time_on_page.total_seconds() if avg_time_on_page else 0,
                'bounce_rate': bounce_rate,
                'top_pages': list(top_pages)
            }
            
            serializer = PageViewStatsSerializer(stats, many=False)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error getting page view stats: {e}")
            return Response(
                {'error': 'Failed to get page view statistics'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def track_page_view(self, request):
        """Track a new page view"""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error tracking page view: {e}")
            return Response(
                {'error': 'Failed to track page view'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for UserSession model"""
    queryset = UserSession.objects.select_related('user', 'session_type').all()
    serializer_class = UserSessionSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'session_type', 'start_time', 'end_time']
    search_fields = ['user__email', 'session_type__name', 'ip_address']
    ordering_fields = ['start_time', 'end_time', 'created_at']
    ordering = ['-start_time']
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get session statistics"""
        try:
            # Get date range from query params
            days = int(request.query_params.get('days', 30))
            start_date = timezone.now() - timedelta(days=days)
            
            sessions = self.get_queryset().filter(start_time__gte=start_date)
            
            # Calculate stats
            total_sessions = sessions.count()
            unique_users = sessions.values('user').distinct().count()
            avg_duration = sessions.aggregate(
                avg_duration=Avg(
                    ExpressionWrapper(
                        F('end_time') - F('start_time'),
                        output_field=fields.DurationField()
                    )
                )
            )['avg_duration']
            
            # Sessions by type
            sessions_by_type = sessions.values('session_type__name').annotate(
                count=Count('id'),
                avg_duration=Avg(
                    ExpressionWrapper(
                        F('end_time') - F('start_time'),
                        output_field=fields.DurationField()
                    )
                )
            )
            
            # Active sessions (last 30 minutes)
            active_sessions = sessions.filter(
                end_time__gte=timezone.now() - timedelta(minutes=30)
            ).count()
            
            stats = {
                'total_sessions': total_sessions,
                'unique_users': unique_users,
                'avg_duration_seconds': avg_duration.total_seconds() if avg_duration else 0,
                'active_sessions': active_sessions,
                'sessions_by_type': list(sessions_by_type)
            }
            
            serializer = SessionStatsSerializer(stats, many=False)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error getting session stats: {e}")
            return Response(
                {'error': 'Failed to get session statistics'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def start_session(self, request):
        """Start a new user session"""
        try:
            data = request.data.copy()
            data['start_time'] = timezone.now()
            data['user'] = request.user.id
            
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                session = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error starting session: {e}")
            return Response(
                {'error': 'Failed to start session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def end_session(self, request, pk=None):
        """End a user session"""
        try:
            session = self.get_object()
            session.end_time = timezone.now()
            session.save()
            
            serializer = self.get_serializer(session)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error ending session: {e}")
            return Response(
                {'error': 'Failed to end session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Analytics API ViewSet for combined stats
class AnalyticsAPIViewSet(viewsets.ViewSet):
    """ViewSet for combined analytics API endpoints"""
    permission_classes = []
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get overview analytics statistics"""
        try:
            # Get date range from query params
            days = int(request.query_params.get('days', 30))
            start_date = timezone.now() - timedelta(days=days)
            
            # Get querysets
            events = AnalyticsEvent.objects.filter(created_at__gte=start_date)
            page_views = PageView.objects.filter(created_at__gte=start_date)
            sessions = UserSession.objects.filter(start_time__gte=start_date)
            
            # Calculate overview stats
            total_events = events.count()
            total_page_views = page_views.count()
            total_sessions = sessions.count()
            total_users = sessions.values('user').distinct().count()
            
            # Average session duration
            avg_session_duration = sessions.aggregate(
                avg_duration=Avg(
                    ExpressionWrapper(
                        F('end_time') - F('start_time'),
                        output_field=fields.DurationField()
                    )
                )
            )['avg_duration']
            
            # Average page views per session
            avg_page_views_per_session = page_views.count() / sessions.count() if sessions.count() > 0 else 0
            
            # Top events
            top_events = events.values('event_type__name').annotate(
                count=Count('id')
            ).order_by('-count')[:5]
            
            # Top pages
            top_pages = page_views.values('page_url', 'page_title').annotate(
                views=Count('id')
            ).order_by('-views')[:5]
            
            # User engagement score (simplified calculation)
            user_engagement_score = min(100, (total_events + total_page_views) / max(total_users, 1) * 10)
            
            # Conversion rate (simplified - based on events vs sessions)
            conversion_rate = (total_events / max(total_sessions, 1)) * 100 if total_sessions > 0 else 0
            
            stats = {
                'total_events': total_events,
                'total_page_views': total_page_views,
                'total_sessions': total_sessions,
                'total_users': total_users,
                'avg_session_duration': avg_session_duration.total_seconds() if avg_session_duration else 0,
                'avg_page_views_per_session': round(avg_page_views_per_session, 2),
                'top_events': list(top_events),
                'top_pages': list(top_pages),
                'user_engagement_score': round(user_engagement_score, 2),
                'conversion_rate': round(conversion_rate, 2)
            }
            
            serializer = AnalyticsStatsSerializer(stats)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error getting overview stats: {e}")
            return Response(
                {'error': 'Failed to get overview statistics'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def real_time(self, request):
        """Get real-time analytics metrics"""
        try:
            # Last hour metrics
            one_hour_ago = timezone.now() - timedelta(hours=1)
            
            # Active users (sessions in last 30 minutes)
            active_users = UserSession.objects.filter(
                end_time__gte=timezone.now() - timedelta(minutes=30)
            ).values('user').distinct().count()
            
            # Active sessions
            active_sessions = UserSession.objects.filter(
                end_time__gte=timezone.now() - timedelta(minutes=30)
            ).count()
            
            # Events in last hour
            events_last_hour = AnalyticsEvent.objects.filter(
                created_at__gte=one_hour_ago
            ).count()
            
            # Page views in last hour
            page_views_last_hour = PageView.objects.filter(
                created_at__gte=one_hour_ago
            ).count()
            
            # Top active pages
            top_active_pages = PageView.objects.filter(
                created_at__gte=one_hour_ago
            ).values('page_url', 'page_title').annotate(
                views=Count('id')
            ).order_by('-views')[:5]
            
            # Recent events
            recent_events = AnalyticsEvent.objects.filter(
                created_at__gte=one_hour_ago
            ).select_related('event_type', 'user').order_by('-created_at')[:10]
            
            recent_events_data = []
            for event in recent_events:
                recent_events_data.append({
                    'id': str(event.id),
                    'event_name': event.event_name,
                    'event_type': event.event_type.name if event.event_type else None,
                    'user_email': event.user.email if event.user else None,
                    'created_at': event.created_at
                })
            
            stats = {
                'active_users': active_users,
                'active_sessions': active_sessions,
                'events_last_hour': events_last_hour,
                'page_views_last_hour': page_views_last_hour,
                'top_active_pages': list(top_active_pages),
                'recent_events': recent_events_data
            }
            
            serializer = RealTimeMetricsSerializer(stats)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error getting real-time stats: {e}")
            return Response(
                {'error': 'Failed to get real-time statistics'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def user_engagement(self, request):
        """Get user engagement metrics"""
        try:
            # Get date range from query params
            days = int(request.query_params.get('days', 30))
            start_date = timezone.now() - timedelta(days=days)
            
            # Get user engagement data
            users_data = []
            
            # Get all users with activity
            active_users = UserSession.objects.filter(
                start_time__gte=start_date
            ).values('user').distinct()
            
            for user_data in active_users:
                user_id = user_data['user']
                
                # Get user sessions
                user_sessions = UserSession.objects.filter(
                    user_id=user_id,
                    start_time__gte=start_date
                )
                
                # Get user page views
                user_page_views = PageView.objects.filter(
                    user_id=user_id,
                    created_at__gte=start_date
                )
                
                # Get user events
                user_events = AnalyticsEvent.objects.filter(
                    user_id=user_id,
                    created_at__gte=start_date
                )
                
                # Calculate metrics
                total_sessions = user_sessions.count()
                total_page_views = user_page_views.count()
                total_events = user_events.count()
                
                # Average session duration
                avg_session_duration = user_sessions.aggregate(
                    avg_duration=Avg(
                        ExpressionWrapper(
                            F('end_time') - F('start_time'),
                            output_field=fields.DurationField()
                        )
                    )
                )['avg_duration']
                
                # Last activity
                last_activity = max(
                    user_sessions.aggregate(last=Max('end_time'))['last'] or timezone.now(),
                    user_page_views.aggregate(last=Max('created_at'))['last'] or timezone.now(),
                    user_events.aggregate(last=Max('created_at'))['last'] or timezone.now()
                )
                
                # Engagement score (simplified calculation)
                engagement_score = min(100, (total_sessions * 10 + total_page_views * 2 + total_events * 5))
                
                # Get user email
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.get(id=user_id)
                
                users_data.append({
                    'user_id': user_id,
                    'user_email': user.email,
                    'total_sessions': total_sessions,
                    'total_page_views': total_page_views,
                    'total_events': total_events,
                    'avg_session_duration': avg_session_duration.total_seconds() if avg_session_duration else 0,
                    'last_activity': last_activity,
                    'engagement_score': round(engagement_score, 2)
                })
            
            # Sort by engagement score
            users_data.sort(key=lambda x: x['engagement_score'], reverse=True)
            
            serializer = UserEngagementSerializer(users_data, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error getting user engagement: {e}")
            return Response(
                {'error': 'Failed to get user engagement metrics'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def conversion_funnel(self, request):
        """Get conversion funnel data"""
        try:
            # Get date range from query params
            days = int(request.query_params.get('days', 30))
            start_date = timezone.now() - timedelta(days=days)
            
            # Define funnel stages (simplified example)
            stages = [
                {'name': 'Page Views', 'query': PageView.objects.filter(created_at__gte=start_date)},
                {'name': 'Sessions', 'query': UserSession.objects.filter(start_time__gte=start_date)},
                {'name': 'Events', 'query': AnalyticsEvent.objects.filter(created_at__gte=start_date)},
                {'name': 'Engagement', 'query': AnalyticsEvent.objects.filter(
                    created_at__gte=start_date,
                    event_type__name__in=['click', 'scroll', 'form_submit']
                )}
            ]
            
            funnel_data = []
            previous_count = None
            
            for i, stage in enumerate(stages):
                count = stage['query'].count()
                
                if previous_count is not None and previous_count > 0:
                    conversion_rate = (count / previous_count) * 100
                    drop_off_rate = ((previous_count - count) / previous_count) * 100
                else:
                    conversion_rate = 100
                    drop_off_rate = 0
                
                # Calculate average time in stage (simplified)
                avg_time_in_stage = 0
                if stage['name'] == 'Sessions':
                    avg_duration = stage['query'].aggregate(
                        avg_duration=Avg(
                            ExpressionWrapper(
                                F('end_time') - F('start_time'),
                                output_field=fields.DurationField()
                            )
                        )
                    )['avg_duration']
                    avg_time_in_stage = avg_duration.total_seconds() if avg_duration else 0
                
                funnel_data.append({
                    'stage': stage['name'],
                    'count': count,
                    'conversion_rate': round(conversion_rate, 2),
                    'drop_off_rate': round(drop_off_rate, 2),
                    'avg_time_in_stage': avg_time_in_stage
                })
                
                previous_count = count
            
            serializer = ConversionFunnelSerializer(funnel_data, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error getting conversion funnel: {e}")
            return Response(
                {'error': 'Failed to get conversion funnel data'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
