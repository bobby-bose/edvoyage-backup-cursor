from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

User = get_user_model()

class QuizCategory(models.Model):
    """Model for organizing quizzes into categories"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#FF5733')  # Hex color
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Quiz Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def quiz_count(self):
        return self.quizzes.count()

class Quiz(models.Model):
    """Main quiz model"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(QuizCategory, on_delete=models.CASCADE, related_name='quizzes')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    
    # Quiz settings
    time_limit = models.PositiveIntegerField(help_text='Time limit in minutes (0 for no limit)')
    passing_score = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Minimum score to pass (0-100)'
    )
    max_attempts = models.PositiveIntegerField(default=3, help_text='Maximum attempts allowed')
    
    # Quiz properties
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_public = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Analytics
    total_attempts = models.PositiveIntegerField(default=0)
    average_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def question_count(self):
        return self.questions.count()

    @property
    def is_active(self):
        return self.status == 'published' and self.is_public

class Question(models.Model):
    """Individual question model"""
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('fill_blank', 'Fill in the Blank'),
        ('essay', 'Essay'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')
    points = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)
    explanation = models.TextField(blank=True, help_text='Explanation shown after answering')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.quiz.title} - {self.question_text[:50]}"

    @property
    def correct_options(self):
        return self.options.filter(is_correct=True)

class Option(models.Model):
    """Multiple choice options for questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.question.question_text[:30]} - {self.option_text[:30]}"

class QuizAttempt(models.Model):
    """Student's attempt at a quiz"""
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    
    # Attempt details
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='in_progress')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    passed = models.BooleanField(null=True, blank=True)
    
    # Time tracking
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_taken = models.PositiveIntegerField(null=True, blank=True, help_text='Time taken in seconds')
    
    # User answers
    answers = models.JSONField(default=dict, help_text='Stores user answers as JSON')
    
    # Analytics
    questions_attempted = models.PositiveIntegerField(default=0)
    questions_correct = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-started_at']
        unique_together = ['quiz', 'user', 'started_at']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.status})"

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
            if self.started_at and self.completed_at:
                self.time_taken = int((self.completed_at - self.started_at).total_seconds())
        super().save(*args, **kwargs)

    @property
    def is_passed(self):
        if self.percentage is not None:
            return self.percentage >= self.quiz.passing_score
        return False

class QuizResult(models.Model):
    """Detailed results for quiz attempts"""
    attempt = models.OneToOneField(QuizAttempt, on_delete=models.CASCADE, related_name='result')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='results')
    
    # Answer details
    user_answer = models.TextField(blank=True)
    is_correct = models.BooleanField()
    points_earned = models.PositiveIntegerField(default=0)
    time_taken = models.PositiveIntegerField(null=True, blank=True, help_text='Time taken for this question in seconds')
    
    # Feedback
    feedback = models.TextField(blank=True)
    explanation_shown = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.attempt.user.username} - {self.question.question_text[:30]}"

class QuizAnalytics(models.Model):
    """Analytics tracking for quizzes"""
    ACTION_TYPES = [
        ('view', 'View'),
        ('start', 'Start'),
        ('complete', 'Complete'),
        ('abandon', 'Abandon'),
        ('share', 'Share'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='analytics')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_analytics', null=True, blank=True)
    action_type = models.CharField(max_length=15, choices=ACTION_TYPES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Quiz Analytics'

    def __str__(self):
        return f"{self.quiz.title} - {self.action_type} - {self.created_at}"

class QuizShare(models.Model):
    """Quiz sharing functionality"""
    SHARE_TYPES = [
        ('link', 'Link'),
        ('email', 'Email'),
        ('social', 'Social Media'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='shares')
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_shares_sent')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_shares_received', null=True, blank=True)
    share_type = models.CharField(max_length=10, choices=SHARE_TYPES)
    message = models.TextField(blank=True)
    share_url = models.URLField(blank=True)
    is_viewed = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.quiz.title} shared by {self.shared_by.username}"

class QuizTimer(models.Model):
    """Timer tracking for quiz attempts"""
    attempt = models.OneToOneField(QuizAttempt, on_delete=models.CASCADE, related_name='timer')
    time_limit = models.PositiveIntegerField(help_text='Time limit in seconds')
    time_remaining = models.PositiveIntegerField(help_text='Time remaining in seconds')
    is_paused = models.BooleanField(default=False)
    paused_at = models.DateTimeField(null=True, blank=True)
    resumed_at = models.DateTimeField(null=True, blank=True)
    total_pause_time = models.PositiveIntegerField(default=0, help_text='Total pause time in seconds')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Timer for {self.attempt}"

    @property
    def is_expired(self):
        return self.time_remaining <= 0

    def pause(self):
        if not self.is_paused:
            self.is_paused = True
            self.paused_at = timezone.now()
            self.save()

    def resume(self):
        if self.is_paused:
            self.is_paused = False
            self.resumed_at = timezone.now()
            if self.paused_at:
                pause_duration = int((self.resumed_at - self.paused_at).total_seconds())
                self.total_pause_time += pause_duration
            self.save()
