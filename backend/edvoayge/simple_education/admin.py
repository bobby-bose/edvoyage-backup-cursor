from django.contrib import admin
from .models import SimpleEducation, SimpleWork, SimpleSocial

@admin.register(SimpleEducation)
class SimpleEducationAdmin(admin.ModelAdmin):
    """Admin for SimpleEducation model"""
    list_display = ['user', 'higher_start_year', 'higher_end_year', 'higher_gpa', 
                   'lower_start_year', 'lower_end_year', 'lower_gpa', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Higher Education', {
            'fields': ('higher_start_year', 'higher_end_year', 'higher_gpa')
        }),
        ('Lower Education', {
            'fields': ('lower_start_year', 'lower_end_year', 'lower_gpa')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SimpleWork)
class SimpleWorkAdmin(admin.ModelAdmin):
    """Admin for SimpleWork model"""
    list_display = ['user', 'position', 'start_year', 'end_year', 'pursuing', 'created_at']
    list_filter = ['pursuing', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'position']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Work Details', {
            'fields': ('position', 'start_year', 'end_year', 'pursuing')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SimpleSocial)
class SimpleSocialAdmin(admin.ModelAdmin):
    """Admin for SimpleSocial model"""
    list_display = ['user', 'facebook_link', 'linkedin_link', 'twitter_link', 'instagram_link', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Social Links', {
            'fields': ('facebook_link', 'linkedin_link', 'twitter_link', 'instagram_link')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
