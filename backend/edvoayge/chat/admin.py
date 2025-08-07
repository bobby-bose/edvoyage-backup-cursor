from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ChatUser, ChatRoom, ChatRoomParticipant, Message, 
    MessageStatus, Contact, ChatNotification
)


@admin.register(ChatUser)
class ChatUserAdmin(admin.ModelAdmin):
    """Admin interface for ChatUser model"""
    list_display = [
        'id', 'user', 'full_name', 'role', 'institution', 
        'specialization', 'is_online', 'is_verified', 'created_at'
    ]
    list_filter = ['role', 'institution', 'specialization', 'is_verified', 'is_online', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'bio', 'institution']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'profile_image', 'bio')
        }),
        ('Medical Information', {
            'fields': ('specialization', 'institution', 'role')
        }),
        ('Status', {
            'fields': ('is_online', 'last_seen', 'is_verified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    """Admin interface for ChatRoom model"""
    list_display = [
        'id', 'name', 'type', 'created_by', 'participant_count', 
        'message_count', 'created_at'
    ]
    list_filter = ['type', 'created_at']
    search_fields = ['name', 'created_by__user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Room Information', {
            'fields': ('name', 'type', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def participant_count(self, obj):
        return obj.participants.filter(is_active=True).count()
    participant_count.short_description = 'Participants'

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(ChatRoomParticipant)
class ChatRoomParticipantAdmin(admin.ModelAdmin):
    """Admin interface for ChatRoomParticipant model"""
    list_display = [
        'id', 'room', 'user', 'role', 'is_active', 'joined_at', 'left_at'
    ]
    list_filter = ['role', 'is_active', 'joined_at']
    search_fields = ['room__name', 'user__user__username']
    readonly_fields = ['id', 'joined_at']
    ordering = ['-joined_at']
    
    fieldsets = (
        ('Participation', {
            'fields': ('room', 'user', 'role')
        }),
        ('Status', {
            'fields': ('is_active', 'left_at')
        }),
        ('Timestamps', {
            'fields': ('joined_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin interface for Message model"""
    list_display = [
        'id', 'room', 'sender', 'content_preview', 'message_type', 
        'is_edited', 'created_at'
    ]
    list_filter = ['message_type', 'is_edited', 'created_at', 'room__type']
    search_fields = ['content', 'sender__user__username', 'room__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Message Information', {
            'fields': ('room', 'sender', 'content', 'message_type')
        }),
        ('Media', {
            'fields': ('media_url', 'file_name', 'file_size'),
            'classes': ('collapse',)
        }),
        ('Reply', {
            'fields': ('reply_to',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_edited', 'edited_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(MessageStatus)
class MessageStatusAdmin(admin.ModelAdmin):
    """Admin interface for MessageStatus model"""
    list_display = [
        'id', 'message', 'user', 'status', 'updated_at'
    ]
    list_filter = ['status', 'updated_at']
    search_fields = ['message__content', 'user__user__username']
    readonly_fields = ['id', 'updated_at']
    ordering = ['-updated_at']
    
    fieldsets = (
        ('Status Information', {
            'fields': ('message', 'user', 'status')
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin interface for Contact model"""
    list_display = [
        'id', 'user', 'contact', 'nickname', 'is_favorite', 
        'is_blocked', 'created_at'
    ]
    list_filter = ['is_favorite', 'is_blocked', 'created_at']
    search_fields = ['user__user__username', 'contact__user__username', 'nickname']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('user', 'contact', 'nickname')
        }),
        ('Status', {
            'fields': ('is_favorite', 'is_blocked')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ChatNotification)
class ChatNotificationAdmin(admin.ModelAdmin):
    """Admin interface for ChatNotification model"""
    list_display = [
        'id', 'user', 'type', 'is_read', 'created_at'
    ]
    list_filter = ['type', 'is_read', 'created_at']
    search_fields = ['user__user__username', 'message__content']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Notification Information', {
            'fields': ('user', 'message', 'type')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


# Customize admin site
admin.site.site_title = "Chat Admin Portal"
admin.site.index_title = "Welcome to Chat Administration"
