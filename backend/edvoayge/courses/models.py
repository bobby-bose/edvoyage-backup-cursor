"""
Course models for EdVoyage application.
Handles course management, subjects, fees, requirements, and applications.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils import timezone


class Course(models.Model):
    """
    Course model representing educational courses offered by universities.
    """
    DURATION_CHOICES = [
        ('1_year', '1 Year'),
        ('2_years', '2 Years'),
        ('3_years', '3 Years'),
        ('4_years', '4 Years'),
        ('6_months', '6 Months'),
        ('1_semester', '1 Semester'),
    ]
    
    LEVEL_CHOICES = [
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Postgraduate'),
        ('phd', 'PhD'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('coming_soon', 'Coming Soon'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255, verbose_name="Course Name")
    code = models.CharField(max_length=50, unique=True, verbose_name="Course Code")
    description = models.TextField(verbose_name="Course Description")
    short_description = models.CharField(max_length=500, blank=True, verbose_name="Short Description")
    
    # University and Level
    university = models.ForeignKey('universities.University', on_delete=models.CASCADE, related_name='courses')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='undergraduate')
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default='4_years')
    
    # Academic Details
    credits = models.PositiveIntegerField(default=120, verbose_name="Total Credits")
    subjects = models.ManyToManyField('Subject', through='CourseSubject', related_name='courses')
    
    # Fees and Financial
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tuition Fee")
    currency = models.CharField(max_length=3, default='USD', verbose_name="Currency")
    
    # Requirements and Eligibility
    minimum_gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name="Minimum GPA")
    language_requirements = models.TextField(blank=True, verbose_name="Language Requirements")
    
    # Status and Visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False, verbose_name="Featured Course")
    is_popular = models.BooleanField(default=False, verbose_name="Popular Course")
    
    # Media
    image = models.ImageField(upload_to='courses/images/', null=True, blank=True, verbose_name="Course Image")
    brochure = models.FileField(upload_to='courses/brochures/', null=True, blank=True, verbose_name="Course Brochure")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['university']),
            models.Index(fields=['level']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.university.name}"
    
    @property
    def average_rating(self):
        """Calculate average rating for the course."""
        ratings = self.ratings.all()
        if ratings:
            return sum(r.rating for r in ratings) / len(ratings)
        return 0
    
    @property
    def total_applications(self):
        """Get total number of applications for this course."""
        return self.applications.count()
    
    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Updating course: {self.name}") if hasattr(self, '_meta') and hasattr(self._meta, 'app_label') else None
        else:
            print(f"Creating new course: {self.name}") if hasattr(self, '_meta') and hasattr(self._meta, 'app_label') else None
        super().save(*args, **kwargs)


class Subject(models.Model):
    """
    Subject model representing individual subjects within courses.
    """
    name = models.CharField(max_length=255, verbose_name="Subject Name")
    code = models.CharField(max_length=50, unique=True, verbose_name="Subject Code")
    description = models.TextField(blank=True, verbose_name="Subject Description")
    credits = models.PositiveIntegerField(default=3, verbose_name="Credits")
    is_core = models.BooleanField(default=True, verbose_name="Core Subject")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class CourseSubject(models.Model):
    """
    Through model for Course-Subject relationship with additional fields.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.PositiveIntegerField(default=1, verbose_name="Semester")
    is_optional = models.BooleanField(default=False, verbose_name="Optional Subject")
    
    class Meta:
        unique_together = ['course', 'subject']
        verbose_name = "Course Subject"
        verbose_name_plural = "Course Subjects"


class FeeStructure(models.Model):
    """
    Detailed fee structure for courses.
    """
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='fee_structure')
    
    # Tuition Fees
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tuition Fee")
    tuition_fee_per_semester = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Additional Costs
    accommodation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Accommodation Fee")
    meal_plan_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Meal Plan Fee")
    transportation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Transportation Fee")
    health_insurance_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Health Insurance Fee")
    books_materials_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Books & Materials Fee")
    other_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Other Fees")
    
    # Currency
    currency = models.CharField(max_length=3, default='USD', verbose_name="Currency")
    
    # Payment Terms
    payment_terms = models.TextField(blank=True, verbose_name="Payment Terms")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Fee Structure"
        verbose_name_plural = "Fee Structures"
    
    def __str__(self):
        return f"Fee Structure - {self.course.name}"
    
    @property
    def total_fees(self):
        """Calculate total fees for the course."""
        return (self.tuition_fee + self.accommodation_fee + self.meal_plan_fee + 
                self.transportation_fee + self.health_insurance_fee + 
                self.books_materials_fee + self.other_fees)


class CourseRequirement(models.Model):
    """
    Requirements for course admission.
    """
    REQUIREMENT_TYPE_CHOICES = [
        ('academic', 'Academic'),
        ('language', 'Language'),
        ('document', 'Document'),
        ('experience', 'Experience'),
        ('other', 'Other'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='requirements')
    requirement_type = models.CharField(max_length=20, choices=REQUIREMENT_TYPE_CHOICES, verbose_name="Requirement Type")
    title = models.CharField(max_length=255, verbose_name="Requirement Title")
    description = models.TextField(verbose_name="Requirement Description")
    is_mandatory = models.BooleanField(default=True, verbose_name="Mandatory Requirement")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Course Requirement"
        verbose_name_plural = "Course Requirements"
        ordering = ['order', 'requirement_type']
    
    def __str__(self):
        return f"{self.title} - {self.course.name}"


class CourseApplication(models.Model):
    """
    Course application model for tracking student applications.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('waitlisted', 'Waitlisted'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_applications')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Application Details
    personal_statement = models.TextField(blank=True, verbose_name="Personal Statement")
    expected_start_date = models.DateField(null=True, blank=True, verbose_name="Expected Start Date")
    
    # Review Details
    review_notes = models.TextField(blank=True, verbose_name="Review Notes")
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_reviewed_applications')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Course Application"
        verbose_name_plural = "Course Applications"
        ordering = ['-created_at']
        unique_together = ['user', 'course']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.name} ({self.status})"
    
    def save(self, *args, **kwargs):
        if self.pk and self.status != self._state.fields_cache.get('status', self.status):
            print(f"Application status changed to: {self.status}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)


class CourseRating(models.Model):
    """
    Course rating and review model.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_ratings')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Rating (1-5)"
    )
    review = models.TextField(blank=True, verbose_name="Review")
    is_verified = models.BooleanField(default=False, verbose_name="Verified Review")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Course Rating"
        verbose_name_plural = "Course Ratings"
        ordering = ['-created_at']
        unique_together = ['user', 'course']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.name} ({self.rating}/5)"
    
    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Updating course rating: {self.course.name} by {self.user.username}") if hasattr(self, '_meta') else None
        else:
            print(f"New course rating: {self.course.name} by {self.user.username}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)
