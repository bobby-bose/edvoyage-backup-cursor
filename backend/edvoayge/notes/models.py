from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class NotesCategory(models.Model):
    """
    Model for different categories of notes content.
    """
    CATEGORY_CHOICES = [
        ('video', 'Video'),
        ('mcq', 'MCQ'),
        ('clinical_case', 'Clinical Case'),
        ('q_bank', 'Q-Bank'),
        ('flash_card', 'Flash Card'),
        ('previous_papers', 'Previous Year Papers'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True, verbose_name="Category Name")
    display_name = models.CharField(max_length=100, verbose_name="Display Name")
    description = models.TextField(blank=True, verbose_name="Description")
    
    # Statistics
    topics_count = models.PositiveIntegerField(default=0, verbose_name="Topics Count")
    modules_count = models.PositiveIntegerField(default=0, verbose_name="Modules Count")
    videos_count = models.PositiveIntegerField(default=0, verbose_name="Videos Count")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_featured = models.BooleanField(default=False, verbose_name="Featured")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Notes Category"
        verbose_name_plural = "Notes Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.display_name
    
    def get_total_content_count(self):
        """Get total content count for this category."""
        if self.name == 'video':
            return self.videos_count
        return self.modules_count


class NotesTopic(models.Model):
    """
    Model for individual topics within categories.
    """
    category = models.ForeignKey(NotesCategory, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=255, verbose_name="Topic Title")
    description = models.TextField(blank=True, verbose_name="Description")
    
    # Content counts
    modules_count = models.PositiveIntegerField(default=0, verbose_name="Modules Count")
    videos_count = models.PositiveIntegerField(default=0, verbose_name="Videos Count")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_featured = models.BooleanField(default=False, verbose_name="Featured")
    
    # Ordering
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Notes Topic"
        verbose_name_plural = "Notes Topics"
        ordering = ['category', 'order', 'title']
        unique_together = ['category', 'title']
    
    def __str__(self):
        return f"{self.category.display_name} - {self.title}"


class NotesModule(models.Model):
    """
    Model for individual modules/content items.
    """
    MODULE_TYPE_CHOICES = [
        ('video', 'Video'),
        ('mcq', 'MCQ'),
        ('clinical_case', 'Clinical Case'),
        ('q_bank', 'Q-Bank'),
        ('flash_card', 'Flash Card'),
        ('previous_papers', 'Previous Year Papers'),
    ]
    
    topic = models.ForeignKey(NotesTopic, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255, verbose_name="Module Title")
    module_type = models.CharField(max_length=20, choices=MODULE_TYPE_CHOICES, verbose_name="Module Type")
    
    # Content details
    description = models.TextField(blank=True, verbose_name="Description")
    content_url = models.URLField(blank=True, verbose_name="Content URL")
    duration_minutes = models.PositiveIntegerField(null=True, blank=True, verbose_name="Duration (Minutes)")
    
    # Instructor/Doctor information
    instructor = models.CharField(max_length=255, blank=True, verbose_name="Instructor/Doctor")
    
    # Access control
    access_type = models.CharField(max_length=20, choices=[
        ('free', 'Free'),
        ('premium', 'Premium'),
    ], default='free', verbose_name="Access Type")
    
    # Statistics
    views_count = models.PositiveIntegerField(default=0, verbose_name="Views Count")
    likes_count = models.PositiveIntegerField(default=0, verbose_name="Likes Count")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_premium = models.BooleanField(default=False, verbose_name="Premium Content")
    
    # Ordering
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Notes Module"
        verbose_name_plural = "Notes Modules"
        ordering = ['topic', 'order', 'title']
        unique_together = ['topic', 'title']
    
    def __str__(self):
        return f"{self.topic.title} - {self.title}"


















# -----------------------------------------------











class NotesVideo(models.Model):
    """
    Model for video content specifically.
    """
    module = models.OneToOneField(NotesModule, on_delete=models.CASCADE, related_name='video')
    video_url = models.URLField(verbose_name="Video URL")
    thumbnail_url = models.URLField(blank=True, verbose_name="Thumbnail URL")
    
    # Video details
    duration_seconds = models.PositiveIntegerField(verbose_name="Duration (Seconds)")
    quality = models.CharField(max_length=20, choices=[
        ('360p', '360p'),
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
    ], default='720p', verbose_name="Video Quality")
    
    # Statistics
    views_count = models.PositiveIntegerField(default=0, verbose_name="Views Count")
    likes_count = models.PositiveIntegerField(default=0, verbose_name="Likes Count")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Notes Video"
        verbose_name_plural = "Notes Videos"
    
    def __str__(self):
        return f"Video: {self.module.title}"


class NotesMCQ(models.Model):
    """
    Model for MCQ content.
    """
    module = models.OneToOneField(NotesModule, on_delete=models.CASCADE, related_name='mcq')
    
    # MCQ details
    question_text = models.TextField(verbose_name="Question Text")
    explanation = models.TextField(blank=True, verbose_name="Explanation")
    
    # Statistics
    attempts_count = models.PositiveIntegerField(default=0, verbose_name="Attempts Count")
    correct_answers_count = models.PositiveIntegerField(default=0, verbose_name="Correct Answers Count")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Notes MCQ"
        verbose_name_plural = "Notes MCQs"
    
    def __str__(self):
        return f"MCQ: {self.module.title}"


class NotesMCQOption(models.Model):
    """
    Model for MCQ options.
    """
    mcq = models.ForeignKey(NotesMCQ, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=500, verbose_name="Option Text")
    is_correct = models.BooleanField(default=False, verbose_name="Is Correct Answer")
    
    # Ordering
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    
    class Meta:
        verbose_name = "Notes MCQ Option"
        verbose_name_plural = "Notes MCQ Options"
        ordering = ['mcq', 'order']
    
    def __str__(self):
        return f"{self.mcq.module.title} - Option {self.order}"


class NotesClinicalCase(models.Model):
    """
    Model for clinical case content.
    """
    module = models.OneToOneField(NotesModule, on_delete=models.CASCADE, related_name='clinical_case')
    
    # Case details
    case_title = models.CharField(max_length=255, verbose_name="Case Title")
    patient_history = models.TextField(verbose_name="Patient History")
    clinical_findings = models.TextField(verbose_name="Clinical Findings")
    diagnosis = models.TextField(blank=True, verbose_name="Diagnosis")
    treatment = models.TextField(blank=True, verbose_name="Treatment")
    
    # Statistics
    views_count = models.PositiveIntegerField(default=0, verbose_name="Views Count")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Notes Clinical Case"
        verbose_name_plural = "Notes Clinical Cases"
    
    def __str__(self):
        return f"Clinical Case: {self.case_title}"


class NotesQBank(models.Model):
    """
    Model for Q-Bank content.
    """
    module = models.OneToOneField(NotesModule, on_delete=models.CASCADE, related_name='q_bank')
    
    # Q-Bank details
    question_text = models.TextField(verbose_name="Question Text")
    explanation = models.TextField(blank=True, verbose_name="Explanation")
    difficulty_level = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ], default='medium', verbose_name="Difficulty Level")
    
    # Statistics
    attempts_count = models.PositiveIntegerField(default=0, verbose_name="Attempts Count")
    correct_answers_count = models.PositiveIntegerField(default=0, verbose_name="Correct Answers Count")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Notes Q-Bank"
        verbose_name_plural = "Notes Q-Banks"
    
    def __str__(self):
        return f"Q-Bank: {self.module.title}"


class NotesQBankOption(models.Model):
    """
    Model for Q-Bank options.
    """
    q_bank = models.ForeignKey(NotesQBank, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=500, verbose_name="Option Text")
    is_correct = models.BooleanField(default=False, verbose_name="Is Correct Answer")
    
    # Ordering
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    
    class Meta:
        verbose_name = "Notes Q-Bank Option"
        verbose_name_plural = "Notes Q-Bank Options"
        ordering = ['q_bank', 'order']
    
    def __str__(self):
        return f"Option {self.order}: {self.option_text[:50]}..."


class NotesFlashCard(models.Model):
    """
    Model for flash card content.
    """
    module = models.OneToOneField(NotesModule, on_delete=models.CASCADE, related_name='flash_card')
    
    # Flash card details
    front_text = models.TextField(verbose_name="Front Text")
    back_text = models.TextField(verbose_name="Back Text")
    category = models.CharField(max_length=100, blank=True, verbose_name="Category")
    
    # Statistics
    views_count = models.PositiveIntegerField(default=0, verbose_name="Views Count")
    mastery_level = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Mastery Level (%)"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Notes Flash Card"
        verbose_name_plural = "Notes Flash Cards"
    
    def __str__(self):
        return f"Flash Card: {self.module.title}"


class NotesPreviousPapers(models.Model):
    """
    Model for Previous Year Papers content.
    """
    module = models.OneToOneField(NotesModule, on_delete=models.CASCADE, related_name='previous_papers')
    
    # Paper details
    paper_title = models.CharField(max_length=255, verbose_name="Paper Title")
    year = models.PositiveIntegerField(verbose_name="Year")
    exam_type = models.CharField(max_length=100, verbose_name="Exam Type")
    paper_url = models.URLField(blank=True, verbose_name="Paper URL")
    solution_url = models.URLField(blank=True, verbose_name="Solution URL")
    
    # Paper content
    total_questions = models.PositiveIntegerField(default=0, verbose_name="Total Questions")
    duration_minutes = models.PositiveIntegerField(default=0, verbose_name="Duration (Minutes)")
    difficulty_level = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ], default='medium', verbose_name="Difficulty Level")
    
    # Statistics
    views_count = models.PositiveIntegerField(default=0, verbose_name="Views Count")
    downloads_count = models.PositiveIntegerField(default=0, verbose_name="Downloads Count")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Notes Previous Year Papers"
        verbose_name_plural = "Notes Previous Year Papers"
    
    def __str__(self):
        return f"Previous Year Paper: {self.paper_title} ({self.year})"


class NotesStatistics(models.Model):
    """
    Model for tracking notes usage statistics.
    """
    date = models.DateField(unique=True, verbose_name="Date")
    
    # Daily statistics
    total_views = models.PositiveIntegerField(default=0, verbose_name="Total Views")
    total_modules_accessed = models.PositiveIntegerField(default=0, verbose_name="Total Modules Accessed")
    total_unique_users = models.PositiveIntegerField(default=0, verbose_name="Total Unique Users")
    
    # Category-wise statistics
    video_views = models.PositiveIntegerField(default=0, verbose_name="Video Views")
    mcq_attempts = models.PositiveIntegerField(default=0, verbose_name="MCQ Attempts")
    clinical_case_views = models.PositiveIntegerField(default=0, verbose_name="Clinical Case Views")
    q_bank_attempts = models.PositiveIntegerField(default=0, verbose_name="Q-Bank Attempts")
    flash_card_views = models.PositiveIntegerField(default=0, verbose_name="Flash Card Views")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Notes Statistics"
        verbose_name_plural = "Notes Statistics"
        ordering = ['-date']
    
    def __str__(self):
        return f"Statistics for {self.date}"
