from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Q
from .models import (
    Bookmark,
    BookmarkCategory,
    BookmarkNote,
    BookmarkCollection,
    BookmarkShare,
    BookmarkAnalytics,
    BookmarkTag,
    BookmarkAccessLog,
)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'user', 'category', 'is_favorite', 'access_count',
        'created_at', 'updated_at', 'status'
    ]
    list_filter = [
        'status', 'is_favorite', 'category', 'created_at', 'updated_at',
        'user__email', 'tags'
    ]
    search_fields = [
        'title', 'description', 'url', 'user__email', 'user__first_name',
        'user__last_name', 'category__name', 'tags__name'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'access_count', 'last_accessed_at',
        'share_count', 'favorite_count'
    ]
    filter_horizontal = ['tags']
    list_select_related = ['user', 'category']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'title', 'description', 'url', 'category')
        }),
        ('Content', {
            'fields': ('content', 'tags', 'metadata')
        }),
        ('Status', {
            'fields': ('status', 'is_favorite', 'is_public')
        }),
        ('Analytics', {
            'fields': ('access_count', 'last_accessed_at', 'share_count', 'favorite_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_favorite', 'mark_as_unfavorite', 'make_public', 'make_private']
    
    def mark_as_favorite(self, request, queryset):
        updated = queryset.update(is_favorite=True)
        self.message_user(request, f'{updated} bookmarks marked as favorite.')
    mark_as_favorite.short_description = "Mark selected bookmarks as favorite"
    
    def mark_as_unfavorite(self, request, queryset):
        updated = queryset.update(is_favorite=False)
        self.message_user(request, f'{updated} bookmarks marked as unfavorite.')
    mark_as_unfavorite.short_description = "Mark selected bookmarks as unfavorite"
    
    def make_public(self, request, queryset):
        updated = queryset.update(is_public=True)
        self.message_user(request, f'{updated} bookmarks made public.')
    make_public.short_description = "Make selected bookmarks public"
    
    def make_private(self, request, queryset):
        updated = queryset.update(is_public=False)
        self.message_user(request, f'{updated} bookmarks made private.')
    make_private.short_description = "Make selected bookmarks private"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'category').prefetch_related('tags')


@admin.register(BookmarkCategory)
class BookmarkCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'user', 'bookmark_count', 'is_default', 'color',
        'created_at', 'updated_at'
    ]
    list_filter = [
        'is_default', 'color', 'created_at', 'updated_at',
        'user__email'
    ]
    search_fields = [
        'name', 'description', 'user__email', 'user__first_name',
        'user__last_name'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'bookmark_count'
    ]
    list_select_related = ['user']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'name', 'description', 'color')
        }),
        ('Settings', {
            'fields': ('is_default', 'sort_order')
        }),
        ('Analytics', {
            'fields': ('bookmark_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_default', 'remove_default']
    
    def make_default(self, request, queryset):
        # Remove default from other categories of the same user
        for category in queryset:
            BookmarkCategory.objects.filter(
                user=category.user, is_default=True
            ).exclude(id=category.id).update(is_default=False)
        
        updated = queryset.update(is_default=True)
        self.message_user(request, f'{updated} categories set as default.')
    make_default.short_description = "Set selected categories as default"
    
    def remove_default(self, request, queryset):
        updated = queryset.update(is_default=False)
        self.message_user(request, f'{updated} categories removed as default.')
    remove_default.short_description = "Remove default status from selected categories"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').annotate(
            bookmark_count=Count('bookmarks')
        )


@admin.register(BookmarkNote)
class BookmarkNoteAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'bookmark', 'user', 'note_type', 'created_at', 'updated_at'
    ]
    list_filter = [
        'note_type', 'created_at', 'updated_at', 'user__email'
    ]
    search_fields = [
        'content', 'bookmark__title', 'user__email', 'user__first_name',
        'user__last_name'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at'
    ]
    list_select_related = ['bookmark', 'user']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'bookmark', 'user', 'note_type')
        }),
        ('Content', {
            'fields': ('content', 'metadata')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('bookmark', 'user')


@admin.register(BookmarkCollection)
class BookmarkCollectionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'user', 'bookmark_count', 'is_public', 'share_count',
        'created_at', 'updated_at'
    ]
    list_filter = [
        'is_public', 'created_at', 'updated_at', 'user__email'
    ]
    search_fields = [
        'name', 'description', 'user__email', 'user__first_name',
        'user__last_name'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'bookmark_count', 'share_count'
    ]
    list_select_related = ['user']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'name', 'description')
        }),
        ('Settings', {
            'fields': ('is_public', 'sort_order')
        }),
        ('Analytics', {
            'fields': ('bookmark_count', 'share_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_public', 'make_private']
    
    def make_public(self, request, queryset):
        updated = queryset.update(is_public=True)
        self.message_user(request, f'{updated} collections made public.')
    make_public.short_description = "Make selected collections public"
    
    def make_private(self, request, queryset):
        updated = queryset.update(is_public=False)
        self.message_user(request, f'{updated} collections made private.')
    make_private.short_description = "Make selected collections private"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').annotate(
            bookmark_count=Count('bookmarks'),
            share_count=Count('shares')
        )


@admin.register(BookmarkShare)
class BookmarkShareAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'share_type', 'shared_by', 'shared_with', 'access_count',
        'is_active', 'expires_at', 'created_at'
    ]
    list_filter = [
        'share_type', 'is_active', 'created_at', 'expires_at',
        'shared_by__email', 'shared_with__email'
    ]
    search_fields = [
        'share_code', 'shared_by__email', 'shared_by__first_name',
        'shared_by__last_name', 'shared_with__email', 'shared_with__first_name',
        'shared_with__last_name'
    ]
    readonly_fields = [
        'id', 'share_code', 'created_at', 'access_count', 'last_accessed_at'
    ]
    list_select_related = ['shared_by', 'shared_with']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'share_code', 'share_type', 'shared_by', 'shared_with')
        }),
        ('Settings', {
            'fields': ('is_active', 'expires_at', 'permissions')
        }),
        ('Analytics', {
            'fields': ('access_count', 'last_accessed_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_shares', 'deactivate_shares', 'extend_expiry']
    
    def activate_shares(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} shares activated.')
    activate_shares.short_description = "Activate selected shares"
    
    def deactivate_shares(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} shares deactivated.')
    deactivate_shares.short_description = "Deactivate selected shares"
    
    def extend_expiry(self, request, queryset):
        from datetime import timedelta
        from django.utils import timezone
        
        # Extend expiry by 30 days
        new_expiry = timezone.now() + timedelta(days=30)
        updated = queryset.update(expires_at=new_expiry)
        self.message_user(request, f'{updated} shares extended by 30 days.')
    extend_expiry.short_description = "Extend expiry by 30 days"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('shared_by', 'shared_with')


@admin.register(BookmarkAnalytics)
class BookmarkAnalyticsAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'analytics_type', 'user', 'bookmark', 'collection',
        'access_count', 'created_at'
    ]
    list_filter = [
        'analytics_type', 'created_at', 'user__email'
    ]
    search_fields = [
        'user__email', 'user__first_name', 'user__last_name',
        'bookmark__title', 'collection__name'
    ]
    readonly_fields = [
        'id', 'created_at', 'access_count', 'last_accessed_at'
    ]
    list_select_related = ['user', 'bookmark', 'collection']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'analytics_type', 'user')
        }),
        ('Related Objects', {
            'fields': ('bookmark', 'collection', 'category')
        }),
        ('Analytics Data', {
            'fields': ('access_count', 'last_accessed_at', 'analytics_data')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'bookmark', 'collection')


@admin.register(BookmarkTag)
class BookmarkTagAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'user', 'bookmark_count', 'color', 'created_at'
    ]
    list_filter = [
        'color', 'created_at', 'user__email'
    ]
    search_fields = [
        'name', 'user__email', 'user__first_name', 'user__last_name'
    ]
    readonly_fields = [
        'id', 'created_at', 'bookmark_count'
    ]
    list_select_related = ['user']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'name', 'color')
        }),
        ('Analytics', {
            'fields': ('bookmark_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').annotate(
            bookmark_count=Count('bookmarks')
        )


@admin.register(BookmarkAccessLog)
class BookmarkAccessLogAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'bookmark', 'user', 'access_type', 'ip_address',
        'user_agent', 'accessed_at'
    ]
    list_filter = [
        'access_type', 'accessed_at', 'user__email'
    ]
    search_fields = [
        'bookmark__title', 'user__email', 'user__first_name',
        'user__last_name', 'ip_address'
    ]
    readonly_fields = [
        'id', 'accessed_at'
    ]
    list_select_related = ['bookmark', 'user']
    list_per_page = 50
    date_hierarchy = 'accessed_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'bookmark', 'user', 'access_type')
        }),
        ('Access Details', {
            'fields': ('ip_address', 'user_agent', 'referrer')
        }),
        ('Timestamps', {
            'fields': ('accessed_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('bookmark', 'user') 