import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class NotificationTemplate(models.Model):
    """Templates for different types of notifications"""
    
    TEMPLATE_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App Notification'),
        ('webhook', 'Webhook'),
        ('slack', 'Slack'),
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
    ]
    
    CATEGORIES = [
        ('system', 'System'),
        ('user', 'User'),
        ('payment', 'Payment'),
        ('application', 'Application'),
        ('university', 'University'),
        ('course', 'Course'),
        ('reminder', 'Reminder'),
        ('alert', 'Alert'),
        ('marketing', 'Marketing'),
        ('support', 'Support'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    is_active = models.BooleanField(default=True)
    
    # Template content
    subject = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    html_content = models.TextField(blank=True)
    
    # Template variables
    variables = models.JSONField(default=dict, blank=True)
    sample_data = models.JSONField(default=dict, blank=True)
    
    # Settings
    priority = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    delay_minutes = models.PositiveIntegerField(default=0)
    retry_count = models.PositiveIntegerField(default=3)
    
    # Metadata
    description = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_templates'
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['template_type', 'is_active']),
            models.Index(fields=['category', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"


class NotificationChannel(models.Model):
    """Notification channels and their configurations"""
    
    CHANNEL_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App'),
        ('webhook', 'Webhook'),
        ('slack', 'Slack'),
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
        ('discord', 'Discord'),
        ('facebook', 'Facebook Messenger'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    channel_type = models.CharField(max_length=20, choices=CHANNEL_TYPES)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    # Configuration
    config = models.JSONField(default=dict, blank=True)
    api_key = models.CharField(max_length=255, blank=True)
    api_secret = models.CharField(max_length=255, blank=True)
    webhook_url = models.URLField(blank=True)
    
    # Settings
    rate_limit = models.PositiveIntegerField(default=100)  # per minute
    timeout_seconds = models.PositiveIntegerField(default=30)
    retry_attempts = models.PositiveIntegerField(default=3)
    
    # Metadata
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_channels'
        ordering = ['name']
        indexes = [
            models.Index(fields=['channel_type', 'is_active']),
            models.Index(fields=['is_default']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_channel_type_display()})"


class Notification(models.Model):
    """Individual notifications sent to users"""
    
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Normal'),
        (3, 'High'),
        (4, 'Urgent'),
        (5, 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('bounced', 'Bounced'),
        ('opened', 'Opened'),
        ('clicked', 'Clicked'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE, related_name='notifications')
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE, related_name='notifications')
    
    # Content
    subject = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    html_content = models.TextField(blank=True)
    
    # Metadata
    priority = models.PositiveIntegerField(choices=PRIORITY_CHOICES, default=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    category = models.CharField(max_length=20, choices=NotificationTemplate.CATEGORIES)
    
    # Related objects
    related_object_type = models.CharField(max_length=50, blank=True, null=True)
    related_object_id = models.UUIDField(blank=True, null=True)
    
    # Delivery
    scheduled_at = models.DateTimeField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    opened_at = models.DateTimeField(blank=True, null=True)
    clicked_at = models.DateTimeField(blank=True, null=True)
    
    # Tracking
    external_id = models.CharField(max_length=255, blank=True, null=True)
    delivery_response = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)
    retry_count = models.PositiveIntegerField(default=0)
    
    # User interaction
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['scheduled_at']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_read']),
        ]
    
    def __str__(self):
        return f"{self.notification_id} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.notification_id:
            import uuid
            self.notification_id = f"NOTIF-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def is_delivered(self):
        """Check if notification was delivered"""
        return self.status in ['delivered', 'opened', 'clicked']
    
    @property
    def is_failed(self):
        """Check if notification failed"""
        return self.status in ['failed', 'bounced', 'cancelled']
    
    @property
    def delivery_time(self):
        """Calculate delivery time"""
        if self.sent_at and self.delivered_at:
            return self.delivered_at - self.sent_at
        return None


class NotificationPreference(models.Model):
    """User notification preferences"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_preferences')
    category = models.CharField(max_length=20, choices=NotificationTemplate.CATEGORIES)
    channel_type = models.CharField(max_length=20, choices=NotificationChannel.CHANNEL_TYPES)
    
    # Preferences
    is_enabled = models.BooleanField(default=True)
    frequency = models.CharField(max_length=20, choices=[
        ('immediate', 'Immediate'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('never', 'Never'),
    ], default='immediate')
    
    # Time preferences
    quiet_hours_start = models.TimeField(blank=True, null=True)
    quiet_hours_end = models.TimeField(blank=True, null=True)
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_preferences'
        unique_together = ['user', 'category', 'channel_type']
        ordering = ['user', 'category', 'channel_type']
        indexes = [
            models.Index(fields=['user', 'category']),
            models.Index(fields=['is_enabled']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.category} - {self.channel_type}"


class NotificationBatch(models.Model):
    """Batches of notifications for bulk sending"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE, related_name='batches')
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE, related_name='batches')
    
    # Batch details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_count = models.PositiveIntegerField(default=0)
    sent_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    
    # Scheduling
    scheduled_at = models.DateTimeField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # Configuration
    batch_data = models.JSONField(default=dict, blank=True)
    filters = models.JSONField(default=dict, blank=True)
    
    # Metadata
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_batches'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'scheduled_at']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.batch_id} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.batch_id:
            import uuid
            self.batch_id = f"BATCH-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def success_rate(self):
        """Calculate success rate"""
        if self.total_count > 0:
            return (self.sent_count / self.total_count) * 100
        return 0


class NotificationLog(models.Model):
    """Logs for notification delivery attempts"""
    
    LOG_LEVELS = [
        ('debug', 'Debug'),
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='logs')
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE, related_name='logs')
    
    # Log details
    level = models.CharField(max_length=10, choices=LOG_LEVELS, default='info')
    message = models.TextField()
    details = models.JSONField(default=dict, blank=True)
    
    # Delivery info
    attempt_number = models.PositiveIntegerField(default=1)
    response_code = models.PositiveIntegerField(blank=True, null=True)
    response_message = models.TextField(blank=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notification_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['notification', 'level']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.level.upper()}: {self.message[:50]}"


class NotificationSchedule(models.Model):
    """Scheduled notifications"""
    
    FREQUENCY_CHOICES = [
        ('once', 'Once'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE, related_name='schedules')
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE, related_name='schedules')
    
    # Schedule details
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    next_run = models.DateTimeField(blank=True, null=True)
    
    # Configuration
    is_active = models.BooleanField(default=True)
    max_runs = models.PositiveIntegerField(blank=True, null=True)
    run_count = models.PositiveIntegerField(default=0)
    
    # Filters and conditions
    filters = models.JSONField(default=dict, blank=True)
    conditions = models.JSONField(default=dict, blank=True)
    
    # Metadata
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_schedules'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', 'next_run']),
            models.Index(fields=['frequency', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_frequency_display()})"
    
    @property
    def is_expired(self):
        """Check if schedule has expired"""
        if self.end_date:
            return timezone.now() > self.end_date
        return False
    
    @property
    def can_run(self):
        """Check if schedule can run"""
        if self.max_runs and self.run_count >= self.max_runs:
            return False
        if self.is_expired:
            return False
        return self.is_active and self.next_run and timezone.now() >= self.next_run
