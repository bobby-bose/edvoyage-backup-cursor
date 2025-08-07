"""
Course admin configuration for Django admin interface.
Provides admin interface for course management.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Course, Subject, CourseSubject, FeeStructure, 
    CourseRequirement, CourseApplication, CourseRating
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin interface for Course model."""
    
    list_display = [
        'id', 'name', 'code', 'university', 'level', 'duration', 
        'tuition_fee', 'currency', 'status', 'is_featured', 'is_popular',
        'average_rating_display', 'total_applications_display', 'created_at'
    ]
    list_filter = [
        'status', 'level', 'duration', 'is_featured', 'is_popular',
        'university', 'created_at'
    ]
    search_fields = ['name', 'code', 'description', 'university__name']
    readonly_fields = ['created_at', 'updated_at', 'average_rating', 'total_applications']
    list_editable = ['status', 'is_featured', 'is_popular']
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description', 'short_description')
        }),
        ('University & Level', {
            'fields': ('university', 'level', 'duration', 'credits')
        }),
        ('Financial Information', {
            'fields': ('tuition_fee', 'currency')
        }),
        ('Requirements', {
            'fields': ('minimum_gpa', 'language_requirements')
        }),
        ('Status & Visibility', {
            'fields': ('status', 'is_featured', 'is_popular')
        }),
        ('Media', {
            'fields': ('image', 'brochure')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def average_rating_display(self, obj):
        """Display average rating with stars."""
        rating = obj.average_rating
        if rating > 0:
            stars = '★' * int(rating) + '☆' * (5 - int(rating))
            return format_html('<span style="color: gold;">{}</span> ({:.1f})', stars, rating)
        return 'No ratings'
    average_rating_display.short_description = 'Average Rating'
    
    def total_applications_display(self, obj):
        """Display total applications with link."""
        count = obj.total_applications
        if count > 0:
            url = reverse('admin:courses_courseapplication_changelist') + f'?course__id__exact={obj.id}'
            return format_html('<a href="{}">{} applications</a>', url, count)
        return '0 applications'
    total_applications_display.short_description = 'Applications'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin interface for Subject model."""
    
    list_display = ['id', 'name', 'code', 'credits', 'is_core', 'created_at']
    list_filter = ['is_core', 'credits', 'created_at']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_core', 'credits']
    list_per_page = 25


@admin.register(CourseSubject)
class CourseSubjectAdmin(admin.ModelAdmin):
    """Admin interface for CourseSubject model."""
    
    list_display = ['id', 'course', 'subject', 'semester', 'is_optional']
    list_filter = ['semester', 'is_optional', 'course__university']
    search_fields = ['course__name', 'subject__name']
    list_editable = ['semester', 'is_optional']
    list_per_page = 25


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    """Admin interface for FeeStructure model."""
    
    list_display = [
        'id', 'course', 'tuition_fee', 'currency', 'total_fees_display',
        'created_at'
    ]
    list_filter = ['currency', 'created_at']
    search_fields = ['course__name']
    readonly_fields = ['created_at', 'updated_at', 'total_fees']
    list_per_page = 25
    
    fieldsets = (
        ('Course', {
            'fields': ('course',)
        }),
        ('Tuition Fees', {
            'fields': ('tuition_fee', 'tuition_fee_per_semester')
        }),
        ('Additional Costs', {
            'fields': (
                'accommodation_fee', 'meal_plan_fee', 'transportation_fee',
                'health_insurance_fee', 'books_materials_fee', 'other_fees'
            )
        }),
        ('Payment Information', {
            'fields': ('currency', 'payment_terms')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def total_fees_display(self, obj):
        """Display total fees."""
        return f"{obj.total_fees} {obj.currency}"
    total_fees_display.short_description = 'Total Fees'


@admin.register(CourseRequirement)
class CourseRequirementAdmin(admin.ModelAdmin):
    """Admin interface for CourseRequirement model."""
    
    list_display = [
        'id', 'course', 'requirement_type', 'title', 'is_mandatory',
        'order', 'created_at'
    ]
    list_filter = ['requirement_type', 'is_mandatory', 'created_at']
    search_fields = ['title', 'description', 'course__name']
    list_editable = ['is_mandatory', 'order']
    list_per_page = 25
    
    fieldsets = (
        ('Course', {
            'fields': ('course',)
        }),
        ('Requirement Details', {
            'fields': ('requirement_type', 'title', 'description')
        }),
        ('Settings', {
            'fields': ('is_mandatory', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CourseApplication)
class CourseApplicationAdmin(admin.ModelAdmin):
    """Admin interface for CourseApplication model."""
    
    list_display = [
        'id', 'user', 'course', 'university_display', 'status',
        'expected_start_date', 'created_at'
    ]
    list_filter = [
        'status', 'created_at', 'course__university', 'course__level'
    ]
    search_fields = [
        'user__username', 'user__email', 'course__name', 'course__university__name'
    ]
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    list_per_page = 25
    
    fieldsets = (
        ('Application Details', {
            'fields': ('user', 'course', 'status')
        }),
        ('Personal Information', {
            'fields': ('personal_statement', 'expected_start_date')
        }),
        ('Documents', {
            'fields': ('documents',)
        }),
        ('Review Information', {
            'fields': ('review_notes', 'reviewed_by', 'reviewed_at')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def university_display(self, obj):
        """Display university name."""
        return obj.course.university.name if obj.course else '-'
    university_display.short_description = 'University'
    
    def get_queryset(self, request):
        """Optimize queryset with related fields."""
        return super().get_queryset(request).select_related(
            'user', 'course', 'course__university', 'reviewed_by'
        )


@admin.register(CourseRating)
class CourseRatingAdmin(admin.ModelAdmin):
    """Admin interface for CourseRating model."""
    
    list_display = [
        'id', 'user', 'course', 'rating_display', 'is_verified',
        'created_at'
    ]
    list_filter = ['rating', 'is_verified', 'created_at']
    search_fields = [
        'user__username', 'user__email', 'course__name', 'review'
    ]
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_verified']
    list_per_page = 25
    
    fieldsets = (
        ('Rating Details', {
            'fields': ('user', 'course', 'rating', 'review')
        }),
        ('Verification', {
            'fields': ('is_verified',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def rating_display(self, obj):
        """Display rating with stars."""
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: gold;">{}</span>', stars)
    rating_display.short_description = 'Rating'
    
    def get_queryset(self, request):
        """Optimize queryset with related fields."""
        return super().get_queryset(request).select_related('user', 'course')
