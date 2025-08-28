from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count

from .models import (
    NotesCategory, NotesTopic, NotesModule, NotesVideo, 
    NotesMCQ, NotesMCQOption, NotesClinicalCase, 
    NotesQBank, NotesFlashCard, NotesStatistics
)



@admin.register(NotesCategory)
class NotesCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_name', 'topics_count', 'modules_count', 'videos_count', 'is_active', 'is_featured']
    list_filter = ['is_active', 'is_featured', 'name']
    search_fields = ['name', 'display_name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'display_name', 'description')
        }),
        ('Statistics', {
            'fields': ('topics_count', 'modules_count', 'videos_count')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class NotesMCQOptionInline(admin.TabularInline):
    model = NotesMCQOption
    extra = 4
    fields = ['option_text', 'is_correct', 'order']


@admin.register(NotesTopic)
class NotesTopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'modules_count', 'videos_count', 'is_active', 'is_featured', 'order']
    list_filter = ['category', 'is_active', 'is_featured']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['category', 'order', 'title']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'title', 'description')
        }),
        ('Statistics', {
            'fields': ('modules_count', 'videos_count')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotesModule)
class NotesModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'module_type', 'duration_minutes', 'views_count', 'likes_count', 'is_active', 'is_premium']
    list_filter = ['module_type', 'is_active', 'is_premium', 'topic__category']
    search_fields = ['title', 'description']
    readonly_fields = ['views_count', 'likes_count', 'created_at', 'updated_at']
    ordering = ['topic', 'order', 'title']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('topic', 'title', 'module_type', 'description')
        }),
        ('Content', {
            'fields': ('content_url', 'duration_minutes')
        }),
        ('Statistics', {
            'fields': ('views_count', 'likes_count')
        }),
        ('Status', {
            'fields': ('is_active', 'is_premium', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotesVideo)
class NotesVideoAdmin(admin.ModelAdmin):
    list_display = ['module_title', 'duration_formatted', 'quality', 'views_count', 'likes_count']
    list_filter = ['quality']
    search_fields = ['module__title']
    readonly_fields = ['views_count', 'likes_count', 'created_at', 'updated_at']
    
    def module_title(self, obj):
        return obj.module.title
    module_title.short_description = 'Module Title'
    
    def duration_formatted(self, obj):
        minutes = obj.duration_seconds // 60
        seconds = obj.duration_seconds % 60
        return f"{minutes}:{seconds:02d}"
    duration_formatted.short_description = 'Duration'
    
    fieldsets = (
        ('Module Information', {
            'fields': ('module',)
        }),
        ('Video Details', {
            'fields': ('video_url', 'thumbnail_url', 'duration_seconds', 'quality')
        }),
        ('Statistics', {
            'fields': ('views_count', 'likes_count')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotesMCQ)
class NotesMCQAdmin(admin.ModelAdmin):
    list_display = ['module_title', 'question_preview', 'attempts_count', 'correct_answers_count', 'success_rate']
    search_fields = ['module__title', 'question_text']
    readonly_fields = ['attempts_count', 'correct_answers_count', 'created_at', 'updated_at']
    inlines = [NotesMCQOptionInline]
    
    def module_title(self, obj):
        return obj.module.title
    module_title.short_description = 'Module Title'
    
    def question_preview(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_preview.short_description = 'Question'
    
    def success_rate(self, obj):
        if obj.attempts_count > 0:
            rate = (obj.correct_answers_count / obj.attempts_count) * 100
            return f"{rate:.1f}%"
        return "0%"
    success_rate.short_description = 'Success Rate'
    
    fieldsets = (
        ('Module Information', {
            'fields': ('module',)
        }),
        ('Question Details', {
            'fields': ('question_text', 'explanation')
        }),
        ('Statistics', {
            'fields': ('attempts_count', 'correct_answers_count')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotesClinicalCase)
class NotesClinicalCaseAdmin(admin.ModelAdmin):
    list_display = ['case_title', 'module_title', 'views_count']
    search_fields = ['case_title', 'module__title']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    
    def module_title(self, obj):
        return obj.module.title
    module_title.short_description = 'Module Title'
    
    fieldsets = (
        ('Module Information', {
            'fields': ('module',)
        }),
        ('Case Details', {
            'fields': ('case_title', 'patient_history', 'clinical_findings', 'diagnosis', 'treatment')
        }),
        ('Statistics', {
            'fields': ('views_count',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotesQBank)
class NotesQBankAdmin(admin.ModelAdmin):
    list_display = ['module_title', 'question_preview', 'difficulty_level', 'attempts_count', 'correct_answers_count', 'success_rate']
    list_filter = ['difficulty_level']
    search_fields = ['module__title', 'question_text']
    readonly_fields = ['attempts_count', 'correct_answers_count', 'created_at', 'updated_at']
    
    def module_title(self, obj):
        return obj.module.title
    module_title.short_description = 'Module Title'
    
    def question_preview(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_preview.short_description = 'Question'
    
    def success_rate(self, obj):
        if obj.attempts_count > 0:
            rate = (obj.correct_answers_count / obj.attempts_count) * 100
            return f"{rate:.1f}%"
        return "0%"
    success_rate.short_description = 'Success Rate'
    
    fieldsets = (
        ('Module Information', {
            'fields': ('module',)
        }),
        ('Question Details', {
            'fields': ('question_text', 'explanation', 'difficulty_level')
        }),
        ('Statistics', {
            'fields': ('attempts_count', 'correct_answers_count')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotesFlashCard)
class NotesFlashCardAdmin(admin.ModelAdmin):
    list_display = ['module_title', 'front_preview', 'back_preview', 'category', 'mastery_level', 'views_count']
    list_filter = ['category', 'mastery_level']
    search_fields = ['module__title', 'front_text', 'back_text']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    
    def module_title(self, obj):
        return obj.module.title
    module_title.short_description = 'Module Title'
    
    def front_preview(self, obj):
        return obj.front_text[:30] + "..." if len(obj.front_text) > 30 else obj.front_text
    front_preview.short_description = 'Front'
    
    def back_preview(self, obj):
        return obj.back_text[:30] + "..." if len(obj.back_text) > 30 else obj.back_text
    back_preview.short_description = 'Back'
    
    fieldsets = (
        ('Module Information', {
            'fields': ('module',)
        }),
        ('Flash Card Details', {
            'fields': ('front_text', 'back_text', 'category')
        }),
        ('Statistics', {
            'fields': ('views_count', 'mastery_level')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotesStatistics)
class NotesStatisticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_views', 'total_modules_accessed', 'total_unique_users', 'video_views', 'mcq_attempts']
    list_filter = ['date']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-date']
    
    fieldsets = (
        ('Date', {
            'fields': ('date',)
        }),
        ('Overall Statistics', {
            'fields': ('total_views', 'total_modules_accessed', 'total_unique_users')
        }),
        ('Category Statistics', {
            'fields': ('video_views', 'mcq_attempts', 'clinical_case_views', 'q_bank_attempts', 'flash_card_views')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Custom admin site configuration
admin.site.site_header = "EdVoyage Notes Administration"
admin.site.site_title = "EdVoyage Notes Admin"
admin.site.index_title = "Welcome to EdVoyage Notes Administration"
