from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Content, ContentCategory, ContentTag, ContentView, ContentRating,
    ContentComment, ContentShare, ContentDownload, ContentBookmark, ContentAnalytics, Feed
)

@admin.register(ContentCategory)
class ContentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'content_count')
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'color', 'icon', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_count(self, obj):
        return obj.contents.count()
    content_count.short_description = 'Contents'

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'content_type', 'status', 'is_public', 'is_featured', 'is_premium', 'view_count', 'average_rating', 'created_at')
    list_filter = ('status', 'content_type', 'is_public', 'is_featured', 'is_premium', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'author__username', 'category__name')
    readonly_fields = ('author', 'view_count', 'download_count', 'share_count', 'average_rating', 'rating_count', 'created_at', 'updated_at', 'published_at', 'is_active', 'tags_list')
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'content_type', 'category', 'author')
        }),
        ('Content Details', {
            'fields': ('file_url', 'file_size', 'duration', 'thumbnail_url')
        }),
        ('Content Properties', {
            'fields': ('status', 'is_public', 'is_featured', 'is_premium')
        }),
        ('SEO and Metadata', {
            'fields': ('meta_title', 'meta_description', 'keywords'),
            'classes': ('collapse',)
        }),
        ('Analytics', {
            'fields': ('view_count', 'download_count', 'share_count', 'average_rating', 'rating_count', 'tags_list'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_active(self, obj):
        return obj.is_active
    is_active.boolean = True
    is_active.short_description = 'Active'
    
    def tags_list(self, obj):
        return ', '.join(obj.tags_list)
    tags_list.short_description = 'Tags'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'author').prefetch_related('tags')

@admin.register(ContentTag)
class ContentTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'content_count', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'content_count')
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'color', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_count(self, obj):
        return obj.contents.count()
    content_count.short_description = 'Contents'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('contents')

@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'ip_address', 'view_duration', 'created_at')
    list_filter = ('content', 'created_at')
    search_fields = ('content__title', 'user__username', 'ip_address')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('View Information', {
            'fields': ('content', 'user', 'ip_address', 'user_agent', 'referrer', 'session_id', 'view_duration')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('content', 'user')

@admin.register(ContentRating)
class ContentRatingAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'rating', 'is_helpful', 'created_at')
    list_filter = ('rating', 'is_helpful', 'content', 'created_at', 'updated_at')
    search_fields = ('content__title', 'user__username', 'review')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25
    
    fieldsets = (
        ('Rating Information', {
            'fields': ('content', 'user', 'rating', 'review', 'is_helpful')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('content', 'user')

@admin.register(ContentComment)
class ContentCommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'comment_preview', 'is_approved', 'is_reply', 'replies_count', 'created_at')
    list_filter = ('is_approved', 'is_edited', 'content', 'created_at', 'updated_at')
    search_fields = ('content__title', 'user__username', 'comment')
    readonly_fields = ('created_at', 'updated_at', 'edited_at', 'is_reply', 'replies_count')
    list_per_page = 25
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('content', 'user', 'parent', 'comment', 'is_approved', 'is_edited', 'edited_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def comment_preview(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    comment_preview.short_description = 'Comment'
    
    def is_reply(self, obj):
        return obj.is_reply
    is_reply.boolean = True
    is_reply.short_description = 'Reply'
    
    def replies_count(self, obj):
        return obj.replies_count
    replies_count.short_description = 'Replies'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('content', 'user', 'parent')

@admin.register(ContentShare)
class ContentShareAdmin(admin.ModelAdmin):
    list_display = ('content', 'shared_by', 'shared_with', 'share_type', 'is_viewed', 'created_at')
    list_filter = ('share_type', 'is_viewed', 'content', 'created_at')
    search_fields = ('content__title', 'shared_by__username', 'shared_with__username')
    readonly_fields = ('created_at', 'viewed_at')
    list_per_page = 25
    
    fieldsets = (
        ('Share Information', {
            'fields': ('content', 'shared_by', 'shared_with', 'share_type', 'message', 'share_url')
        }),
        ('View Tracking', {
            'fields': ('is_viewed', 'viewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('content', 'shared_by', 'shared_with')

@admin.register(ContentDownload)
class ContentDownloadAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'download_url_preview', 'file_size', 'created_at')
    list_filter = ('content', 'created_at')
    search_fields = ('content__title', 'user__username', 'download_url')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Download Information', {
            'fields': ('content', 'user', 'ip_address', 'user_agent', 'download_url', 'file_size')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def download_url_preview(self, obj):
        return obj.download_url[:50] + '...' if len(obj.download_url) > 50 else obj.download_url
    download_url_preview.short_description = 'Download URL'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('content', 'user')

@admin.register(ContentBookmark)
class ContentBookmarkAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'notes_preview', 'created_at')
    list_filter = ('content', 'created_at')
    search_fields = ('content__title', 'user__username', 'notes')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Bookmark Information', {
            'fields': ('content', 'user', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def notes_preview(self, obj):
        return obj.notes[:50] + '...' if len(obj.notes) > 50 else obj.notes
    notes_preview.short_description = 'Notes'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('content', 'user')

@admin.register(ContentAnalytics)
class ContentAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'action_type', 'ip_address', 'user_agent_preview', 'created_at')
    list_filter = ('action_type', 'content', 'created_at')
    search_fields = ('content__title', 'user__username', 'ip_address')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Analytics Information', {
            'fields': ('content', 'user', 'action_type', 'ip_address', 'user_agent', 'referrer', 'session_id', 'metadata')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def user_agent_preview(self, obj):
        if obj.user_agent:
            return obj.user_agent[:50] + '...' if len(obj.user_agent) > 50 else obj.user_agent
        return '-'
    user_agent_preview.short_description = 'User Agent'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('content', 'user')

@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_name', 'date_posted')
    search_fields = ('title', 'user_name', 'description')
    list_filter = ('date_posted',)

# Custom admin actions
@admin.action(description="Publish selected contents")
def publish_contents(modeladmin, request, queryset):
    updated = queryset.update(status='published')
    modeladmin.message_user(request, f'{updated} contents were successfully published.')

@admin.action(description="Archive selected contents")
def archive_contents(modeladmin, request, queryset):
    updated = queryset.update(status='archived')
    modeladmin.message_user(request, f'{updated} contents were successfully archived.')

@admin.action(description="Feature selected contents")
def feature_contents(modeladmin, request, queryset):
    updated = queryset.update(is_featured=True)
    modeladmin.message_user(request, f'{updated} contents were successfully featured.')

@admin.action(description="Unfeature selected contents")
def unfeature_contents(modeladmin, request, queryset):
    updated = queryset.update(is_featured=False)
    modeladmin.message_user(request, f'{updated} contents were successfully unfeatured.')

@admin.action(description="Make selected contents public")
def make_public(modeladmin, request, queryset):
    updated = queryset.update(is_public=True)
    modeladmin.message_user(request, f'{updated} contents were successfully made public.')

@admin.action(description="Make selected contents private")
def make_private(modeladmin, request, queryset):
    updated = queryset.update(is_public=False)
    modeladmin.message_user(request, f'{updated} contents were successfully made private.')

@admin.action(description="Make selected contents premium")
def make_premium(modeladmin, request, queryset):
    updated = queryset.update(is_premium=True)
    modeladmin.message_user(request, f'{updated} contents were successfully made premium.')

@admin.action(description="Make selected contents non-premium")
def make_non_premium(modeladmin, request, queryset):
    updated = queryset.update(is_premium=False)
    modeladmin.message_user(request, f'{updated} contents were successfully made non-premium.')

# Add actions to ContentAdmin
ContentAdmin.actions = [publish_contents, archive_contents, feature_contents, unfeature_contents, make_public, make_private, make_premium, make_non_premium]
