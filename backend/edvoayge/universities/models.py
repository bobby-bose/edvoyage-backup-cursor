"""
University models for EdVoyage application.
Handles university information, campuses, rankings, and related data.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Feed(models.Model):
    university = models.ForeignKey(
        "University",
        on_delete=models.CASCADE,
        related_name="feeds",
        verbose_name="University",
    )
    user_name = models.CharField(max_length=255, verbose_name="User Name")
    profile_image = models.ImageField(
        upload_to="feeds/profile_images/", blank=True, null=True, verbose_name="Profile Image"
    )
    title = models.CharField(max_length=255, verbose_name="Heading / Title")
    description = models.TextField(verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Feed"
        verbose_name_plural = "Feeds"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.university.name} - {self.user_name}: {self.title}"

    @property
    def time_ago(self):
        """
        Returns human-readable time like "2 days ago".
        """
        now = timezone.now()
        diff = now - self.created_at

        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds // 3600 > 0:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds // 60 > 0:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "just now"


class University(models.Model):
    """
    University model with comprehensive information.
    """
    UNIVERSITY_TYPE_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('international', 'International'),
        ('research', 'Research'),
        ('liberal_arts', 'Liberal Arts'),
        ('technical', 'Technical'),
        ('medical', 'Medical'),
        ('business', 'Business'),
    ]
    
    name = models.CharField(max_length=255, verbose_name="University Name")
    short_name = models.CharField(max_length=100, blank=True, verbose_name="Short Name")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL Slug")
    
    # Basic Information
    description = models.TextField(blank=True, verbose_name="Description")
    mission_statement = models.TextField(blank=True, verbose_name="Mission Statement")
    vision_statement = models.TextField(blank=True, verbose_name="Vision Statement")
    
    # Type and Classification
    university_type = models.CharField(max_length=20, choices=UNIVERSITY_TYPE_CHOICES, verbose_name="University Type")
    founded_year = models.PositiveIntegerField(null=True, blank=True, verbose_name="Founded Year")
    accreditation = models.TextField(blank=True, verbose_name="Accreditation")
    
    # Contact Information
    website = models.URLField(blank=True, verbose_name="Website")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone")
    
    # Location
    country = models.CharField(max_length=100, verbose_name="Country")
    state = models.CharField(max_length=100, blank=True, verbose_name="State/Province")
    city = models.CharField(max_length=100, verbose_name="City")
    address = models.TextField(blank=True, verbose_name="Address")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="Postal Code")
    
    # Media
    logo = models.ImageField(upload_to='universities/logos/', null=True, blank=True, verbose_name="Logo")
    banner_image = models.ImageField(upload_to='universities/banners/', null=True, blank=True, verbose_name="Banner Image")
    # Gallery field for multiple images (uses ImageField with multiple=True via a related model)
    # This is the recommended Django way: use a separate model for gallery images, related to University.
    # The admin and serializers can handle multiple uploads.
    # The field below is a reverse relation, not a direct field.

    total_students = models.PositiveIntegerField(null=True, blank=True, verbose_name="Total Students")
    international_students = models.PositiveIntegerField(null=True, blank=True, verbose_name="International Students")
    faculty_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="Faculty Count")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_featured = models.BooleanField(default=False, verbose_name="Featured")
    is_verified = models.BooleanField(default=False, verbose_name="Verified")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universities"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Updating university: {self.name}") if hasattr(self, '_meta') else None
        else:
            print(f"Creating new university: {self.name}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)
    
    @property
    def age(self):
        """Calculate university age."""
        if self.founded_year:
            return timezone.now().year - self.founded_year
        return None
    
    @property
    def international_student_percentage(self):
        """Calculate international student percentage."""
        if self.total_students and self.international_students:
            return (self.international_students / self.total_students) * 100
        return None


class Campus(models.Model):
    """
    Campus model for university campuses.
    """
    CAMPUS_TYPE_CHOICES = [
        ('main', 'Main Campus'),
        ('branch', 'Branch Campus'),
        ('satellite', 'Satellite Campus'),
        ('online', 'Online Campus'),
        ('international', 'International Campus'),
    ]
    
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='campuses')
    name = models.CharField(max_length=255, verbose_name="Campus Name")
    campus_type = models.CharField(max_length=20, choices=CAMPUS_TYPE_CHOICES, default='main', verbose_name="Campus Type")
    
    # Location
    address = models.TextField(verbose_name="Address")
    city = models.CharField(max_length=100, verbose_name="City")
    state = models.CharField(max_length=100, blank=True, verbose_name="State/Province")
    country = models.CharField(max_length=100, verbose_name="Country")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="Postal Code")
    
    # Contact
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone")
    email = models.EmailField(blank=True, verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Website")
    
    # Facilities
    facilities = models.JSONField(default=list, blank=True, verbose_name="Facilities")
    accommodation = models.TextField(blank=True, verbose_name="Accommodation")
    transportation = models.TextField(blank=True, verbose_name="Transportation")
    
    # Media
    images = models.JSONField(default=list, blank=True, verbose_name="Campus Images")
    virtual_tour_url = models.URLField(blank=True, verbose_name="Virtual Tour URL")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_main_campus = models.BooleanField(default=False, verbose_name="Main Campus")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Campus"
        verbose_name_plural = "Campuses"
        ordering = ['university', 'name']
    
    def __str__(self):
        return f"{self.university.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Updating campus: {self.name}") if hasattr(self, '_meta') else None
        else:
            print(f"Creating new campus: {self.name}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)


class UniversityRanking(models.Model):
    """
    University ranking information.
    """
    RANKING_TYPE_CHOICES = [
        ('world', 'World Ranking'),
        ('national', 'National Ranking'),
        ('regional', 'Regional Ranking'),
        ('subject', 'Subject Ranking'),
        ('employability', 'Employability Ranking'),
        ('research', 'Research Ranking'),
    ]
    
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='rankings')
    ranking_type = models.CharField(max_length=20, choices=RANKING_TYPE_CHOICES, verbose_name="Ranking Type")
    ranking_source = models.CharField(max_length=100, verbose_name="Ranking Source")
    
    # Ranking Details
    rank = models.PositiveIntegerField(verbose_name="Rank")
    total_institutions = models.PositiveIntegerField(null=True, blank=True, verbose_name="Total Institutions")
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Score")
    
    # Year
    year = models.PositiveIntegerField(verbose_name="Year")
    
    # Additional Information
    methodology = models.TextField(blank=True, verbose_name="Methodology")
    criteria = models.JSONField(default=list, blank=True, verbose_name="Criteria")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "University Ranking"
        verbose_name_plural = "University Rankings"
        ordering = ['-year', 'ranking_type', 'rank']
        unique_together = ['university', 'ranking_type', 'ranking_source', 'year']
    
    def __str__(self):
        return f"{self.university.name} - {self.ranking_type} ({self.year})"
    
    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Updating ranking: {self.university.name} - {self.ranking_type}") if hasattr(self, '_meta') else None
        else:
            print(f"Creating new ranking: {self.university.name} - {self.ranking_type}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)


class UniversityProgram(models.Model):
    """
    University program information.
    """
    PROGRAM_LEVEL_CHOICES = [
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('postgraduate', 'Postgraduate'),
        ('phd', 'PhD'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ]
    
    PROGRAM_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('online', 'Online'),
        ('hybrid', 'Hybrid'),
        ('distance', 'Distance Learning'),
    ]
    
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=255, verbose_name="Program Name")
    program_level = models.CharField(max_length=20, choices=PROGRAM_LEVEL_CHOICES, verbose_name="Program Level")
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPE_CHOICES, verbose_name="Program Type")
    
    # Description
    description = models.TextField(blank=True, verbose_name="Description")
    objectives = models.TextField(blank=True, verbose_name="Objectives")
    outcomes = models.TextField(blank=True, verbose_name="Learning Outcomes")
    
    # Duration and Structure
    duration_years = models.PositiveIntegerField(verbose_name="Duration (Years)")
    total_credits = models.PositiveIntegerField(null=True, blank=True, verbose_name="Total Credits")
    semesters = models.PositiveIntegerField(default=2, verbose_name="Semesters per Year")
    
    # Requirements
    entry_requirements = models.TextField(blank=True, verbose_name="Entry Requirements")
    language_requirements = models.TextField(blank=True, verbose_name="Language Requirements")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_featured = models.BooleanField(default=False, verbose_name="Featured")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "University Program"
        verbose_name_plural = "University Programs"
        ordering = ['university', 'program_level', 'name']
    
    def __str__(self):
        return f"{self.university.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Updating program: {self.name}") if hasattr(self, '_meta') else None
        else:
            print(f"Creating new program: {self.name}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)


class UniversityFaculty(models.Model):
    """
    University faculty/department information.
    """
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='faculties')
    name = models.CharField(max_length=255, verbose_name="Faculty Name")
    short_name = models.CharField(max_length=50, blank=True, verbose_name="Short Name")
    
    # Description
    description = models.TextField(blank=True, verbose_name="Description")
    mission = models.TextField(blank=True, verbose_name="Mission")
    
    # Contact
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone")
    website = models.URLField(blank=True, verbose_name="Website")
    
    # Statistics
    student_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="Student Count")
    faculty_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="Faculty Count")
    
    # Media
    logo = models.ImageField(upload_to='faculties/logos/', null=True, blank=True, verbose_name="Logo")
    images = models.JSONField(default=list, blank=True, verbose_name="Images")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "University Faculty"
        verbose_name_plural = "University Faculties"
        ordering = ['university', 'name']
    
    def __str__(self):
        return f"{self.university.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Updating faculty: {self.name}") if hasattr(self, '_meta') else None
        else:
            print(f"Creating new faculty: {self.name}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)


class UniversityResearch(models.Model):
    """
    University research information.
    """
    RESEARCH_AREA_CHOICES = [
        ('science', 'Science'),
        ('technology', 'Technology'),
        ('engineering', 'Engineering'),
        ('medicine', 'Medicine'),
        ('arts', 'Arts & Humanities'),
        ('social_sciences', 'Social Sciences'),
        ('business', 'Business'),
        ('education', 'Education'),
        ('environment', 'Environment'),
        ('agriculture', 'Agriculture'),
    ]
    
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='research')
    title = models.CharField(max_length=255, verbose_name="Research Title")
    research_area = models.CharField(max_length=20, choices=RESEARCH_AREA_CHOICES, verbose_name="Research Area")
    
    # Description
    description = models.TextField(verbose_name="Description")
    objectives = models.TextField(blank=True, verbose_name="Objectives")
    methodology = models.TextField(blank=True, verbose_name="Methodology")
    
    # Funding
    funding_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Funding Amount")
    funding_source = models.CharField(max_length=255, blank=True, verbose_name="Funding Source")
    
    # Timeline
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(null=True, blank=True, verbose_name="End Date")
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('planned', 'Planned'),
        ('suspended', 'Suspended'),
    ], default='ongoing', verbose_name="Status")
    
    # Publications
    publications = models.JSONField(default=list, blank=True, verbose_name="Publications")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "University Research"
        verbose_name_plural = "University Research"
        ordering = ['-start_date', 'title']
    
    def __str__(self):
        return f"{self.university.name} - {self.title}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Updating research: {self.title}") if hasattr(self, '_meta') else None
        else:
            print(f"Creating new research: {self.title}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)


class UniversityPartnership(models.Model):
    """
    University partnership information.
    """
    PARTNERSHIP_TYPE_CHOICES = [
        ('academic', 'Academic'),
        ('research', 'Research'),
        ('student_exchange', 'Student Exchange'),
        ('faculty_exchange', 'Faculty Exchange'),
        ('joint_degree', 'Joint Degree'),
        ('mou', 'Memorandum of Understanding'),
    ]
    
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='partnerships')
    partner_name = models.CharField(max_length=255, verbose_name="Partner Name")
    partnership_type = models.CharField(max_length=20, choices=PARTNERSHIP_TYPE_CHOICES, verbose_name="Partnership Type")
    
    # Description
    description = models.TextField(verbose_name="Description")
    objectives = models.TextField(blank=True, verbose_name="Objectives")
    
    # Contact
    partner_contact = models.CharField(max_length=255, blank=True, verbose_name="Partner Contact")
    partner_email = models.EmailField(blank=True, verbose_name="Partner Email")
    partner_website = models.URLField(blank=True, verbose_name="Partner Website")
    
    # Timeline
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(null=True, blank=True, verbose_name="End Date")
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('pending', 'Pending'),
        ('terminated', 'Terminated'),
    ], default='active', verbose_name="Status")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "University Partnership"
        verbose_name_plural = "University Partnerships"
        ordering = ['-start_date', 'partner_name']
    
    def __str__(self):
        return f"{self.university.name} - {self.partner_name}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Updating partnership: {self.partner_name}") if hasattr(self, '_meta') else None
        else:
            print(f"Creating new partnership: {self.partner_name}") if hasattr(self, '_meta') else None
        super().save(*args, **kwargs)



class UniversityGallery(models.Model):
    university = models.OneToOneField(
        'University', 
        on_delete=models.CASCADE, 
        related_name='gallery'
    )
    
    image1 = models.ImageField(upload_to='universities/gallery/', verbose_name="University Image 1", blank=True, null=True)
    image2 = models.ImageField(upload_to='universities/gallery/', verbose_name="University Image 2", blank=True, null=True)
    image3 = models.ImageField(upload_to='universities/gallery/', verbose_name="University Image 3", blank=True, null=True)
    image4 = models.ImageField(upload_to='universities/gallery/', verbose_name="University Image 4", blank=True, null=True)
    image5 = models.ImageField(upload_to='universities/gallery/', verbose_name="University Image 5", blank=True, null=True)
    image6 = models.ImageField(upload_to='universities/gallery/', verbose_name="University Image 6", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
