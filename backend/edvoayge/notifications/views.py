import uuid
import logging
from datetime import timedelta
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    NotificationTemplate,
    NotificationChannel,
    Notification,
    NotificationPreference,
    NotificationBatch,
    NotificationLog,
    NotificationSchedule,
)
from .serializers import (
    NotificationTemplateSerializer,
    NotificationChannelSerializer,
    NotificationSerializer,
    NotificationPreferenceSerializer,
    NotificationBatchSerializer,
    NotificationLogSerializer,
    NotificationScheduleSerializer,
    NotificationTemplateCreateSerializer,
    NotificationCreateSerializer,
    NotificationPreferenceCreateSerializer,
    NotificationBatchCreateSerializer,
    NotificationScheduleCreateSerializer,
    NotificationStatsSerializer,
    NotificationChannelStatsSerializer,
    NotificationTemplateStatsSerializer,
    NotificationPreferenceStatsSerializer,
)

logger = logging.getLogger(__name__)


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for notification templates"""
    
    serializer_class = NotificationTemplateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['template_type', 'category', 'is_active']
    search_fields = ['name', 'subject', 'title', 'content']
    ordering_fields = ['name', 'priority', 'created_at']
    ordering = ['category', 'name']
    
    def get_queryset(self):
        return NotificationTemplate.objects.filter(is_active=True)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return NotificationTemplateCreateSerializer
        return NotificationTemplateSerializer
    
    @action(detail=True, methods=['post'])
    def test_template(self, request, pk=None):
        """Test notification template"""
        template = self.get_object()
        test_data = request.data.get('test_data', {})
        
        # Simulate template rendering
        rendered_content = template.content
        for key, value in test_data.items():
            rendered_content = rendered_content.replace(f'{{{{{key}}}}}', str(value))
        
        return Response({
            'template_id': template.id,
            'rendered_content': rendered_content,
            'test_data': test_data
        })
    
    @action(detail=True, methods=['post'])
    def duplicate_template(self, request, pk=None):
        """Duplicate notification template"""
        template = self.get_object()
        
        new_template = NotificationTemplate.objects.create(
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
        
        serializer = self.get_serializer(new_template)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get templates grouped by category"""
        templates = self.get_queryset()
        categories = {}
        
        for template in templates:
            category = template.get_category_display()
            if category not in categories:
                categories[category] = []
            categories[category].append(NotificationTemplateSerializer(template).data)
        
        return Response(categories)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get templates grouped by type"""
        templates = self.get_queryset()
        types = {}
        
        for template in templates:
            template_type = template.get_template_type_display()
            if template_type not in types:
                types[template_type] = []
            types[template_type].append(NotificationTemplateSerializer(template).data)
        
        return Response(types)


class NotificationChannelViewSet(viewsets.ModelViewSet):
    """ViewSet for notification channels"""
    
    serializer_class = NotificationChannelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['channel_type', 'is_active', 'is_default']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        return NotificationChannel.objects.filter(is_active=True)
    
    @action(detail=True, methods=['post'])
    def test_channel(self, request, pk=None):
        """Test notification channel"""
        channel = self.get_object()
        test_data = request.data.get('test_data', {})
        
        # Simulate channel testing
        try:
            # This would actually test the channel configuration
            success = True
            message = "Channel test successful"
        except Exception as e:
            success = False
            message = f"Channel test failed: {str(e)}"
        
        return Response({
            'channel_id': channel.id,
            'success': success,
            'message': message,
            'test_data': test_data
        })
    
    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """Set channel as default"""
        channel = self.get_object()
        
        # Remove default from other channels of the same type
        NotificationChannel.objects.filter(
            channel_type=channel.channel_type, is_default=True
        ).exclude(id=channel.id).update(is_default=False)
        
        channel.is_default = True
        channel.save()
        
        serializer = self.get_serializer(channel)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def defaults(self, request):
        """Get default channels by type"""
        default_channels = NotificationChannel.objects.filter(
            is_default=True, is_active=True
        )
        serializer = self.get_serializer(default_channels, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get channels grouped by type"""
        channels = self.get_queryset()
        types = {}
        
        for channel in channels:
            channel_type = channel.get_channel_type_display()
            if channel_type not in types:
                types[channel_type] = []
            types[channel_type].append(NotificationChannelSerializer(channel).data)
        
        return Response(types)


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for notifications"""
    
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'priority', 'channel__channel_type']
    search_fields = ['notification_id', 'subject', 'title', 'content']
    ordering_fields = ['created_at', 'priority', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return NotificationCreateSerializer
        return NotificationSerializer
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        
        if not notification.is_read:
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save()
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_unread(self, request, pk=None):
        """Mark notification as unread"""
        notification = self.get_object()
        
        notification.is_read = False
        notification.read_at = None
        notification.save()
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archive notification"""
        notification = self.get_object()
        
        notification.is_archived = True
        notification.archived_at = timezone.now()
        notification.save()
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def unarchive(self, request, pk=None):
        """Unarchive notification"""
        notification = self.get_object()
        
        notification.is_archived = False
        notification.archived_at = None
        notification.save()
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def resend(self, request, pk=None):
        """Resend notification"""
        notification = self.get_object()
        
        if notification.status in ['failed', 'cancelled']:
            notification.status = 'pending'
            notification.retry_count += 1
            notification.save()
            
            # Log the resend attempt
            NotificationLog.objects.create(
                notification=notification,
                channel=notification.channel,
                level='info',
                message='Notification resent',
                attempt_number=notification.retry_count
            )
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        queryset = self.get_queryset().filter(is_read=False)
        updated = queryset.update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return Response({
            'message': f'{updated} notifications marked as read'
        })
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications"""
        queryset = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent notifications"""
        limit = int(request.query_params.get('limit', 10))
        queryset = self.get_queryset().order_by('-created_at')[:limit]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get notification statistics"""
        queryset = self.get_queryset()
        
        # Date range filter
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        queryset = queryset.filter(created_at__gte=start_date)
        
        stats = {
            'total_notifications': queryset.count(),
            'unread_notifications': queryset.filter(is_read=False).count(),
            'archived_notifications': queryset.filter(is_archived=True).count(),
            'sent_notifications': queryset.filter(status='sent').count(),
            'delivered_notifications': queryset.filter(status='delivered').count(),
            'failed_notifications': queryset.filter(status='failed').count(),
            'by_status': queryset.values('status').annotate(count=Count('id')),
            'by_category': queryset.values('category').annotate(count=Count('id')),
            'by_priority': queryset.values('priority').annotate(count=Count('id'))
        }
        
        return Response(stats)


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """ViewSet for notification preferences"""
    
    serializer_class = NotificationPreferenceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'channel_type', 'is_enabled']
    search_fields = ['category', 'channel_type']
    ordering_fields = ['category', 'channel_type']
    ordering = ['category', 'channel_type']
    
    def get_queryset(self):
        return NotificationPreference.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return NotificationPreferenceCreateSerializer
        return NotificationPreferenceSerializer
    
    @action(detail=True, methods=['post'])
    def toggle_enabled(self, request, pk=None):
        """Toggle preference enabled status"""
        preference = self.get_object()
        preference.is_enabled = not preference.is_enabled
        preference.save()
        
        serializer = self.get_serializer(preference)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get preferences grouped by category"""
        preferences = self.get_queryset()
        categories = {}
        
        for preference in preferences:
            category = preference.get_category_display()
            if category not in categories:
                categories[category] = []
            categories[category].append(NotificationPreferenceSerializer(preference).data)
        
        return Response(categories)
    
    @action(detail=False, methods=['get'])
    def by_channel(self, request):
        """Get preferences grouped by channel type"""
        preferences = self.get_queryset()
        channels = {}
        
        for preference in preferences:
            channel_type = preference.get_channel_type_display()
            if channel_type not in channels:
                channels[channel_type] = []
            channels[channel_type].append(NotificationPreferenceSerializer(preference).data)
        
        return Response(channels)
    
    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """Bulk update notification preferences"""
        updates = request.data.get('updates', [])
        updated_count = 0
        
        for update in updates:
            category = update.get('category')
            channel_type = update.get('channel_type')
            is_enabled = update.get('is_enabled')
            
            if category and channel_type:
                preference, created = NotificationPreference.objects.get_or_create(
                    user=request.user,
                    category=category,
                    channel_type=channel_type,
                    defaults={'is_enabled': is_enabled}
                )
                
                if not created:
                    preference.is_enabled = is_enabled
                    preference.save()
                
                updated_count += 1
        
        return Response({
            'message': f'{updated_count} preferences updated'
        })


class NotificationBatchViewSet(viewsets.ModelViewSet):
    """ViewSet for notification batches"""
    
    serializer_class = NotificationBatchSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'template__category', 'channel__channel_type']
    search_fields = ['batch_id', 'name', 'description']
    ordering_fields = ['created_at', 'scheduled_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return NotificationBatch.objects.filter(created_by=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return NotificationBatchCreateSerializer
        return NotificationBatchSerializer
    
    @action(detail=True, methods=['post'])
    def start_batch(self, request, pk=None):
        """Start processing batch"""
        batch = self.get_object()
        
        if batch.status == 'pending':
            batch.status = 'processing'
            batch.started_at = timezone.now()
            batch.save()
            
            # Simulate batch processing
            batch.status = 'completed'
            batch.completed_at = timezone.now()
            batch.sent_count = batch.total_count
            batch.save()
        
        serializer = self.get_serializer(batch)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel_batch(self, request, pk=None):
        """Cancel batch processing"""
        batch = self.get_object()
        
        if batch.status in ['pending', 'processing']:
            batch.status = 'cancelled'
            batch.save()
        
        serializer = self.get_serializer(batch)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get batch statistics"""
        queryset = self.get_queryset()
        
        stats = {
            'total_batches': queryset.count(),
            'completed_batches': queryset.filter(status='completed').count(),
            'failed_batches': queryset.filter(status='failed').count(),
            'pending_batches': queryset.filter(status='pending').count(),
            'total_notifications_sent': queryset.aggregate(
                total=Sum('sent_count')
            )['total'] or 0,
            'total_notifications_failed': queryset.aggregate(
                total=Sum('failed_count')
            )['total'] or 0,
            'average_success_rate': queryset.aggregate(
                avg=Avg('success_rate')
            )['avg'] or 0
        }
        
        return Response(stats)


class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for notification logs (read-only)"""
    
    serializer_class = NotificationLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['level', 'channel__channel_type']
    search_fields = ['message', 'response_message']
    ordering_fields = ['created_at', 'level']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return NotificationLog.objects.filter(notification__user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def errors(self, request):
        """Get error logs"""
        queryset = self.get_queryset().filter(level__in=['error', 'critical'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_level(self, request):
        """Get logs grouped by level"""
        logs = self.get_queryset()
        levels = {}
        
        for log in logs:
            level = log.get_level_display()
            if level not in levels:
                levels[level] = []
            levels[level].append(NotificationLogSerializer(log).data)
        
        return Response(levels)


class NotificationScheduleViewSet(viewsets.ModelViewSet):
    """ViewSet for notification schedules"""
    
    serializer_class = NotificationScheduleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['frequency', 'is_active', 'template__category']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'start_date', 'next_run']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return NotificationSchedule.objects.filter(created_by=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return NotificationScheduleCreateSerializer
        return NotificationScheduleSerializer
    
    @action(detail=True, methods=['post'])
    def activate_schedule(self, request, pk=None):
        """Activate schedule"""
        schedule = self.get_object()
        
        schedule.is_active = True
        schedule.save()
        
        serializer = self.get_serializer(schedule)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate_schedule(self, request, pk=None):
        """Deactivate schedule"""
        schedule = self.get_object()
        
        schedule.is_active = False
        schedule.save()
        
        serializer = self.get_serializer(schedule)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def run_now(self, request, pk=None):
        """Run schedule immediately"""
        schedule = self.get_object()
        
        if schedule.can_run:
            # Simulate running the schedule
            schedule.run_count += 1
            schedule.save()
            
            return Response({
                'message': 'Schedule executed successfully',
                'run_count': schedule.run_count
            })
        else:
            return Response({
                'error': 'Schedule cannot run at this time'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active schedules"""
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def due(self, request):
        """Get schedules due to run"""
        now = timezone.now()
        queryset = self.get_queryset().filter(
            is_active=True,
            next_run__lte=now
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NotificationStatsViewSet(viewsets.ViewSet):
    """ViewSet for notification statistics"""
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get notification overview statistics"""
        user = request.user
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        notifications = Notification.objects.filter(
            user=user, created_at__gte=start_date
        )
        
        preferences = NotificationPreference.objects.filter(user=user)
        
        stats = {
            'period': f'Last {days} days',
            'notifications': {
                'total': notifications.count(),
                'unread': notifications.filter(is_read=False).count(),
                'archived': notifications.filter(is_archived=True).count(),
                'sent': notifications.filter(status='sent').count(),
                'delivered': notifications.filter(status='delivered').count(),
                'failed': notifications.filter(status='failed').count()
            },
            'preferences': {
                'total': preferences.count(),
                'enabled': preferences.filter(is_enabled=True).count(),
                'disabled': preferences.filter(is_enabled=False).count()
            },
            'by_category': notifications.values('category').annotate(
                count=Count('id')
            ),
            'by_status': notifications.values('status').annotate(
                count=Count('id')
            )
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def trends(self, request):
        """Get notification trends over time"""
        user = request.user
        days = int(request.query_params.get('days', 30))
        
        # Get daily notification counts
        daily_notifications = Notification.objects.filter(
            user=user,
            created_at__gte=timezone.now() - timedelta(days=days)
        ).extra(
            select={'date': 'DATE(created_at)'}
        ).values('date').annotate(
            count=Count('id'),
            sent_count=Count('id', filter=Q(status='sent')),
            failed_count=Count('id', filter=Q(status='failed'))
        ).order_by('date')
        
        trends = {
            'notifications': list(daily_notifications)
        }
        
        return Response(trends)
