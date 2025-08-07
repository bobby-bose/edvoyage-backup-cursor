"""
Application models for EdVoyage application.
Handles university applications, documents, and application tracking.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Application(models.Model):
    """
    University application model.
    """
    APPLICATION_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('interview_completed', 'Interview Completed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('waitlisted', 'Waitlisted'),
        ('withdrawn', 'Withdrawn'),
        ('deferred', 'Deferred'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    university = models.ForeignKey('universities.University', on_delete=models.CASCADE, related_name='applications')
    program = models.ForeignKey('universities.UniversityProgram', on_delete=models.CASCADE, related_name='applications')
    
    # Application Details
    application_number = models.CharField(max_length=50, unique=True, blank=True, verbose_name="Application Number")
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default='draft', verbose_name="Status")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="Priority")
    
    # Academic Information
    intended_start_date = models.DateField(verbose_name="Intended Start Date")
    intended_start_semester = models.CharField(max_length=20, verbose_name="Intended Start Semester")
    academic_year = models.CharField(max_length=10, verbose_name="Academic Year")
    
    # Personal Statement
    personal_statement = models.TextField(blank=True, verbose_name="Personal Statement")
    research_proposal = models.TextField(blank=True, verbose_name="Research Proposal")
    
    # References
    references = models.JSONField(default=list, blank=True, verbose_name="References")
    
    # Additional Information
    additional_info = models.JSONField(default=dict, blank=True, verbose_name="Additional Information")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    # Timeline
    submitted_at = models.DateTimeField(null=True, blank=True, verbose_name="Submitted At")
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name="Reviewed At")
    decision_date = models.DateTimeField(null=True, blank=True, verbose_name="Decision Date")
    
    # Status Tracking
    is_complete = models.BooleanField(default=False, verbose_name="Application Complete")
    is_verified = models.BooleanField(default=False, verbose_name="Application Verified")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.university.name} ({self.application_number})"
    
    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Updating application: {self.application_number}") if hasattr(self, '_meta') else None
        else:
            print(f"Creating new application: {self.application_number}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)
    
    @property
    def days_since_submission(self):
        """Calculate days since submission."""
        if self.submitted_at:
            return (timezone.now() - self.submitted_at).days
        return None
    
    @property
    def is_overdue(self):
        """Check if application is overdue."""
        if self.submitted_at and self.status in ['submitted', 'under_review']:
            return self.days_since_submission > 30
        return False


class ApplicationDocument(models.Model):
    """
    Application document model.
    """
    DOCUMENT_TYPE_CHOICES = [
        ('transcript', 'Academic Transcript'),
        ('diploma', 'Diploma/Certificate'),
        ('passport', 'Passport'),
        ('visa', 'Visa'),
        ('ielts', 'IELTS Certificate'),
        ('toefl', 'TOEFL Certificate'),
        ('gre', 'GRE Score'),
        ('gmat', 'GMAT Score'),
        ('cv', 'CV/Resume'),
        ('personal_statement', 'Personal Statement'),
        ('research_proposal', 'Research Proposal'),
        ('reference_letter', 'Reference Letter'),
        ('financial_statement', 'Financial Statement'),
        ('medical_certificate', 'Medical Certificate'),
        ('other', 'Other'),
    ]
    
    DOCUMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('uploaded', 'Uploaded'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, verbose_name="Document Type")
    document_name = models.CharField(max_length=255, verbose_name="Document Name")
    
    # File Information
    file = models.FileField(upload_to='applications/documents/', verbose_name="Document File")
    file_size = models.PositiveIntegerField(null=True, blank=True, verbose_name="File Size (bytes)")
    file_type = models.CharField(max_length=50, blank=True, verbose_name="File Type")
    
    # Status
    status = models.CharField(max_length=20, choices=DOCUMENT_STATUS_CHOICES, default='pending', verbose_name="Status")
    is_required = models.BooleanField(default=True, verbose_name="Required Document")
    is_verified = models.BooleanField(default=False, verbose_name="Document Verified")
    
    # Verification
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_documents', verbose_name="Verified By")
    verified_at = models.DateTimeField(null=True, blank=True, verbose_name="Verified At")
    verification_notes = models.TextField(blank=True, verbose_name="Verification Notes")
    
    # Expiry
    expiry_date = models.DateField(null=True, blank=True, verbose_name="Expiry Date")
    
    # Metadata
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Uploaded At")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Application Document"
        verbose_name_plural = "Application Documents"
        ordering = ['application', 'document_type']
    
    def __str__(self):
        return f"{self.application.application_number} - {self.document_type}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Updating document: {self.document_name}") if hasattr(self, '_meta') else None
        else:
            print(f"Creating new document: {self.document_name}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        """Check if document is expired."""
        if self.expiry_date:
            return timezone.now().date() > self.expiry_date
        return False


class ApplicationStatus(models.Model):
    """
    Application status tracking model.
    """
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20, choices=Application.APPLICATION_STATUS_CHOICES, verbose_name="Status")
    
    # Status Details
    description = models.TextField(blank=True, verbose_name="Description")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    # User Information
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='status_changes', verbose_name="Changed By")
    
    # Timeline
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name="Changed At")
    
    class Meta:
        verbose_name = "Application Status"
        verbose_name_plural = "Application Statuses"
        ordering = ['-changed_at']
    
    def __str__(self):
        return f"{self.application.application_number} - {self.status} ({self.changed_at})"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            print(f"Status change: {self.application.application_number} -> {self.status}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)


class ApplicationInterview(models.Model):
    """
    Application interview model.
    """
    INTERVIEW_TYPE_CHOICES = [
        ('phone', 'Phone Interview'),
        ('video', 'Video Interview'),
        ('in_person', 'In-Person Interview'),
        ('panel', 'Panel Interview'),
        ('technical', 'Technical Interview'),
    ]
    
    INTERVIEW_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPE_CHOICES, verbose_name="Interview Type")
    status = models.CharField(max_length=20, choices=INTERVIEW_STATUS_CHOICES, default='scheduled', verbose_name="Status")
    
    # Schedule
    scheduled_date = models.DateTimeField(verbose_name="Scheduled Date")
    duration_minutes = models.PositiveIntegerField(default=60, verbose_name="Duration (minutes)")
    
    # Participants
    interviewer_name = models.CharField(max_length=255, blank=True, verbose_name="Interviewer Name")
    interviewer_email = models.EmailField(blank=True, verbose_name="Interviewer Email")
    interviewer_phone = models.CharField(max_length=20, blank=True, verbose_name="Interviewer Phone")
    
    # Location/Platform
    location = models.CharField(max_length=255, blank=True, verbose_name="Location")
    platform = models.CharField(max_length=100, blank=True, verbose_name="Platform (for video interviews)")
    meeting_link = models.URLField(blank=True, verbose_name="Meeting Link")
    
    # Notes
    preparation_notes = models.TextField(blank=True, verbose_name="Preparation Notes")
    interview_notes = models.TextField(blank=True, verbose_name="Interview Notes")
    feedback = models.TextField(blank=True, verbose_name="Interview Feedback")
    
    # Results
    score = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Interview Score")
    recommendation = models.CharField(max_length=22, choices=[
        ('strongly_recommend', 'Strongly Recommend'),
        ('recommend', 'Recommend'),
        ('neutral', 'Neutral'),
        ('not_recommend', 'Do Not Recommend'),
        ('strongly_not_recommend', 'Strongly Do Not Recommend'),
    ], blank=True, verbose_name="Recommendation")
    
    # Timeline
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Completed At")
    
    class Meta:
        verbose_name = "Application Interview"
        verbose_name_plural = "Application Interviews"
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.application.application_number} - {self.interview_type} ({self.scheduled_date})"
    
    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Updating interview: {self.application.application_number}") if hasattr(self, '_meta') else None
        else:
            print(f"Creating new interview: {self.application.application_number}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)


class ApplicationFee(models.Model):
    """
    Application fee model.
    """
    FEE_TYPE_CHOICES = [
        ('application_fee', 'Application Fee'),
        ('processing_fee', 'Processing Fee'),
        ('late_fee', 'Late Fee'),
        ('document_fee', 'Document Processing Fee'),
        ('interview_fee', 'Interview Fee'),
        ('other', 'Other'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='fees')
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES, verbose_name="Fee Type")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    currency = models.CharField(max_length=3, default='USD', verbose_name="Currency")
    
    # Payment Information
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name="Payment Status")
    payment_method = models.CharField(max_length=50, blank=True, verbose_name="Payment Method")
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name="Transaction ID")
    
    # Due Date
    due_date = models.DateField(verbose_name="Due Date")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="Paid At")
    
    # Notes
    description = models.TextField(blank=True, verbose_name="Description")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Application Fee"
        verbose_name_plural = "Application Fees"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.application.application_number} - {self.fee_type} ({self.amount} {self.currency})"
    
    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Updating fee: {self.fee_type}") if hasattr(self, '_meta') else None
        else:
            print(f"Creating new fee: {self.fee_type}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        """Check if fee payment is overdue."""
        return timezone.now().date() > self.due_date and self.payment_status == 'pending'


class ApplicationCommunication(models.Model):
    """
    Application communication model.
    """
    COMMUNICATION_TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('phone', 'Phone Call'),
        ('letter', 'Letter'),
        ('notification', 'In-App Notification'),
    ]
    
    DIRECTION_CHOICES = [
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='communications')
    communication_type = models.CharField(max_length=20, choices=COMMUNICATION_TYPE_CHOICES, verbose_name="Communication Type")
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, verbose_name="Direction")
    
    # Content
    subject = models.CharField(max_length=255, blank=True, verbose_name="Subject")
    message = models.TextField(verbose_name="Message")
    
    # Recipients
    from_email = models.EmailField(blank=True, verbose_name="From Email")
    to_email = models.EmailField(blank=True, verbose_name="To Email")
    from_phone = models.CharField(max_length=20, blank=True, verbose_name="From Phone")
    to_phone = models.CharField(max_length=20, blank=True, verbose_name="To Phone")
    
    # Status
    is_sent = models.BooleanField(default=False, verbose_name="Sent")
    is_delivered = models.BooleanField(default=False, verbose_name="Delivered")
    is_read = models.BooleanField(default=False, verbose_name="Read")
    
    # Timeline
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Sent At")
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name="Delivered At")
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="Read At")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Application Communication"
        verbose_name_plural = "Application Communications"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.application.application_number} - {self.communication_type} ({self.direction})"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            print(f"Communication created: {self.application.application_number}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)
