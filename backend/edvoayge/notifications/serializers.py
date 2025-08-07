from rest_framework import serializers
from django.contrib.auth import get_user_model
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

User = get_user_model()


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """Serializer for notification templates"""
    
    template_type_display = serializers.CharField(source='get_template_type_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = NotificationTemplate
        fields = [
            'id', 'name', 'template_type', 'template_type_display', 'category',
            'category_display', 'is_active', 'subject', 'title', 'content',
            'html_content', 'variables', 'sample_data', 'priority',
            'delay_minutes', 'retry_count', 'description', 'tags',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate template data"""
        template_type = data.get('template_type')
        subject = data.get('subject')
        title = data.get('title')
        
        # Validate required fields based on template type
        if template_type == 'email' and not subject:
            raise serializers.ValidationError("Subject is required for email templates")
        
        if template_type in ['push', 'in_app'] and not title:
            raise serializers.ValidationError("Title is required for push and in-app templates")
        
        return data


class NotificationChannelSerializer(serializers.ModelSerializer):
    """Serializer for notification channels"""
    
    channel_type_display = serializers.CharField(source='get_channel_type_display', read_only=True)
    
    class Meta:
        model = NotificationChannel
        fields = [
            'id', 'name', 'channel_type', 'channel_type_display', 'is_active',
            'is_default', 'config', 'webhook_url', 'rate_limit', 'timeout_seconds',
            'retry_attempts', 'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate channel configuration"""
        channel_type = data.get('channel_type')
        webhook_url = data.get('webhook_url')
        
        # Validate webhook URL for webhook channels
        if channel_type == 'webhook' and not webhook_url:
            raise serializers.ValidationError("Webhook URL is required for webhook channels")
        
        return data


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications"""
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    template_details = NotificationTemplateSerializer(source='template', read_only=True)
    channel_details = NotificationChannelSerializer(source='channel', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    is_delivered = serializers.BooleanField(read_only=True)
    is_failed = serializers.BooleanField(read_only=True)
    delivery_time = serializers.DurationField(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_id', 'user', 'template', 'template_details',
            'channel', 'channel_details', 'subject', 'title', 'content',
            'html_content', 'priority', 'priority_display', 'status',
            'status_display', 'category', 'category_display', 'related_object_type',
            'related_object_id', 'scheduled_at', 'sent_at', 'delivered_at',
            'opened_at', 'clicked_at', 'external_id', 'delivery_response',
            'error_message', 'retry_count', 'is_read', 'read_at', 'is_archived',
            'archived_at', 'is_delivered', 'is_failed', 'delivery_time',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'notification_id', 'user', 'template_details', 'channel_details',
            'is_delivered', 'is_failed', 'delivery_time', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        """Create notification with user"""
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for notification preferences"""
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    channel_type_display = serializers.CharField(source='get_channel_type_display', read_only=True)
    frequency_display = serializers.CharField(source='get_frequency_display', read_only=True)
    
    class Meta:
        model = NotificationPreference
        fields = [
            'id', 'user', 'category', 'category_display', 'channel_type',
            'channel_type_display', 'is_enabled', 'frequency', 'frequency_display',
            'quiet_hours_start', 'quiet_hours_end', 'timezone', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate preference data"""
        quiet_hours_start = data.get('quiet_hours_start')
        quiet_hours_end = data.get('quiet_hours_end')
        
        if quiet_hours_start and quiet_hours_end and quiet_hours_start >= quiet_hours_end:
            raise serializers.ValidationError("Quiet hours start must be before end time")
        
        return data
    
    def create(self, validated_data):
        """Create preference with user"""
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class NotificationBatchSerializer(serializers.ModelSerializer):
    """Serializer for notification batches"""
    
    template_details = NotificationTemplateSerializer(source='template', read_only=True)
    channel_details = NotificationChannelSerializer(source='channel', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    success_rate = serializers.FloatField(read_only=True)
    
    class Meta:
        model = NotificationBatch
        fields = [
            'id', 'batch_id', 'name', 'template', 'template_details', 'channel',
            'channel_details', 'status', 'status_display', 'total_count',
            'sent_count', 'failed_count', 'success_rate', 'scheduled_at',
            'started_at', 'completed_at', 'batch_data', 'filters', 'description',
            'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'batch_id', 'template_details', 'channel_details',
            'status_display', 'success_rate', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        """Create batch with user"""
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class NotificationLogSerializer(serializers.ModelSerializer):
    """Serializer for notification logs"""
    
    notification_details = NotificationSerializer(source='notification', read_only=True)
    channel_details = NotificationChannelSerializer(source='channel', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    
    class Meta:
        model = NotificationLog
        fields = [
            'id', 'notification', 'notification_details', 'channel', 'channel_details',
            'level', 'level_display', 'message', 'details', 'attempt_number',
            'response_code', 'response_message', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class NotificationScheduleSerializer(serializers.ModelSerializer):
    """Serializer for notification schedules"""
    
    template_details = NotificationTemplateSerializer(source='template', read_only=True)
    channel_details = NotificationChannelSerializer(source='channel', read_only=True)
    frequency_display = serializers.CharField(source='get_frequency_display', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    can_run = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = NotificationSchedule
        fields = [
            'id', 'name', 'template', 'template_details', 'channel', 'channel_details',
            'frequency', 'frequency_display', 'start_date', 'end_date', 'next_run',
            'is_active', 'max_runs', 'run_count', 'filters', 'conditions',
            'description', 'is_expired', 'can_run', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'template_details', 'channel_details', 'frequency_display',
            'is_expired', 'can_run', 'created_at', 'updated_at'
        ]
    
    def validate(self, data):
        """Validate schedule data"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("End date must be after start date")
        
        return data
    
    def create(self, validated_data):
        """Create schedule with user"""
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class NotificationTemplateCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating notification templates"""
    
    class Meta:
        model = NotificationTemplate
        fields = [
            'name', 'template_type', 'category', 'is_active', 'subject', 'title',
            'content', 'html_content', 'variables', 'sample_data', 'priority',
            'delay_minutes', 'retry_count', 'description', 'tags'
        ]
    
    def validate(self, data):
        """Validate template creation data"""
        template_type = data.get('template_type')
        content = data.get('content')
        
        if not content:
            raise serializers.ValidationError("Content is required for all templates")
        
        return data


class NotificationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating notifications"""
    
    class Meta:
        model = Notification
        fields = [
            'template', 'channel', 'subject', 'title', 'content', 'html_content',
            'priority', 'category', 'related_object_type', 'related_object_id',
            'scheduled_at'
        ]
    
    def validate(self, data):
        """Validate notification creation data"""
        template = data.get('template')
        channel = data.get('channel')
        
        if template and channel and template.template_type != channel.channel_type:
            raise serializers.ValidationError("Template and channel types must match")
        
        return data


class NotificationPreferenceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating notification preferences"""
    
    class Meta:
        model = NotificationPreference
        fields = [
            'category', 'channel_type', 'is_enabled', 'frequency',
            'quiet_hours_start', 'quiet_hours_end', 'timezone'
        ]
    
    def validate(self, data):
        """Validate preference creation data"""
        category = data.get('category')
        channel_type = data.get('channel_type')
        
        # Check if preference already exists
        user = self.context['request'].user
        if NotificationPreference.objects.filter(
            user=user, category=category, channel_type=channel_type
        ).exists():
            raise serializers.ValidationError("Preference already exists for this category and channel")
        
        return data


class NotificationBatchCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating notification batches"""
    
    class Meta:
        model = NotificationBatch
        fields = [
            'name', 'template', 'channel', 'scheduled_at', 'batch_data',
            'filters', 'description'
        ]
    
    def validate(self, data):
        """Validate batch creation data"""
        template = data.get('template')
        channel = data.get('channel')
        
        if template and channel and template.template_type != channel.channel_type:
            raise serializers.ValidationError("Template and channel types must match")
        
        return data


class NotificationScheduleCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating notification schedules"""
    
    class Meta:
        model = NotificationSchedule
        fields = [
            'name', 'template', 'channel', 'frequency', 'start_date', 'end_date',
            'is_active', 'max_runs', 'filters', 'conditions', 'description'
        ]
    
    def validate(self, data):
        """Validate schedule creation data"""
        template = data.get('template')
        channel = data.get('channel')
        
        if template and channel and template.template_type != channel.channel_type:
            raise serializers.ValidationError("Template and channel types must match")
        
        return data


class NotificationStatsSerializer(serializers.Serializer):
    """Serializer for notification statistics"""
    
    total_notifications = serializers.IntegerField()
    sent_notifications = serializers.IntegerField()
    failed_notifications = serializers.IntegerField()
    pending_notifications = serializers.IntegerField()
    delivery_rate = serializers.FloatField()
    average_delivery_time = serializers.DurationField()
    period = serializers.CharField()
    date_range = serializers.ListField(child=serializers.CharField())


class NotificationChannelStatsSerializer(serializers.Serializer):
    """Serializer for notification channel statistics"""
    
    channel_type = serializers.CharField()
    count = serializers.IntegerField()
    success_rate = serializers.FloatField()
    average_delivery_time = serializers.DurationField()
    total_sent = serializers.IntegerField()
    total_failed = serializers.IntegerField()


class NotificationTemplateStatsSerializer(serializers.Serializer):
    """Serializer for notification template statistics"""
    
    template_name = serializers.CharField()
    category = serializers.CharField()
    usage_count = serializers.IntegerField()
    success_rate = serializers.FloatField()
    average_delivery_time = serializers.DurationField()
    last_used = serializers.DateTimeField()


class NotificationPreferenceStatsSerializer(serializers.Serializer):
    """Serializer for notification preference statistics"""
    
    category = serializers.CharField()
    channel_type = serializers.CharField()
    enabled_count = serializers.IntegerField()
    disabled_count = serializers.IntegerField()
    most_common_frequency = serializers.CharField()
    average_quiet_hours = serializers.CharField() 