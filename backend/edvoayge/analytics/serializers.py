from rest_framework import serializers
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    AnalyticsEvent, PageView, UserSession, EventType, PageType, SessionType
)


class EventTypeSerializer(serializers.ModelSerializer):
    """Serializer for EventType model"""
    
    class Meta:
        model = EventType
        fields = '__all__'


class PageTypeSerializer(serializers.ModelSerializer):
    """Serializer for PageType model"""
    
    class Meta:
        model = PageType
        fields = '__all__'


class SessionTypeSerializer(serializers.ModelSerializer):
    """Serializer for SessionType model"""
    
    class Meta:
        model = SessionType
        fields = '__all__'


class AnalyticsEventSerializer(serializers.ModelSerializer):
    """Serializer for AnalyticsEvent model"""
    event_type_name = serializers.CharField(source='event_type.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    session_duration = serializers.SerializerMethodField()
    
    class Meta:
        model = AnalyticsEvent
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_session_duration(self, obj):
        """Calculate session duration in seconds"""
        if obj.session_start and obj.session_end:
            return (obj.session_end - obj.session_start).total_seconds()
        return None
    
    def validate(self, data):
        """Validate event data"""
        if data.get('session_end') and data.get('session_start'):
            if data['session_end'] <= data['session_start']:
                raise serializers.ValidationError("Session end must be after session start")
        
        if data.get('metadata') and not isinstance(data['metadata'], dict):
            raise serializers.ValidationError("Metadata must be a valid JSON object")
        
        return data


class PageViewSerializer(serializers.ModelSerializer):
    """Serializer for PageView model"""
    page_type_name = serializers.CharField(source='page_type.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    session_duration = serializers.SerializerMethodField()
    
    class Meta:
        model = PageView
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_session_duration(self, obj):
        """Calculate session duration in seconds"""
        if obj.session_start and obj.session_end:
            return (obj.session_end - obj.session_start).total_seconds()
        return None
    
    def validate(self, data):
        """Validate page view data"""
        if data.get('session_end') and data.get('session_start'):
            if data['session_end'] <= data['session_start']:
                raise serializers.ValidationError("Session end must be after session start")
        
        if data.get('metadata') and not isinstance(data['metadata'], dict):
            raise serializers.ValidationError("Metadata must be a valid JSON object")
        
        return data


class UserSessionSerializer(serializers.ModelSerializer):
    """Serializer for UserSession model"""
    session_type_name = serializers.CharField(source='session_type.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    duration_seconds = serializers.SerializerMethodField()
    page_views_count = serializers.SerializerMethodField()
    events_count = serializers.SerializerMethodField()
    
    class Meta:
        model = UserSession
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_duration_seconds(self, obj):
        """Calculate session duration in seconds"""
        if obj.start_time and obj.end_time:
            return (obj.end_time - obj.start_time).total_seconds()
        return None
    
    def get_page_views_count(self, obj):
        """Get count of page views for this session"""
        return PageView.objects.filter(session_id=obj.id).count()
    
    def get_events_count(self, obj):
        """Get count of events for this session"""
        return AnalyticsEvent.objects.filter(session_id=obj.id).count()
    
    def validate(self, data):
        """Validate session data"""
        if data.get('end_time') and data.get('start_time'):
            if data['end_time'] <= data['start_time']:
                raise serializers.ValidationError("End time must be after start time")
        
        if data.get('metadata') and not isinstance(data['metadata'], dict):
            raise serializers.ValidationError("Metadata must be a valid JSON object")
        
        return data


# Analytics Stats Serializers
class AnalyticsStatsSerializer(serializers.Serializer):
    """Serializer for analytics statistics"""
    total_events = serializers.IntegerField()
    total_page_views = serializers.IntegerField()
    total_sessions = serializers.IntegerField()
    total_users = serializers.IntegerField()
    avg_session_duration = serializers.FloatField()
    avg_page_views_per_session = serializers.FloatField()
    top_events = serializers.ListField(child=serializers.DictField())
    top_pages = serializers.ListField(child=serializers.DictField())
    user_engagement_score = serializers.FloatField()
    conversion_rate = serializers.FloatField()


class EventStatsSerializer(serializers.Serializer):
    """Serializer for event statistics"""
    event_type = serializers.CharField()
    count = serializers.IntegerField()
    percentage = serializers.FloatField()
    avg_duration = serializers.FloatField()
    unique_users = serializers.IntegerField()


class PageViewStatsSerializer(serializers.Serializer):
    """Serializer for page view statistics"""
    page_url = serializers.CharField()
    page_type = serializers.CharField()
    views = serializers.IntegerField()
    unique_views = serializers.IntegerField()
    avg_time_on_page = serializers.FloatField()
    bounce_rate = serializers.FloatField()


class SessionStatsSerializer(serializers.Serializer):
    """Serializer for session statistics"""
    session_type = serializers.CharField()
    count = serializers.IntegerField()
    avg_duration = serializers.FloatField()
    unique_users = serializers.IntegerField()
    avg_page_views = serializers.FloatField()


class UserEngagementSerializer(serializers.Serializer):
    """Serializer for user engagement metrics"""
    user_id = serializers.UUIDField()
    user_email = serializers.CharField()
    total_sessions = serializers.IntegerField()
    total_page_views = serializers.IntegerField()
    total_events = serializers.IntegerField()
    avg_session_duration = serializers.FloatField()
    last_activity = serializers.DateTimeField()
    engagement_score = serializers.FloatField()


class ConversionFunnelSerializer(serializers.Serializer):
    """Serializer for conversion funnel data"""
    stage = serializers.CharField()
    count = serializers.IntegerField()
    conversion_rate = serializers.FloatField()
    drop_off_rate = serializers.FloatField()
    avg_time_in_stage = serializers.FloatField()


class RealTimeMetricsSerializer(serializers.Serializer):
    """Serializer for real-time metrics"""
    active_users = serializers.IntegerField()
    active_sessions = serializers.IntegerField()
    events_last_hour = serializers.IntegerField()
    page_views_last_hour = serializers.IntegerField()
    top_active_pages = serializers.ListField(child=serializers.DictField())
    recent_events = serializers.ListField(child=serializers.DictField()) 