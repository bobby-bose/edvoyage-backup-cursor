from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Q
from django.utils import timezone
from .models import (
    NotificationTemplate,
    NotificationChannel,
    Notification,
    NotificationPreference,
    NotificationBatch,
    NotificationLog,
    NotificationSchedule,
)


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'template_type', 'category', 'is_active', 'priority',
        'delay_minutes', 'retry_count', 'created_at'
    ]
    list_filter = [
        'template_type', 'category', 'is_active', 'priority', 'created_at'
    ]
    search_fields = [
        'name', 'subject', 'title', 'content', 'description'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at'
    ]
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'template_type', 'category', 'is_active')
        }),
        ('Content', {
            'fields': ('subject', 'title', 'content', 'html_content')
        }),
        ('Template Variables', {
            'fields': ('variables', 'sample_data'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('priority', 'delay_minutes', 'retry_count')
        }),
        ('Metadata', {
            'fields': ('description', 'tags'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_templates', 'deactivate_templates', 'duplicate_templates']
    
    def activate_templates(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} templates activated.')
    activate_templates.short_description = "Activate selected templates"
    
    def deactivate_templates(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} templates deactivated.')
    deactivate_templates.short_description = "Deactivate selected templates"
    
    def duplicate_templates(self, request, queryset):
        for template in queryset:
            NotificationTemplate.objects.create(
                name=f"{template.name} (Copy)",
                template_type=template.template_type,
                category=template.category,
                subject=template.subject,
                title=template.title,
                content=template.content,
                html_content=template.html_content,
                variables=template.variables,
                sample_data=template.sample_data,
                priority=template.priority,
                delay_minutes=template.delay_minutes,
                retry_count=template.retry_count,
                description=template.description,
                tags=template.tags
            )
        self.message_user(request, f'{queryset.count()} templates duplicated.')
    duplicate_templates.short_description = "Duplicate selected templates"


@admin.register(NotificationChannel)
class NotificationChannelAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'channel_type', 'is_active', 'is_default', 'rate_limit',
        'timeout_seconds', 'retry_attempts', 'created_at'
    ]
    list_filter = [
        'channel_type', 'is_active', 'is_default', 'created_at'
    ]
    search_fields = [
        'name', 'description', 'webhook_url'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at'
    ]
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'channel_type', 'is_active', 'is_default')
        }),
        ('Configuration', {
            'fields': ('config', 'api_key', 'api_secret', 'webhook_url'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('rate_limit', 'timeout_seconds', 'retry_attempts')
        }),
        ('Metadata', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_channels', 'deactivate_channels', 'set_as_default']
    
    def activate_channels(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} channels activated.')
    activate_channels.short_description = "Activate selected channels"
    
    def deactivate_channels(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} channels deactivated.')
    deactivate_channels.short_description = "Deactivate selected channels"
    
    def set_as_default(self, request, queryset):
        for channel in queryset:
            # Remove default from other channels of the same type
            NotificationChannel.objects.filter(
                channel_type=channel.channel_type, is_default=True
            ).exclude(id=channel.id).update(is_default=False)
            channel.is_default = True
            channel.save()
        self.message_user(request, f'{queryset.count()} channels set as default.')
    set_as_default.short_description = "Set selected channels as default"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'notification_id', 'user', 'template', 'channel', 'priority', 'status',
        'category', 'is_read', 'is_archived', 'created_at'
    ]
    list_filter = [
        'status', 'category', 'priority', 'is_read', 'is_archived', 'created_at',
        'user__email'
    ]
    search_fields = [
        'notification_id', 'subject', 'title', 'content', 'user__email',
        'user__first_name', 'user__last_name'
    ]
    readonly_fields = [
        'id', 'notification_id', 'is_delivered', 'is_failed', 'delivery_time',
        'created_at', 'updated_at'
    ]
    list_select_related = ['user', 'template', 'channel']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'notification_id', 'user', 'template', 'channel')
        }),
        ('Content', {
            'fields': ('subject', 'title', 'content', 'html_content')
        }),
        ('Metadata', {
            'fields': ('priority', 'status', 'category', 'related_object_type', 'related_object_id')
        }),
        ('Delivery', {
            'fields': ('scheduled_at', 'sent_at', 'delivered_at', 'opened_at', 'clicked_at'),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('external_id', 'delivery_response', 'error_message', 'retry_count'),
            'classes': ('collapse',)
        }),
        ('User Interaction', {
            'fields': ('is_read', 'read_at', 'is_archived', 'archived_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_sent', 'mark_as_delivered', 'mark_as_failed', 'mark_all_read']
    
    def mark_as_sent(self, request, queryset):
        updated = queryset.update(
            status='sent',
            sent_at=timezone.now()
        )
        self.message_user(request, f'{updated} notifications marked as sent.')
    mark_as_sent.short_description = "Mark selected notifications as sent"
    
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(
            status='delivered',
            delivered_at=timezone.now()
        )
        self.message_user(request, f'{updated} notifications marked as delivered.')
    mark_as_delivered.short_description = "Mark selected notifications as delivered"
    
    def mark_as_failed(self, request, queryset):
        updated = queryset.update(status='failed')
        self.message_user(request, f'{updated} notifications marked as failed.')
    mark_as_failed.short_description = "Mark selected notifications as failed"
    
    def mark_all_read(self, request, queryset):
        updated = queryset.update(
            is_read=True,
            read_at=timezone.now()
        )
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_all_read.short_description = "Mark selected notifications as read"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'template', 'channel')


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'category', 'channel_type', 'is_enabled', 'frequency',
        'quiet_hours_start', 'quiet_hours_end', 'created_at'
    ]
    list_filter = [
        'category', 'channel_type', 'is_enabled', 'frequency', 'created_at',
        'user__email'
    ]
    search_fields = [
        'user__email', 'user__first_name', 'user__last_name', 'category', 'channel_type'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at'
    ]
    list_select_related = ['user']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'category', 'channel_type')
        }),
        ('Preferences', {
            'fields': ('is_enabled', 'frequency')
        }),
        ('Time Preferences', {
            'fields': ('quiet_hours_start', 'quiet_hours_end', 'timezone'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['enable_preferences', 'disable_preferences']
    
    def enable_preferences(self, request, queryset):
        updated = queryset.update(is_enabled=True)
        self.message_user(request, f'{updated} preferences enabled.')
    enable_preferences.short_description = "Enable selected preferences"
    
    def disable_preferences(self, request, queryset):
        updated = queryset.update(is_enabled=False)
        self.message_user(request, f'{updated} preferences disabled.')
    disable_preferences.short_description = "Disable selected preferences"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(NotificationBatch)
class NotificationBatchAdmin(admin.ModelAdmin):
    list_display = [
        'batch_id', 'name', 'template', 'channel', 'status', 'total_count',
        'sent_count', 'failed_count', 'success_rate', 'created_at'
    ]
    list_filter = [
        'status', 'template__category', 'channel__channel_type', 'created_at',
        'created_by__email'
    ]
    search_fields = [
        'batch_id', 'name', 'description', 'created_by__email'
    ]
    readonly_fields = [
        'id', 'batch_id', 'success_rate', 'created_at', 'updated_at'
    ]
    list_select_related = ['template', 'channel', 'created_by']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'batch_id', 'name', 'template', 'channel', 'created_by')
        }),
        ('Batch Details', {
            'fields': ('status', 'total_count', 'sent_count', 'failed_count', 'success_rate')
        }),
        ('Scheduling', {
            'fields': ('scheduled_at', 'started_at', 'completed_at'),
            'classes': ('collapse',)
        }),
        ('Configuration', {
            'fields': ('batch_data', 'filters'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['start_batches', 'cancel_batches', 'mark_as_completed']
    
    def start_batches(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='processing',
            started_at=timezone.now()
        )
        self.message_user(request, f'{updated} batches started.')
    start_batches.short_description = "Start selected batches"
    
    def cancel_batches(self, request, queryset):
        updated = queryset.filter(status__in=['pending', 'processing']).update(
            status='cancelled'
        )
        self.message_user(request, f'{updated} batches cancelled.')
    cancel_batches.short_description = "Cancel selected batches"
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(
            status='completed',
            completed_at=timezone.now()
        )
        self.message_user(request, f'{updated} batches marked as completed.')
    mark_as_completed.short_description = "Mark selected batches as completed"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('template', 'channel', 'created_by')


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'notification', 'channel', 'level', 'attempt_number',
        'response_code', 'created_at'
    ]
    list_filter = [
        'level', 'channel__channel_type', 'created_at'
    ]
    search_fields = [
        'message', 'response_message', 'notification__notification_id'
    ]
    readonly_fields = [
        'id', 'created_at'
    ]
    list_select_related = ['notification', 'channel']
    list_per_page = 100
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'notification', 'channel', 'level')
        }),
        ('Log Details', {
            'fields': ('message', 'details')
        }),
        ('Delivery Info', {
            'fields': ('attempt_number', 'response_code', 'response_message'),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['clear_old_logs']
    
    def clear_old_logs(self, request, queryset):
        from datetime import timedelta
        cutoff_date = timezone.now() - timedelta(days=30)
        deleted, _ = NotificationLog.objects.filter(created_at__lt=cutoff_date).delete()
        self.message_user(request, f'{deleted} old notification logs deleted.')
    clear_old_logs.short_description = "Clear logs older than 30 days"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('notification', 'channel')


@admin.register(NotificationSchedule)
class NotificationScheduleAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'template', 'channel', 'frequency', 'is_active',
        'run_count', 'next_run', 'is_expired', 'can_run', 'created_at'
    ]
    list_filter = [
        'frequency', 'is_active', 'created_at', 'created_by__email'
    ]
    search_fields = [
        'name', 'description', 'created_by__email'
    ]
    readonly_fields = [
        'id', 'is_expired', 'can_run', 'created_at', 'updated_at'
    ]
    list_select_related = ['template', 'channel', 'created_by']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'template', 'channel', 'created_by')
        }),
        ('Schedule Details', {
            'fields': ('frequency', 'start_date', 'end_date', 'next_run')
        }),
        ('Configuration', {
            'fields': ('is_active', 'max_runs', 'run_count')
        }),
        ('Filters and Conditions', {
            'fields': ('filters', 'conditions'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_schedules', 'deactivate_schedules', 'run_now']
    
    def activate_schedules(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} schedules activated.')
    activate_schedules.short_description = "Activate selected schedules"
    
    def deactivate_schedules(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} schedules deactivated.')
    deactivate_schedules.short_description = "Deactivate selected schedules"
    
    def run_now(self, request, queryset):
        for schedule in queryset:
            if schedule.can_run:
                schedule.run_count += 1
                schedule.save()
        self.message_user(request, f'{queryset.count()} schedules executed.')
    run_now.short_description = "Run selected schedules now"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('template', 'channel', 'created_by')
