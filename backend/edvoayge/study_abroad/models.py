from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

User = get_user_model()

class StudyAbroadProgram(models.Model):
    """Study abroad programs and opportunities"""
    PROGRAM_TYPE_CHOICES = [
        ('semester', 'Semester Abroad'),
        ('summer', 'Summer Program'),
        ('year', 'Full Year'),
        ('short_term', 'Short Term'),
        ('exchange', 'Exchange Program'),
        ('internship', 'Internship Abroad'),
        ('research', 'Research Abroad'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Location details
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    campus_location = models.CharField(max_length=200, blank=True)
    
    # Academic details
    academic_level = models.CharField(max_length=100, blank=True)
    field_of_study = models.CharField(max_length=200, blank=True)
    credits_offered = models.PositiveIntegerField(null=True, blank=True)
    language_requirement = models.CharField(max_length=100, blank=True)
    
    # Duration and dates
    start_date = models.DateField()
    end_date = models.DateField()
    application_deadline = models.DateField()
    
    # Cost and financial information
    tuition_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    accommodation_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    other_costs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    scholarships_available = models.BooleanField(default=False)
    scholarship_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Capacity and requirements
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    min_gpa_requirement = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True,
                                            validators=[MinValueValidator(0.0), MaxValueValidator(4.0)])
    language_proficiency_required = models.BooleanField(default=False)
    visa_required = models.BooleanField(default=True)
    
    # Additional information
    highlights = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    application_process = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    
    # Media
    program_image = models.ImageField(upload_to='study_abroad/programs/', blank=True)
    brochure_file = models.FileField(upload_to='study_abroad/brochures/', blank=True)
    
    # Metadata
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Study Abroad Program"
        verbose_name_plural = "Study Abroad Programs"

    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"

    @property
    def total_cost(self):
        """Calculate total cost of the program"""
        total = 0
        if self.tuition_cost:
            total += self.tuition_cost
        if self.accommodation_cost:
            total += self.accommodation_cost
        if self.other_costs:
            total += self.other_costs
        return total

    @property
    def duration_days(self):
        """Calculate program duration in days"""
        return (self.end_date - self.start_date).days

    @property
    def is_application_open(self):
        """Check if applications are still open"""
        return timezone.now().date() <= self.application_deadline

    @property
    def available_spots(self):
        """Calculate available spots"""
        if self.max_participants:
            current_applications = self.applications.filter(status='accepted').count()
            return max(0, self.max_participants - current_applications)
        return None

class StudyAbroadApplication(models.Model):
    """Applications for study abroad programs"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('waitlisted', 'Waitlisted'),
        ('withdrawn', 'Withdrawn'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_abroad_applications')
    program = models.ForeignKey(StudyAbroadProgram, on_delete=models.CASCADE, related_name='applications')
    
    # Application details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    application_date = models.DateTimeField(auto_now_add=True)
    review_date = models.DateTimeField(null=True, blank=True)
    decision_date = models.DateTimeField(null=True, blank=True)
    
    # Personal information
    current_institution = models.CharField(max_length=200)
    current_major = models.CharField(max_length=200)
    current_gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True,
                                    validators=[MinValueValidator(0.0), MaxValueValidator(4.0)])
    graduation_date = models.DateField(null=True, blank=True)
    
    # Academic information
    academic_standing = models.CharField(max_length=100, blank=True)
    language_proficiency = models.CharField(max_length=100, blank=True)
    relevant_coursework = models.TextField(blank=True)
    academic_goals = models.TextField()
    
    # Personal statement and motivation
    personal_statement = models.TextField()
    motivation_letter = models.TextField(blank=True)
    
    # Additional documents
    resume_file = models.FileField(upload_to='study_abroad/applications/resumes/', blank=True)
    transcript_file = models.FileField(upload_to='study_abroad/applications/transcripts/', blank=True)
    recommendation_letters = models.FileField(upload_to='study_abroad/applications/recommendations/', blank=True)
    
    # Financial information
    financial_aid_needed = models.BooleanField(default=False)
    scholarship_applied = models.BooleanField(default=False)
    additional_funding_sources = models.TextField(blank=True)
    
    # Review information
    reviewer_notes = models.TextField(blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-application_date']
        verbose_name = "Study Abroad Application"
        verbose_name_plural = "Study Abroad Applications"
        unique_together = ['user', 'program']

    def __str__(self):
        return f"{self.user.username} - {self.program.name}"

    def save(self, *args, **kwargs):
        """Update timestamps when status changes"""
        if self.pk:
            old_instance = StudyAbroadApplication.objects.get(pk=self.pk)
            if old_instance.status != self.status:
                if self.status == 'under_review':
                    self.review_date = timezone.now()
                elif self.status in ['accepted', 'rejected', 'waitlisted']:
                    self.decision_date = timezone.now()
        super().save(*args, **kwargs)

class StudyAbroadExperience(models.Model):
    """User experiences and testimonials from study abroad"""
    EXPERIENCE_TYPE_CHOICES = [
        ('academic', 'Academic Experience'),
        ('cultural', 'Cultural Experience'),
        ('personal', 'Personal Growth'),
        ('professional', 'Professional Development'),
        ('social', 'Social Experience'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_abroad_experiences')
    program = models.ForeignKey(StudyAbroadProgram, on_delete=models.CASCADE, related_name='experiences')
    
    # Experience details
    title = models.CharField(max_length=200)
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPE_CHOICES)
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    # Media
    photos = models.ImageField(upload_to='study_abroad/experiences/photos/', blank=True)
    video_url = models.URLField(blank=True)
    
    # Approval and visibility
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Study Abroad Experience"
        verbose_name_plural = "Study Abroad Experiences"

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class StudyAbroadResource(models.Model):
    """Resources and guides for study abroad"""
    RESOURCE_TYPE_CHOICES = [
        ('guide', 'Guide'),
        ('checklist', 'Checklist'),
        ('template', 'Template'),
        ('video', 'Video'),
        ('article', 'Article'),
        ('faq', 'FAQ'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    description = models.TextField()
    content = models.TextField()
    
    # File attachments
    file_attachment = models.FileField(upload_to='study_abroad/resources/', blank=True)
    
    # Categories and tags
    categories = models.CharField(max_length=200, blank=True, help_text='Comma-separated categories')
    tags = models.CharField(max_length=200, blank=True, help_text='Comma-separated tags')
    
    # Visibility and access
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    requires_authentication = models.BooleanField(default=False)
    
    # Usage tracking
    download_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Study Abroad Resource"
        verbose_name_plural = "Study Abroad Resources"

    def __str__(self):
        return self.title

    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def increment_download_count(self):
        """Increment download count"""
        self.download_count += 1
        self.save(update_fields=['download_count'])

class StudyAbroadEvent(models.Model):
    """Events related to study abroad (info sessions, fairs, etc.)"""
    EVENT_TYPE_CHOICES = [
        ('info_session', 'Information Session'),
        ('fair', 'Study Abroad Fair'),
        ('workshop', 'Workshop'),
        ('webinar', 'Webinar'),
        ('orientation', 'Orientation'),
        ('reunion', 'Alumni Reunion'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    description = models.TextField()
    
    # Event details
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    is_virtual = models.BooleanField(default=False)
    virtual_meeting_url = models.URLField(blank=True)
    
    # Registration
    max_attendees = models.PositiveIntegerField(null=True, blank=True)
    registration_required = models.BooleanField(default=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_datetime']
        verbose_name = "Study Abroad Event"
        verbose_name_plural = "Study Abroad Events"

    def __str__(self):
        return f"{self.title} - {self.start_datetime.strftime('%Y-%m-%d %H:%M')}"

    @property
    def is_registration_open(self):
        """Check if registration is still open"""
        if not self.registration_required:
            return True
        if self.registration_deadline:
            return timezone.now() <= self.registration_deadline
        return True

    @property
    def available_spots(self):
        """Calculate available spots"""
        if self.max_attendees:
            registered_count = self.registrations.filter(status='registered').count()
            return max(0, self.max_attendees - registered_count)
        return None

class StudyAbroadEventRegistration(models.Model):
    """Event registrations for study abroad events"""
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_abroad_event_registrations')
    event = models.ForeignKey(StudyAbroadEvent, on_delete=models.CASCADE, related_name='registrations')
    
    # Registration details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    registration_date = models.DateTimeField(auto_now_add=True)
    attendance_date = models.DateTimeField(null=True, blank=True)
    
    # Additional information
    dietary_restrictions = models.CharField(max_length=200, blank=True)
    special_accommodations = models.TextField(blank=True)
    questions = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-registration_date']
        verbose_name = "Study Abroad Event Registration"
        verbose_name_plural = "Study Abroad Event Registrations"
        unique_together = ['user', 'event']

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

    def mark_attended(self):
        """Mark user as attended"""
        self.status = 'attended'
        self.attendance_date = timezone.now()
        self.save()
