from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import (
    StudyAbroadProgram, StudyAbroadApplication, StudyAbroadExperience,
    StudyAbroadResource, StudyAbroadEvent, StudyAbroadEventRegistration
)

@admin.register(StudyAbroadProgram)
class StudyAbroadProgramAdmin(admin.ModelAdmin):
    """Admin interface for StudyAbroadProgram model"""
    list_display = [
        'name', 'program_type', 'country', 'city', 'institution', 'status',
        'is_active', 'is_featured', 'total_cost', 'duration_days', 'available_spots'
    ]
    list_filter = [
        'program_type', 'status', 'country', 'is_active', 'is_featured',
        'scholarships_available', 'language_proficiency_required', 'visa_required'
    ]
    search_fields = [
        'name', 'description', 'institution', 'field_of_study', 'country', 'city'
    ]
    ordering = ['-created_at']
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'total_cost', 'duration_days', 'available_spots'
    ]
    list_editable = ['is_active', 'is_featured']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'description', 'program_type', 'status')
        }),
        ('Location', {
            'fields': ('country', 'city', 'institution', 'campus_location')
        }),
        ('Academic Details', {
            'fields': ('academic_level', 'field_of_study', 'credits_offered', 'language_requirement')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'application_deadline')
        }),
        ('Financial Information', {
            'fields': ('tuition_cost', 'accommodation_cost', 'other_costs', 'currency',
                      'scholarships_available', 'scholarship_amount')
        }),
        ('Requirements', {
            'fields': ('max_participants', 'min_gpa_requirement', 'language_proficiency_required', 'visa_required')
        }),
        ('Additional Information', {
            'fields': ('highlights', 'requirements', 'application_process', 'contact_email', 'contact_phone')
        }),
        ('Media', {
            'fields': ('program_image', 'brochure_file')
        }),
        ('Calculated Fields', {
            'fields': ('total_cost', 'duration_days', 'available_spots'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def total_cost(self, obj):
        """Display total cost"""
        if obj.total_cost:
            return f"${obj.total_cost:,.2f}"
        return '-'
    total_cost.short_description = 'Total Cost'

    def duration_days(self, obj):
        """Display duration in days"""
        return f"{obj.duration_days} days"
    duration_days.short_description = 'Duration'

    def available_spots(self, obj):
        """Display available spots"""
        if obj.available_spots is not None:
            return obj.available_spots
        return 'Unlimited'
    available_spots.short_description = 'Available Spots'

    actions = ['activate_programs', 'deactivate_programs', 'feature_programs', 'unfeature_programs']

    def activate_programs(self, request, queryset):
        """Activate selected programs"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} program(s) activated successfully.')
    activate_programs.short_description = "Activate selected programs"

    def deactivate_programs(self, request, queryset):
        """Deactivate selected programs"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} program(s) deactivated successfully.')
    deactivate_programs.short_description = "Deactivate selected programs"

    def feature_programs(self, request, queryset):
        """Feature selected programs"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} program(s) featured successfully.')
    feature_programs.short_description = "Feature selected programs"

    def unfeature_programs(self, request, queryset):
        """Unfeature selected programs"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} program(s) unfeatured successfully.')
    unfeature_programs.short_description = "Unfeature selected programs"

@admin.register(StudyAbroadApplication)
class StudyAbroadApplicationAdmin(admin.ModelAdmin):
    """Admin interface for StudyAbroadApplication model"""
    list_display = [
        'user', 'program', 'status', 'current_institution', 'current_major',
        'current_gpa', 'application_date', 'review_date', 'decision_date'
    ]
    list_filter = [
        'status', 'program__program_type', 'program__country', 'financial_aid_needed',
        'scholarship_applied', 'application_date', 'review_date', 'decision_date'
    ]
    search_fields = [
        'user__username', 'user__email', 'program__name', 'current_institution',
        'current_major', 'academic_goals'
    ]
    ordering = ['-application_date']
    readonly_fields = [
        'id', 'application_date', 'review_date', 'decision_date', 'created_at', 'updated_at'
    ]
    list_editable = ['status']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'program', 'status')
        }),
        ('Personal Information', {
            'fields': ('current_institution', 'current_major', 'current_gpa', 'graduation_date')
        }),
        ('Academic Information', {
            'fields': ('academic_standing', 'language_proficiency', 'relevant_coursework', 'academic_goals')
        }),
        ('Documents', {
            'fields': ('personal_statement', 'motivation_letter', 'resume_file', 'transcript_file', 'recommendation_letters')
        }),
        ('Financial Information', {
            'fields': ('financial_aid_needed', 'scholarship_applied', 'additional_funding_sources')
        }),
        ('Review Information', {
            'fields': ('reviewer_notes', 'reviewer')
        }),
        ('Timestamps', {
            'fields': ('application_date', 'review_date', 'decision_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_under_review', 'accept_applications', 'reject_applications', 'waitlist_applications']

    def mark_under_review(self, request, queryset):
        """Mark applications as under review"""
        updated = queryset.update(status='under_review', review_date=timezone.now())
        self.message_user(request, f'{updated} application(s) marked as under review.')
    mark_under_review.short_description = "Mark selected applications as under review"

    def accept_applications(self, request, queryset):
        """Accept selected applications"""
        updated = queryset.update(status='accepted', decision_date=timezone.now())
        self.message_user(request, f'{updated} application(s) accepted.')
    accept_applications.short_description = "Accept selected applications"

    def reject_applications(self, request, queryset):
        """Reject selected applications"""
        updated = queryset.update(status='rejected', decision_date=timezone.now())
        self.message_user(request, f'{updated} application(s) rejected.')
    reject_applications.short_description = "Reject selected applications"

    def waitlist_applications(self, request, queryset):
        """Waitlist selected applications"""
        updated = queryset.update(status='waitlisted', decision_date=timezone.now())
        self.message_user(request, f'{updated} application(s) waitlisted.')
    waitlist_applications.short_description = "Waitlist selected applications"

@admin.register(StudyAbroadExperience)
class StudyAbroadExperienceAdmin(admin.ModelAdmin):
    """Admin interface for StudyAbroadExperience model"""
    list_display = [
        'title', 'user', 'program', 'experience_type', 'rating', 'is_approved',
        'is_featured', 'is_public', 'created_at'
    ]
    list_filter = [
        'experience_type', 'is_approved', 'is_featured', 'is_public', 'rating', 'created_at'
    ]
    search_fields = [
        'title', 'content', 'user__username', 'program__name'
    ]
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_editable = ['is_approved', 'is_featured', 'is_public']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'program', 'title', 'experience_type')
        }),
        ('Content', {
            'fields': ('content', 'rating')
        }),
        ('Media', {
            'fields': ('photos', 'video_url')
        }),
        ('Visibility', {
            'fields': ('is_approved', 'is_featured', 'is_public')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['approve_experiences', 'unapprove_experiences', 'feature_experiences', 'unfeature_experiences']

    def approve_experiences(self, request, queryset):
        """Approve selected experiences"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} experience(s) approved.')
    approve_experiences.short_description = "Approve selected experiences"

    def unapprove_experiences(self, request, queryset):
        """Unapprove selected experiences"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} experience(s) unapproved.')
    unapprove_experiences.short_description = "Unapprove selected experiences"

    def feature_experiences(self, request, queryset):
        """Feature selected experiences"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} experience(s) featured.')
    feature_experiences.short_description = "Feature selected experiences"

    def unfeature_experiences(self, request, queryset):
        """Unfeature selected experiences"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} experience(s) unfeatured.')
    unfeature_experiences.short_description = "Unfeature selected experiences"

@admin.register(StudyAbroadResource)
class StudyAbroadResourceAdmin(admin.ModelAdmin):
    """Admin interface for StudyAbroadResource model"""
    list_display = [
        'title', 'resource_type', 'is_active', 'is_featured', 'requires_authentication',
        'download_count', 'view_count', 'created_at'
    ]
    list_filter = [
        'resource_type', 'is_active', 'is_featured', 'requires_authentication', 'created_at'
    ]
    search_fields = [
        'title', 'description', 'content', 'categories', 'tags'
    ]
    ordering = ['-created_at']
    readonly_fields = ['id', 'download_count', 'view_count', 'created_at', 'updated_at']
    list_editable = ['is_active', 'is_featured', 'requires_authentication']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'title', 'resource_type', 'description', 'content')
        }),
        ('File Attachment', {
            'fields': ('file_attachment',)
        }),
        ('Categories and Tags', {
            'fields': ('categories', 'tags')
        }),
        ('Visibility and Access', {
            'fields': ('is_active', 'is_featured', 'requires_authentication')
        }),
        ('Usage Statistics', {
            'fields': ('download_count', 'view_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['activate_resources', 'deactivate_resources', 'feature_resources', 'unfeature_resources']

    def activate_resources(self, request, queryset):
        """Activate selected resources"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} resource(s) activated.')
    activate_resources.short_description = "Activate selected resources"

    def deactivate_resources(self, request, queryset):
        """Deactivate selected resources"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} resource(s) deactivated.')
    deactivate_resources.short_description = "Deactivate selected resources"

    def feature_resources(self, request, queryset):
        """Feature selected resources"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} resource(s) featured.')
    feature_resources.short_description = "Feature selected resources"

    def unfeature_resources(self, request, queryset):
        """Unfeature selected resources"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} resource(s) unfeatured.')
    unfeature_resources.short_description = "Unfeature selected resources"

@admin.register(StudyAbroadEvent)
class StudyAbroadEventAdmin(admin.ModelAdmin):
    """Admin interface for StudyAbroadEvent model"""
    list_display = [
        'title', 'event_type', 'start_datetime', 'end_datetime', 'location',
        'is_virtual', 'is_active', 'is_featured', 'available_spots'
    ]
    list_filter = [
        'event_type', 'is_active', 'is_featured', 'is_virtual', 'registration_required',
        'start_datetime', 'end_datetime'
    ]
    search_fields = [
        'title', 'description', 'location'
    ]
    ordering = ['start_datetime']
    readonly_fields = ['id', 'created_at', 'updated_at', 'available_spots']
    list_editable = ['is_active', 'is_featured']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'title', 'event_type', 'description')
        }),
        ('Event Details', {
            'fields': ('start_datetime', 'end_datetime', 'location', 'is_virtual', 'virtual_meeting_url')
        }),
        ('Registration', {
            'fields': ('max_attendees', 'registration_required', 'registration_deadline')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Calculated Fields', {
            'fields': ('available_spots',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def available_spots(self, obj):
        """Display available spots"""
        if obj.available_spots is not None:
            return obj.available_spots
        return 'Unlimited'
    available_spots.short_description = 'Available Spots'

    actions = ['activate_events', 'deactivate_events', 'feature_events', 'unfeature_events']

    def activate_events(self, request, queryset):
        """Activate selected events"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} event(s) activated.')
    activate_events.short_description = "Activate selected events"

    def deactivate_events(self, request, queryset):
        """Deactivate selected events"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} event(s) deactivated.')
    deactivate_events.short_description = "Deactivate selected events"

    def feature_events(self, request, queryset):
        """Feature selected events"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} event(s) featured.')
    feature_events.short_description = "Feature selected events"

    def unfeature_events(self, request, queryset):
        """Unfeature selected events"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} event(s) unfeatured.')
    unfeature_events.short_description = "Unfeature selected events"

@admin.register(StudyAbroadEventRegistration)
class StudyAbroadEventRegistrationAdmin(admin.ModelAdmin):
    """Admin interface for StudyAbroadEventRegistration model"""
    list_display = [
        'user', 'event', 'status', 'registration_date', 'attendance_date',
        'dietary_restrictions'
    ]
    list_filter = [
        'status', 'event__event_type', 'registration_date', 'attendance_date'
    ]
    search_fields = [
        'user__username', 'user__email', 'event__title', 'dietary_restrictions',
        'special_accommodations'
    ]
    ordering = ['-registration_date']
    readonly_fields = [
        'id', 'registration_date', 'attendance_date', 'created_at', 'updated_at'
    ]
    list_editable = ['status']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'event', 'status')
        }),
        ('Registration Details', {
            'fields': ('registration_date', 'attendance_date')
        }),
        ('Additional Information', {
            'fields': ('dietary_restrictions', 'special_accommodations', 'questions')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_attended', 'mark_cancelled', 'mark_no_show']

    def mark_attended(self, request, queryset):
        """Mark registrations as attended"""
        updated = queryset.update(status='attended', attendance_date=timezone.now())
        self.message_user(request, f'{updated} registration(s) marked as attended.')
    mark_attended.short_description = "Mark selected registrations as attended"

    def mark_cancelled(self, request, queryset):
        """Mark registrations as cancelled"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} registration(s) marked as cancelled.')
    mark_cancelled.short_description = "Mark selected registrations as cancelled"

    def mark_no_show(self, request, queryset):
        """Mark registrations as no show"""
        updated = queryset.update(status='no_show')
        self.message_user(request, f'{updated} registration(s) marked as no show.')
    mark_no_show.short_description = "Mark selected registrations as no show"
