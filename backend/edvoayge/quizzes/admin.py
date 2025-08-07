from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Quiz, QuizCategory, Question, Option, QuizAttempt, 
    QuizResult, QuizAnalytics, QuizShare, QuizTimer
)

@admin.register(QuizCategory)
class QuizCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'quiz_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'quiz_count')
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
    
    def quiz_count(self, obj):
        return obj.quizzes.count()
    quiz_count.short_description = 'Quizzes'

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'category', 'difficulty', 'status', 'is_public', 'is_featured', 'total_attempts', 'average_score', 'created_at')
    list_filter = ('status', 'difficulty', 'is_public', 'is_featured', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'creator__username', 'category__name')
    readonly_fields = ('creator', 'total_attempts', 'average_score', 'completion_rate', 'created_at', 'updated_at', 'published_at', 'question_count')
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'creator')
        }),
        ('Quiz Settings', {
            'fields': ('time_limit', 'passing_score', 'max_attempts', 'difficulty', 'status', 'is_public', 'is_featured')
        }),
        ('Analytics', {
            'fields': ('total_attempts', 'average_score', 'completion_rate', 'question_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'creator').prefetch_related('questions')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text_preview', 'quiz', 'question_type', 'points', 'order', 'is_active', 'created_at')
    list_filter = ('question_type', 'is_active', 'quiz', 'created_at', 'updated_at')
    search_fields = ('question_text', 'quiz__title')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25
    
    fieldsets = (
        ('Question Information', {
            'fields': ('quiz', 'question_text', 'question_type', 'points', 'order', 'explanation', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def question_text_preview(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    question_text_preview.short_description = 'Question'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('quiz').prefetch_related('options')

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('option_text_preview', 'question', 'is_correct', 'order', 'created_at')
    list_filter = ('is_correct', 'question__quiz', 'created_at')
    search_fields = ('option_text', 'question__question_text')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Option Information', {
            'fields': ('question', 'option_text', 'is_correct', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def option_text_preview(self, obj):
        return obj.option_text[:50] + '...' if len(obj.option_text) > 50 else obj.option_text
    option_text_preview.short_description = 'Option'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('question')

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'user', 'status', 'percentage', 'passed', 'time_taken', 'started_at')
    list_filter = ('status', 'passed', 'quiz', 'started_at', 'completed_at')
    search_fields = ('quiz__title', 'user__username', 'user__email')
    readonly_fields = ('id', 'user', 'score', 'percentage', 'passed', 'started_at', 'completed_at', 'time_taken', 'questions_attempted', 'questions_correct', 'created_at', 'updated_at')
    list_per_page = 25
    
    fieldsets = (
        ('Attempt Information', {
            'fields': ('id', 'quiz', 'user', 'status')
        }),
        ('Results', {
            'fields': ('score', 'percentage', 'passed', 'questions_attempted', 'questions_correct')
        }),
        ('Time Tracking', {
            'fields': ('started_at', 'completed_at', 'time_taken')
        }),
        ('User Answers', {
            'fields': ('answers',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('quiz', 'user')

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question_preview', 'user_answer_preview', 'is_correct', 'points_earned', 'created_at')
    list_filter = ('is_correct', 'attempt__quiz', 'created_at')
    search_fields = ('attempt__quiz__title', 'question__question_text', 'user_answer')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Result Information', {
            'fields': ('attempt', 'question', 'user_answer', 'is_correct', 'points_earned', 'time_taken', 'feedback', 'explanation_shown')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def question_preview(self, obj):
        return obj.question.question_text[:50] + '...' if len(obj.question.question_text) > 50 else obj.question.question_text
    question_preview.short_description = 'Question'
    
    def user_answer_preview(self, obj):
        return obj.user_answer[:50] + '...' if len(obj.user_answer) > 50 else obj.user_answer
    user_answer_preview.short_description = 'User Answer'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('attempt', 'question')

@admin.register(QuizAnalytics)
class QuizAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'action_type', 'ip_address', 'user_agent_preview', 'created_at')
    list_filter = ('action_type', 'quiz', 'created_at')
    search_fields = ('quiz__title', 'user__username', 'ip_address')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Analytics Information', {
            'fields': ('quiz', 'user', 'action_type', 'ip_address', 'user_agent', 'referrer', 'session_id')
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
        return super().get_queryset(request).select_related('quiz', 'user')

@admin.register(QuizShare)
class QuizShareAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'shared_by', 'shared_with', 'share_type', 'is_viewed', 'created_at')
    list_filter = ('share_type', 'is_viewed', 'quiz', 'created_at')
    search_fields = ('quiz__title', 'shared_by__username', 'shared_with__username')
    readonly_fields = ('created_at', 'viewed_at')
    list_per_page = 25
    
    fieldsets = (
        ('Share Information', {
            'fields': ('quiz', 'shared_by', 'shared_with', 'share_type', 'message', 'share_url')
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
        return super().get_queryset(request).select_related('quiz', 'shared_by', 'shared_with')

@admin.register(QuizTimer)
class QuizTimerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'time_limit', 'time_remaining', 'is_paused', 'is_expired', 'created_at')
    list_filter = ('is_paused', 'attempt__quiz', 'created_at')
    search_fields = ('attempt__quiz__title', 'attempt__user__username')
    readonly_fields = ('created_at', 'updated_at', 'is_expired')
    list_per_page = 25
    
    fieldsets = (
        ('Timer Information', {
            'fields': ('attempt', 'time_limit', 'time_remaining', 'is_paused', 'is_expired')
        }),
        ('Pause Tracking', {
            'fields': ('paused_at', 'resumed_at', 'total_pause_time')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('attempt')

# Custom admin actions
@admin.action(description="Publish selected quizzes")
def publish_quizzes(modeladmin, request, queryset):
    updated = queryset.update(status='published')
    modeladmin.message_user(request, f'{updated} quizzes were successfully published.')

@admin.action(description="Archive selected quizzes")
def archive_quizzes(modeladmin, request, queryset):
    updated = queryset.update(status='archived')
    modeladmin.message_user(request, f'{updated} quizzes were successfully archived.')

@admin.action(description="Feature selected quizzes")
def feature_quizzes(modeladmin, request, queryset):
    updated = queryset.update(is_featured=True)
    modeladmin.message_user(request, f'{updated} quizzes were successfully featured.')

@admin.action(description="Unfeature selected quizzes")
def unfeature_quizzes(modeladmin, request, queryset):
    updated = queryset.update(is_featured=False)
    modeladmin.message_user(request, f'{updated} quizzes were successfully unfeatured.')

@admin.action(description="Make selected quizzes public")
def make_public(modeladmin, request, queryset):
    updated = queryset.update(is_public=True)
    modeladmin.message_user(request, f'{updated} quizzes were successfully made public.')

@admin.action(description="Make selected quizzes private")
def make_private(modeladmin, request, queryset):
    updated = queryset.update(is_public=False)
    modeladmin.message_user(request, f'{updated} quizzes were successfully made private.')

# Add actions to QuizAdmin
QuizAdmin.actions = [publish_quizzes, archive_quizzes, feature_quizzes, unfeature_quizzes, make_public, make_private]
