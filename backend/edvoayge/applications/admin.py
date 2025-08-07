"""
Admin configuration for applications app.
Provides Django admin interface for application management.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import (
    Application, ApplicationDocument, ApplicationStatus, ApplicationInterview,
    ApplicationFee, ApplicationCommunication
)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Admin for Application model."""
    
    list_display = [
        'application_number', 'user_username', 'university_name', 'program_name',
        'status', 'priority', 'is_complete', 'is_verified', 'days_since_submission',
        'created_at'
    ]
    list_filter = [
        'status', 'priority', 'is_complete', 'is_verified', 'intended_start_semester',
        'academic_year', 'created_at', 'submitted_at'
    ]
    search_fields = [
        'application_number', 'user__username', 'user__email', 'university__name',
        'program__name', 'personal_statement'
    ]
    readonly_fields = [
        'application_number', 'days_since_submission', 'is_overdue',
        'created_at', 'updated_at'
    ]
    fieldsets = (
        ('Application Information', {
            'fields': ('application_number', 'user', 'university', 'program')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'is_complete', 'is_verified')
        }),
        ('Academic Information', {
            'fields': ('intended_start_date', 'intended_start_semester', 'academic_year')
        }),
        ('Personal Statement', {
            'fields': ('personal_statement', 'research_proposal'),
            'classes': ('collapse',)
        }),
        ('References & Additional Info', {
            'fields': ('references', 'additional_info', 'notes'),
            'classes': ('collapse',)
        }),
        ('Timeline', {
            'fields': ('submitted_at', 'reviewed_at', 'decision_date')
        }),
        ('Metadata', {
            'fields': ('days_since_submission', 'is_overdue', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_username(self, obj):
        """Display username with link."""
        if obj.user:
            url = reverse('admin:auth_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return '-'
    user_username.short_description = 'Username'
    user_username.admin_order_field = 'user__username'
    
    def university_name(self, obj):
        """Display university name with link."""
        if obj.university:
            url = reverse('admin:universities_university_change', args=[obj.university.id])
            return format_html('<a href="{}">{}</a>', url, obj.university.name)
        return '-'
    university_name.short_description = 'University'
    university_name.admin_order_field = 'university__name'
    
    def program_name(self, obj):
        """Display program name."""
        return obj.program.name if obj.program else '-'
    program_name.short_description = 'Program'
    program_name.admin_order_field = 'program__name'
    
    def days_since_submission(self, obj):
        """Display days since submission."""
        return obj.days_since_submission or '-'
    days_since_submission.short_description = 'Days Since Submission'
    
    list_per_page = 25
    ordering = ['-created_at']
    
    actions = ['mark_complete', 'mark_verified', 'update_status']
    
    def mark_complete(self, request, queryset):
        """Mark selected applications as complete."""
        updated = queryset.update(is_complete=True)
        self.message_user(request, f'{updated} applications marked as complete.')
    mark_complete.short_description = "Mark applications as complete"
    
    def mark_verified(self, request, queryset):
        """Mark selected applications as verified."""
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} applications marked as verified.')
    mark_verified.short_description = "Mark applications as verified"
    
    def update_status(self, request, queryset):
        """Update status of selected applications."""
        # This would typically be done through a custom admin action
        self.message_user(request, 'Status update action would be implemented here.')
    update_status.short_description = "Update application status"


@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    """Admin for ApplicationDocument model."""
    
    list_display = [
        'application_number', 'document_type', 'document_name', 'status',
        'is_required', 'is_verified', 'is_expired', 'uploaded_at'
    ]
    list_filter = [
        'document_type', 'status', 'is_required', 'is_verified', 'uploaded_at'
    ]
    search_fields = [
        'document_name', 'application__application_number', 'document_type'
    ]
    readonly_fields = [
        'file_size', 'file_type', 'is_expired', 'uploaded_at', 'updated_at'
    ]
    fieldsets = (
        ('Application Information', {
            'fields': ('application',)
        }),
        ('Document Information', {
            'fields': ('document_type', 'document_name', 'file')
        }),
        ('Status', {
            'fields': ('status', 'is_required', 'is_verified')
        }),
        ('Verification', {
            'fields': ('verified_by', 'verified_at', 'verification_notes'),
            'classes': ('collapse',)
        }),
        ('Expiry', {
            'fields': ('expiry_date', 'is_expired')
        }),
        ('File Information', {
            'fields': ('file_size', 'file_type'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('uploaded_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def application_number(self, obj):
        """Display application number with link."""
        if obj.application:
            url = reverse('admin:applications_application_change', args=[obj.application.id])
            return format_html('<a href="{}">{}</a>', url, obj.application.application_number)
        return '-'
    application_number.short_description = 'Application Number'
    application_number.admin_order_field = 'application__application_number'
    
    def is_expired(self, obj):
        """Display expiry status."""
        return obj.is_expired
    is_expired.boolean = True
    is_expired.short_description = 'Expired'
    
    list_per_page = 25
    ordering = ['-uploaded_at']
    
    actions = ['verify_documents', 'reject_documents']
    
    def verify_documents(self, request, queryset):
        """Verify selected documents."""
        updated = queryset.update(
            is_verified=True,
            verified_by=request.user,
            verified_at=timezone.now()
        )
        self.message_user(request, f'{updated} documents verified successfully.')
    verify_documents.short_description = "Verify selected documents"
    
    def reject_documents(self, request, queryset):
        """Reject selected documents."""
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} documents rejected successfully.')
    reject_documents.short_description = "Reject selected documents"


@admin.register(ApplicationStatus)
class ApplicationStatusAdmin(admin.ModelAdmin):
    """Admin for ApplicationStatus model."""
    
    list_display = [
        'application_number', 'status', 'changed_by_username', 'changed_at'
    ]
    list_filter = [
        'status', 'changed_at'
    ]
    search_fields = [
        'application__application_number', 'status', 'description'
    ]
    readonly_fields = ['changed_at']
    fieldsets = (
        ('Application Information', {
            'fields': ('application',)
        }),
        ('Status Information', {
            'fields': ('status', 'description', 'notes')
        }),
        ('User Information', {
            'fields': ('changed_by',)
        }),
        ('Timeline', {
            'fields': ('changed_at',)
        }),
    )
    
    def application_number(self, obj):
        """Display application number with link."""
        if obj.application:
            url = reverse('admin:applications_application_change', args=[obj.application.id])
            return format_html('<a href="{}">{}</a>', url, obj.application.application_number)
        return '-'
    application_number.short_description = 'Application Number'
    application_number.admin_order_field = 'application__application_number'
    
    def changed_by_username(self, obj):
        """Display changed by username."""
        return obj.changed_by.username if obj.changed_by else '-'
    changed_by_username.short_description = 'Changed By'
    changed_by_username.admin_order_field = 'changed_by__username'
    
    list_per_page = 25
    ordering = ['-changed_at']


@admin.register(ApplicationInterview)
class ApplicationInterviewAdmin(admin.ModelAdmin):
    """Admin for ApplicationInterview model."""
    
    list_display = [
        'application_number', 'interview_type', 'status', 'scheduled_date',
        'interviewer_name', 'duration_minutes', 'score'
    ]
    list_filter = [
        'interview_type', 'status', 'scheduled_date', 'created_at'
    ]
    search_fields = [
        'application__application_number', 'interviewer_name', 'location'
    ]
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Application Information', {
            'fields': ('application',)
        }),
        ('Interview Information', {
            'fields': ('interview_type', 'status', 'scheduled_date', 'duration_minutes')
        }),
        ('Interviewer Information', {
            'fields': ('interviewer_name', 'interviewer_email', 'interviewer_phone')
        }),
        ('Location & Platform', {
            'fields': ('location', 'platform', 'meeting_link'),
            'classes': ('collapse',)
        }),
        ('Notes & Feedback', {
            'fields': ('preparation_notes', 'interview_notes', 'feedback'),
            'classes': ('collapse',)
        }),
        ('Results', {
            'fields': ('score', 'recommendation', 'completed_at')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def application_number(self, obj):
        """Display application number with link."""
        if obj.application:
            url = reverse('admin:applications_application_change', args=[obj.application.id])
            return format_html('<a href="{}">{}</a>', url, obj.application.application_number)
        return '-'
    application_number.short_description = 'Application Number'
    application_number.admin_order_field = 'application__application_number'
    
    list_per_page = 25
    ordering = ['-scheduled_date']
    
    actions = ['complete_interviews', 'cancel_interviews']
    
    def complete_interviews(self, request, queryset):
        """Mark selected interviews as completed."""
        updated = queryset.update(
            status='completed',
            completed_at=timezone.now()
        )
        self.message_user(request, f'{updated} interviews marked as completed.')
    complete_interviews.short_description = "Mark interviews as completed"
    
    def cancel_interviews(self, request, queryset):
        """Cancel selected interviews."""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} interviews cancelled successfully.')
    cancel_interviews.short_description = "Cancel selected interviews"


@admin.register(ApplicationFee)
class ApplicationFeeAdmin(admin.ModelAdmin):
    """Admin for ApplicationFee model."""
    
    list_display = [
        'application_number', 'fee_type', 'amount', 'currency', 'payment_status',
        'due_date', 'is_overdue', 'created_at'
    ]
    list_filter = [
        'fee_type', 'payment_status', 'currency', 'due_date', 'created_at'
    ]
    search_fields = [
        'application__application_number', 'fee_type', 'transaction_id'
    ]
    readonly_fields = ['is_overdue', 'created_at', 'updated_at']
    fieldsets = (
        ('Application Information', {
            'fields': ('application',)
        }),
        ('Fee Information', {
            'fields': ('fee_type', 'amount', 'currency', 'due_date')
        }),
        ('Payment Information', {
            'fields': ('payment_status', 'payment_method', 'transaction_id', 'paid_at')
        }),
        ('Notes', {
            'fields': ('description', 'notes'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_overdue',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def application_number(self, obj):
        """Display application number with link."""
        if obj.application:
            url = reverse('admin:applications_application_change', args=[obj.application.id])
            return format_html('<a href="{}">{}</a>', url, obj.application.application_number)
        return '-'
    application_number.short_description = 'Application Number'
    application_number.admin_order_field = 'application__application_number'
    
    def is_overdue(self, obj):
        """Display overdue status."""
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'
    
    list_per_page = 25
    ordering = ['-created_at']
    
    actions = ['mark_paid', 'mark_failed']
    
    def mark_paid(self, request, queryset):
        """Mark selected fees as paid."""
        updated = queryset.update(
            payment_status='paid',
            paid_at=timezone.now()
        )
        self.message_user(request, f'{updated} fees marked as paid.')
    mark_paid.short_description = "Mark fees as paid"
    
    def mark_failed(self, request, queryset):
        """Mark selected fees as failed."""
        updated = queryset.update(payment_status='failed')
        self.message_user(request, f'{updated} fees marked as failed.')
    mark_failed.short_description = "Mark fees as failed"


@admin.register(ApplicationCommunication)
class ApplicationCommunicationAdmin(admin.ModelAdmin):
    """Admin for ApplicationCommunication model."""
    
    list_display = [
        'application_number', 'communication_type', 'direction', 'subject',
        'is_sent', 'is_delivered', 'is_read', 'created_at'
    ]
    list_filter = [
        'communication_type', 'direction', 'is_sent', 'is_delivered', 'is_read',
        'created_at'
    ]
    search_fields = [
        'application__application_number', 'subject', 'message', 'from_email', 'to_email'
    ]
    readonly_fields = ['created_at']
    fieldsets = (
        ('Application Information', {
            'fields': ('application',)
        }),
        ('Communication Information', {
            'fields': ('communication_type', 'direction', 'subject', 'message')
        }),
        ('Recipients', {
            'fields': ('from_email', 'to_email', 'from_phone', 'to_phone'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_sent', 'is_delivered', 'is_read')
        }),
        ('Timeline', {
            'fields': ('sent_at', 'delivered_at', 'read_at'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def application_number(self, obj):
        """Display application number with link."""
        if obj.application:
            url = reverse('admin:applications_application_change', args=[obj.application.id])
            return format_html('<a href="{}">{}</a>', url, obj.application.application_number)
        return '-'
    application_number.short_description = 'Application Number'
    application_number.admin_order_field = 'application__application_number'
    
    list_per_page = 25
    ordering = ['-created_at']
    
    actions = ['mark_sent', 'mark_delivered', 'mark_read']
    
    def mark_sent(self, request, queryset):
        """Mark selected communications as sent."""
        updated = queryset.update(
            is_sent=True,
            sent_at=timezone.now()
        )
        self.message_user(request, f'{updated} communications marked as sent.')
    mark_sent.short_description = "Mark communications as sent"
    
    def mark_delivered(self, request, queryset):
        """Mark selected communications as delivered."""
        updated = queryset.update(
            is_delivered=True,
            delivered_at=timezone.now()
        )
        self.message_user(request, f'{updated} communications marked as delivered.')
    mark_delivered.short_description = "Mark communications as delivered"
    
    def mark_read(self, request, queryset):
        """Mark selected communications as read."""
        updated = queryset.update(
            is_read=True,
            read_at=timezone.now()
        )
        self.message_user(request, f'{updated} communications marked as read.')
    mark_read.short_description = "Mark communications as read"
