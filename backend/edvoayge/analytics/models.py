import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class AnalyticsEvent(models.Model):
    """Analytics events for tracking user interactions"""
    
    EVENT_TYPES = [
        ('page_view', 'Page View'),
        ('button_click', 'Button Click'),
        ('form_submit', 'Form Submit'),
        ('link_click', 'Link Click'),
        ('search', 'Search'),
        ('download', 'Download'),
        ('video_play', 'Video Play'),
        ('video_pause', 'Video Pause'),
        ('video_complete', 'Video Complete'),
        ('scroll', 'Scroll'),
        ('hover', 'Hover'),
        ('focus', 'Focus'),
        ('blur', 'Blur'),
        ('error', 'Error'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('info', 'Info'),
        ('custom', 'Custom'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analytics_events', null=True, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    
    # Event details
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    event_name = models.CharField(max_length=100)
    event_category = models.CharField(max_length=50, blank=True)
    event_action = models.CharField(max_length=50, blank=True)
    event_label = models.CharField(max_length=100, blank=True)
    
    # Page/context information
    page_url = models.URLField(blank=True)
    page_title = models.CharField(max_length=200, blank=True)
    referrer_url = models.URLField(blank=True)
    
    # User agent and device info
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    device_type = models.CharField(max_length=20, blank=True)
    browser = models.CharField(max_length=50, blank=True)
    os = models.CharField(max_length=50, blank=True)
    
    # Location information
    country = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    
    # Event data
    event_data = models.JSONField(default=dict, blank=True)
    event_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'analytics_events'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'event_type']),
            models.Index(fields=['event_type', 'created_at']),
            models.Index(fields=['session_id']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.event_name} - {self.user.email if self.user else 'Anonymous'}"


class PageView(models.Model):
    """Page view analytics"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='page_views', null=True, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    
    # Page information
    page_url = models.URLField()
    page_title = models.CharField(max_length=200, blank=True)
    page_category = models.CharField(max_length=50, blank=True)
    page_section = models.CharField(max_length=50, blank=True)
    
    # View details
    view_duration = models.PositiveIntegerField(default=0)  # in seconds
    scroll_depth = models.PositiveIntegerField(default=0)  # percentage
    is_bounce = models.BooleanField(default=True)
    
    # Referrer information
    referrer_url = models.URLField(blank=True)
    referrer_domain = models.CharField(max_length=100, blank=True)
    
    # User agent and device info
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    device_type = models.CharField(max_length=20, blank=True)
    browser = models.CharField(max_length=50, blank=True)
    os = models.CharField(max_length=50, blank=True)
    
    # Location information
    country = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'page_views'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'page_url']),
            models.Index(fields=['page_url', 'created_at']),
            models.Index(fields=['session_id']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.page_title} - {self.user.email if self.user else 'Anonymous'}"


class UserSession(models.Model):
    """User session analytics"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analytics_sessions', null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    
    # Session details
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.PositiveIntegerField(default=0)  # in seconds
    is_active = models.BooleanField(default=True)
    
    # Session data
    page_views_count = models.PositiveIntegerField(default=0)
    events_count = models.PositiveIntegerField(default=0)
    unique_pages = models.PositiveIntegerField(default=0)
    
    # User agent and device info
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    device_type = models.CharField(max_length=20, blank=True)
    browser = models.CharField(max_length=50, blank=True)
    os = models.CharField(max_length=50, blank=True)
    
    # Location information
    country = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    
    # Session data
    session_data = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_sessions'
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['user', 'start_time']),
            models.Index(fields=['session_id']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"Session {self.session_id} - {self.user.email if self.user else 'Anonymous'}"
    
    @property
    def session_duration(self):
        """Calculate session duration"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (timezone.now() - self.start_time).total_seconds()


class UserMetrics(models.Model):
    """User behavior metrics"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metrics')
    date = models.DateField()
    
    # Engagement metrics
    sessions_count = models.PositiveIntegerField(default=0)
    page_views_count = models.PositiveIntegerField(default=0)
    events_count = models.PositiveIntegerField(default=0)
    unique_pages_visited = models.PositiveIntegerField(default=0)
    
    # Time metrics
    total_session_duration = models.PositiveIntegerField(default=0)  # in seconds
    average_session_duration = models.PositiveIntegerField(default=0)  # in seconds
    average_pages_per_session = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Conversion metrics
    conversions_count = models.PositiveIntegerField(default=0)
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Retention metrics
    is_returning_user = models.BooleanField(default=False)
    days_since_first_visit = models.PositiveIntegerField(default=0)
    
    # Custom metrics
    custom_metrics = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_metrics'
        ordering = ['-date']
        unique_together = ['user', 'date']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.date}"


class AnalyticsReport(models.Model):
    """Analytics reports and dashboards"""
    
    REPORT_TYPES = [
        ('user_behavior', 'User Behavior'),
        ('page_performance', 'Page Performance'),
        ('conversion_funnel', 'Conversion Funnel'),
        ('traffic_sources', 'Traffic Sources'),
        ('device_analytics', 'Device Analytics'),
        ('geographic_data', 'Geographic Data'),
        ('custom', 'Custom Report'),
    ]
    
    REPORT_FORMATS = [
        ('json', 'JSON'),
        ('csv', 'CSV'),
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('html', 'HTML'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    format = models.CharField(max_length=10, choices=REPORT_FORMATS, default='json')
    
    # Report configuration
    date_range_start = models.DateField()
    date_range_end = models.DateField()
    filters = models.JSONField(default=dict, blank=True)
    metrics = models.JSONField(default=list, blank=True)
    dimensions = models.JSONField(default=list, blank=True)
    
    # Report data
    report_data = models.JSONField(default=dict, blank=True)
    report_url = models.URLField(blank=True)
    
    # Scheduling
    is_scheduled = models.BooleanField(default=False)
    schedule_frequency = models.CharField(max_length=20, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ], blank=True)
    last_generated = models.DateTimeField(blank=True, null=True)
    next_generation = models.DateTimeField(blank=True, null=True)
    
    # Access control
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_reports')
    shared_with = models.ManyToManyField(User, related_name='shared_reports', blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'analytics_reports'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['report_type', 'created_at']),
            models.Index(fields=['created_by', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_report_type_display()})"


class AnalyticsDashboard(models.Model):
    """Analytics dashboards"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Dashboard configuration
    layout = models.JSONField(default=dict, blank=True)
    widgets = models.JSONField(default=list, blank=True)
    filters = models.JSONField(default=dict, blank=True)
    
    # Access control
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_dashboards')
    shared_with = models.ManyToManyField(User, related_name='shared_dashboards', blank=True)
    
    # Settings
    refresh_interval = models.PositiveIntegerField(default=300)  # in seconds
    auto_refresh = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'analytics_dashboards'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_by', 'created_at']),
        ]
    
    def __str__(self):
        return self.name


class AnalyticsWidget(models.Model):
    """Analytics dashboard widgets"""
    
    WIDGET_TYPES = [
        ('chart', 'Chart'),
        ('table', 'Table'),
        ('metric', 'Metric'),
        ('map', 'Map'),
        ('funnel', 'Funnel'),
        ('heatmap', 'Heatmap'),
        ('custom', 'Custom'),
    ]
    
    CHART_TYPES = [
        ('line', 'Line Chart'),
        ('bar', 'Bar Chart'),
        ('pie', 'Pie Chart'),
        ('area', 'Area Chart'),
        ('scatter', 'Scatter Plot'),
        ('bubble', 'Bubble Chart'),
        ('radar', 'Radar Chart'),
        ('gauge', 'Gauge'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    chart_type = models.CharField(max_length=20, choices=CHART_TYPES, blank=True)
    
    # Widget configuration
    query = models.JSONField(default=dict, blank=True)
    metrics = models.JSONField(default=list, blank=True)
    dimensions = models.JSONField(default=list, blank=True)
    filters = models.JSONField(default=dict, blank=True)
    
    # Display settings
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    size = models.JSONField(default=dict, blank=True)
    position = models.JSONField(default=dict, blank=True)
    
    # Data settings
    refresh_interval = models.PositiveIntegerField(default=300)  # in seconds
    auto_refresh = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'analytics_widgets'
        ordering = ['name']
        indexes = [
            models.Index(fields=['widget_type', 'chart_type']),
        ]
    
    def __str__(self):
        return self.name


class AnalyticsExport(models.Model):
    """Analytics data exports"""
    
    EXPORT_TYPES = [
        ('events', 'Events'),
        ('page_views', 'Page Views'),
        ('sessions', 'Sessions'),
        ('metrics', 'Metrics'),
        ('reports', 'Reports'),
        ('custom', 'Custom'),
    ]
    
    EXPORT_FORMATS = [
        ('json', 'JSON'),
        ('csv', 'CSV'),
        ('excel', 'Excel'),
        ('pdf', 'PDF'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    export_type = models.CharField(max_length=20, choices=EXPORT_TYPES)
    format = models.CharField(max_length=10, choices=EXPORT_FORMATS)
    
    # Export configuration
    date_range_start = models.DateField()
    date_range_end = models.DateField()
    filters = models.JSONField(default=dict, blank=True)
    fields = models.JSONField(default=list, blank=True)
    
    # Export status
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    
    # File information
    file_url = models.URLField(blank=True)
    file_size = models.PositiveIntegerField(default=0)  # in bytes
    record_count = models.PositiveIntegerField(default=0)
    
    # User information
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exports')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'analytics_exports'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['export_type', 'status']),
            models.Index(fields=['created_by', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_export_type_display()})"


class EventType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'category')
        ordering = ['name']

    def __str__(self):
        return self.name

class PageType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'category')
        ordering = ['name']

    def __str__(self):
        return self.name

class SessionType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'category')
        ordering = ['name']

    def __str__(self):
        return self.name
