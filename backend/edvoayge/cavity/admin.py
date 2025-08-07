from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Post, PostLike, Comment, CommentLike, 
    PostShare, Notification, UserFollow
)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for Post model"""
    list_display = [
        'id', 'author', 'content_preview', 'year', 'post_type', 
        'like_count', 'comment_count', 'share_count', 
        'is_anonymous', 'is_edited', 'created_at'
    ]
    list_filter = ['year', 'post_type', 'is_anonymous', 'is_edited', 'created_at']
    search_fields = ['content', 'author__username', 'author__first_name', 'year']
    readonly_fields = ['id', 'like_count', 'comment_count', 'share_count', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Post Information', {
            'fields': ('author', 'content', 'year', 'media_urls', 'is_anonymous')
        }),
        ('Status', {
            'fields': ('post_type', 'is_edited', 'edit_history')
        }),
        ('Statistics', {
            'fields': ('like_count', 'comment_count', 'share_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model"""
    list_display = [
        'id', 'author', 'post_preview', 'content_preview', 
        'parent_comment', 'like_count', 'replies_count',
        'is_edited', 'created_at'
    ]
    list_filter = ['is_edited', 'created_at']
    search_fields = ['content', 'author__username', 'post__content']
    readonly_fields = ['id', 'like_count', 'replies_count', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('author', 'post', 'parent_comment', 'content')
        }),
        ('Status', {
            'fields': ('is_edited', 'edit_history')
        }),
        ('Statistics', {
            'fields': ('like_count', 'replies_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

    def post_preview(self, obj):
        return obj.post.content[:30] + '...' if len(obj.post.content) > 30 else obj.post.content
    post_preview.short_description = 'Post Preview'

    def replies_count(self, obj):
        return obj.replies.count()
    replies_count.short_description = 'Replies Count'


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    """Admin interface for PostLike model"""
    list_display = ['id', 'user', 'post_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__content']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']

    def post_preview(self, obj):
        return obj.post.content[:50] + '...' if len(obj.post.content) > 50 else obj.post.content
    post_preview.short_description = 'Post Preview'


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    """Admin interface for CommentLike model"""
    list_display = ['id', 'user', 'comment_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'comment__content']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']

    def comment_preview(self, obj):
        return obj.comment.content[:50] + '...' if len(obj.comment.content) > 50 else obj.comment.content
    comment_preview.short_description = 'Comment Preview'


@admin.register(PostShare)
class PostShareAdmin(admin.ModelAdmin):
    """Admin interface for PostShare model"""
    list_display = ['id', 'user', 'post_preview', 'share_text', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__content', 'share_text']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']

    def post_preview(self, obj):
        return obj.post.content[:50] + '...' if len(obj.post.content) > 50 else obj.post.content
    post_preview.short_description = 'Post Preview'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification model"""
    list_display = [
        'id', 'recipient', 'sender', 'notification_type', 'message_preview', 
        'is_read', 'created_at'
    ]
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__username', 'sender__username', 'message']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Notification Information', {
            'fields': ('recipient', 'sender', 'notification_type', 'message')
        }),
        ('References', {
            'fields': ('post', 'comment')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message Preview'


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    """Admin interface for UserFollow model"""
    list_display = ['id', 'follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'following__username']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']


# Custom admin site configuration
admin.site.site_header = "Cavity Admin"
admin.site.site_title = "Cavity Admin Portal"
admin.site.index_title = "Welcome to Cavity Administration"
