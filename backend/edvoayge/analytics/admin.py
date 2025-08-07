from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta

from .models import (
    AnalyticsEvent, PageView, UserSession, UserMetrics, AnalyticsReport, 
    AnalyticsDashboard, AnalyticsWidget, AnalyticsExport, EventType, PageType, SessionType
)


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    """Admin for EventType model"""
    list_display = ['name', 'category', 'is_active', 'created_at', 'updated_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'category']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Settings', {
            'fields': ('is_active', 'metadata')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PageType)
class PageTypeAdmin(admin.ModelAdmin):
    """Admin for PageType model"""
    list_display = ['name', 'category', 'is_active', 'created_at', 'updated_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'category']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Settings', {
            'fields': ('is_active', 'metadata')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SessionType)
class SessionTypeAdmin(admin.ModelAdmin):
    """Admin for SessionType model"""
    list_display = ['name', 'category', 'is_active', 'created_at', 'updated_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'category']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Settings', {
            'fields': ('is_active', 'metadata')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    """Admin for AnalyticsEvent model"""
    list_display = ['event_name', 'user', 'event_type', 'session_duration_display', 'created_at']
    list_filter = ['event_type', 'created_at']
    search_fields = ['event_name', 'user__email', 'event_type__name', 'session_id']
    readonly_fields = ['id', 'created_at', 'session_duration_display']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Event Information', {
            'fields': ('event_name', 'event_type', 'user', 'session_id')
        }),
        ('Session Details', {
            'fields': ('session_start', 'session_end', 'session_duration_display')
        }),
        ('Additional Data', {
            'fields': ('metadata', 'tags')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def session_duration_display(self, obj):
        """Display session duration in a readable format"""
        if obj.session_start and obj.session_end:
            duration = obj.session_end - obj.session_start
            return f"{duration.total_seconds():.1f} seconds"
        return "N/A"
    session_duration_display.short_description = "Session Duration"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('user', 'event_type')


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    """Admin for PageView model"""
    list_display = ['page_url', 'page_title', 'user', 'session_duration_display', 'created_at']
    list_filter = ['created_at']
    search_fields = ['page_url', 'page_title', 'user__email', 'session_id']
    readonly_fields = ['id', 'created_at', 'session_duration_display']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Page Information', {
            'fields': ('page_url', 'page_title', 'page_type', 'user', 'session_id')
        }),
        ('Session Details', {
            'fields': ('session_start', 'session_end', 'session_duration_display')
        }),
        ('Additional Data', {
            'fields': ('metadata', 'tags')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def session_duration_display(self, obj):
        """Display session duration in a readable format"""
        if obj.session_start and obj.session_end:
            duration = obj.session_end - obj.session_start
            return f"{duration.total_seconds():.1f} seconds"
        return "N/A"
    session_duration_display.short_description = "Session Duration"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('user', 'page_type')


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """Admin for UserSession model"""
    list_display = ['user', 'duration_display', 'page_views_count', 'events_count', 'start_time']
    list_filter = ['start_time', 'end_time', 'created_at']
    search_fields = ['user__email', 'ip_address', 'user_agent']
    readonly_fields = ['id', 'created_at', 'duration_display', 'page_views_count', 'events_count']
    ordering = ['-start_time']
    date_hierarchy = 'start_time'
    
    fieldsets = (
        ('Session Information', {
            'fields': ('user', 'session_type', 'session_id')
        }),
        ('Timing', {
            'fields': ('start_time', 'end_time', 'duration_display')
        }),
        ('Technical Details', {
            'fields': ('ip_address', 'user_agent', 'device_info')
        }),
        ('Additional Data', {
            'fields': ('metadata', 'tags')
        }),
        ('Statistics', {
            'fields': ('page_views_count', 'events_count'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def duration_display(self, obj):
        """Display session duration in a readable format"""
        if obj.start_time and obj.end_time:
            duration = obj.end_time - obj.start_time
            return f"{duration.total_seconds():.1f} seconds"
        return "N/A"
    duration_display.short_description = "Duration"
    
    def page_views_count(self, obj):
        """Get count of page views for this session"""
        return PageView.objects.filter(session_id=obj.id).count()
    page_views_count.short_description = "Page Views"
    
    def events_count(self, obj):
        """Get count of events for this session"""
        return AnalyticsEvent.objects.filter(session_id=obj.id).count()
    events_count.short_description = "Events"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('user', 'session_type')


@admin.register(UserMetrics)
class UserMetricsAdmin(admin.ModelAdmin):
    """Admin for UserMetrics model"""
    list_display = ['user', 'date', 'sessions_count', 'page_views_count', 'events_count', 'unique_pages_visited', 'total_session_duration', 'average_session_duration', 'average_pages_per_session', 'conversions_count', 'conversion_rate', 'is_returning_user', 'days_since_first_visit', 'created_at']
    list_filter = ['date', 'is_returning_user', 'user']
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-date']
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Metrics', {'fields': ('sessions_count', 'page_views_count', 'events_count', 'unique_pages_visited', 'total_session_duration', 'average_session_duration', 'average_pages_per_session', 'conversions_count', 'conversion_rate', 'is_returning_user', 'days_since_first_visit', 'custom_metrics')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(AnalyticsReport)
class AnalyticsReportAdmin(admin.ModelAdmin):
    """Admin for AnalyticsReport model"""
    list_display = ['name', 'report_type', 'created_by', 'is_public', 'created_at']
    list_filter = ['report_type', 'is_public', 'created_by', 'created_at']
    search_fields = ['name', 'description', 'report_type', 'created_by__email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'report_type')
        }),
        ('Settings', {
            'fields': ('is_public', 'created_by')
        }),
        ('Configuration', {
            'fields': ('filters', 'metadata')
        }),
        ('Statistics', {
            'fields': ('metrics_count', 'widgets_count'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def metrics_count(self, obj):
        """Get count of metrics in this report"""
        return UserMetrics.objects.filter(report=obj).count()
    metrics_count.short_description = "Metrics"
    
    def widgets_count(self, obj):
        """Get count of widgets in this report"""
        return AnalyticsWidget.objects.filter(report=obj).count()
    widgets_count.short_description = "Widgets"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('created_by')


@admin.register(AnalyticsWidget)
class AnalyticsWidgetAdmin(admin.ModelAdmin):
    """Admin for AnalyticsWidget model"""
    list_display = ['name', 'widget_type', 'created_at']
    list_filter = ['widget_type', 'created_at']
    search_fields = ['name', 'description', 'widget_type']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'widget_type')
        }),
        ('Relationships', {
            'fields': ('report', 'dashboard')
        }),
        ('Configuration', {
            'fields': ('config', 'metadata')
        }),
        ('Statistics', {
            'fields': ('metrics_count',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def metrics_count(self, obj):
        """Get count of metrics in this widget"""
        return UserMetrics.objects.filter(widget=obj).count()
    metrics_count.short_description = "Metrics"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('report', 'dashboard')


@admin.register(AnalyticsDashboard)
class AnalyticsDashboardAdmin(admin.ModelAdmin):
    """Admin for AnalyticsDashboard model"""
    list_display = ['name', 'created_by', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_by', 'created_at']
    search_fields = ['name', 'description', 'created_by__email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Settings', {
            'fields': ('is_public', 'created_by')
        }),
        ('Layout', {
            'fields': ('layout', 'metadata')
        }),
        ('Statistics', {
            'fields': ('widgets_count', 'reports_count'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def widgets_count(self, obj):
        """Get count of widgets in this dashboard"""
        return AnalyticsWidget.objects.filter(dashboard=obj).count()
    widgets_count.short_description = "Widgets"
    
    def reports_count(self, obj):
        """Get count of reports in this dashboard"""
        return AnalyticsReport.objects.filter(dashboard=obj).count()
    reports_count.short_description = "Reports"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('created_by')


@admin.register(AnalyticsExport)
class AnalyticsExportAdmin(admin.ModelAdmin):
    """Admin for AnalyticsExport model"""
    list_display = ['name', 'export_type', 'created_by', 'created_at']
    list_filter = ['export_type', 'created_by', 'created_at']
    search_fields = ['name', 'description', 'export_type', 'created_by__email']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'export_type')
        }),
        ('Relationships', {
            'fields': ('dashboard', 'report', 'created_by')
        }),
        ('File', {
            'fields': ('file', 'file_size_display')
        }),
        ('Additional Data', {
            'fields': ('metadata', 'tags')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def file_size_display(self, obj):
        """Display file size in a readable format"""
        if obj.file and hasattr(obj.file, 'size'):
            size_mb = obj.file.size / (1024 * 1024)
            return f"{size_mb:.2f} MB"
        return "N/A"
    file_size_display.short_description = "File Size"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('dashboard', 'report', 'created_by')


# Analytics Dashboard Admin
class AnalyticsDashboardAdmin(admin.ModelAdmin):
    """Admin for analytics dashboard overview"""
    change_list_template = 'admin/analytics_dashboard.html'
    
    def changelist_view(self, request, extra_context=None):
        """Custom changelist view for analytics dashboard"""
        extra_context = extra_context or {}
        
        # Get analytics statistics
        now = timezone.now()
        last_30_days = now - timedelta(days=30)
        
        # Event statistics
        total_events = AnalyticsEvent.objects.count()
        events_last_30_days = AnalyticsEvent.objects.filter(created_at__gte=last_30_days).count()
        
        # Page view statistics
        total_page_views = PageView.objects.count()
        page_views_last_30_days = PageView.objects.filter(created_at__gte=last_30_days).count()
        
        # Session statistics
        total_sessions = UserSession.objects.count()
        sessions_last_30_days = UserSession.objects.filter(start_time__gte=last_30_days).count()
        
        # User statistics
        unique_users = UserSession.objects.values('user').distinct().count()
        active_users_last_30_days = UserSession.objects.filter(
            start_time__gte=last_30_days
        ).values('user').distinct().count()
        
        # Top event types
        top_event_types = AnalyticsEvent.objects.values('event_type__name').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # Top pages
        top_pages = PageView.objects.values('page_url', 'page_title').annotate(
            views=Count('id')
        ).order_by('-views')[:5]
        
        extra_context.update({
            'total_events': total_events,
            'events_last_30_days': events_last_30_days,
            'total_page_views': total_page_views,
            'page_views_last_30_days': page_views_last_30_days,
            'total_sessions': total_sessions,
            'sessions_last_30_days': sessions_last_30_days,
            'unique_users': unique_users,
            'active_users_last_30_days': active_users_last_30_days,
            'top_event_types': top_event_types,
            'top_pages': top_pages,
        })
        
        return super().changelist_view(request, extra_context)
