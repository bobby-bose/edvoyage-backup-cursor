from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

User = get_user_model()

class TimerSession(models.Model):
    """Timer sessions for study and work tracking"""
    SESSION_TYPE_CHOICES = [
        ('study', 'Study Session'),
        ('work', 'Work Session'),
        ('break', 'Break Session'),
        ('exercise', 'Exercise Session'),
        ('meditation', 'Meditation Session'),
        ('reading', 'Reading Session'),
        ('custom', 'Custom Session'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timer_sessions')
    
    # Session details
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES, default='study')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Duration settings
    target_duration = models.PositiveIntegerField(help_text='Target duration in minutes')
    actual_duration = models.PositiveIntegerField(default=0, help_text='Actual duration in minutes')
    break_duration = models.PositiveIntegerField(default=0, help_text='Break duration in minutes')
    
    # Time tracking
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    pause_start_time = models.DateTimeField(null=True, blank=True)
    total_pause_duration = models.PositiveIntegerField(default=0, help_text='Total pause duration in minutes')
    
    # Progress tracking
    progress_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_completed = models.BooleanField(default=False)
    
    # Settings
    auto_start_break = models.BooleanField(default=False)
    auto_start_next_session = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_time']
        verbose_name = "Timer Session"
        verbose_name_plural = "Timer Sessions"

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def save(self, *args, **kwargs):
        """Calculate progress and handle completion"""
        if self.actual_duration and self.target_duration:
            self.progress_percentage = (self.actual_duration / self.target_duration) * 100
            if self.progress_percentage >= 100:
                self.is_completed = True
                self.status = 'completed'
                if not self.end_time:
                    self.end_time = timezone.now()
        super().save(*args, **kwargs)

    @property
    def elapsed_time(self):
        """Calculate elapsed time in minutes"""
        if self.end_time:
            return int((self.end_time - self.start_time).total_seconds() / 60)
        else:
            return int((timezone.now() - self.start_time).total_seconds() / 60)

    @property
    def remaining_time(self):
        """Calculate remaining time in minutes"""
        if self.target_duration:
            return max(0, self.target_duration - self.actual_duration)
        return 0

    @property
    def is_active(self):
        """Check if session is currently active"""
        return self.status == 'active'

    @property
    def is_paused(self):
        """Check if session is paused"""
        return self.status == 'paused'

    def pause_session(self):
        """Pause the session"""
        if self.status == 'active':
            self.status = 'paused'
            self.pause_start_time = timezone.now()
            self.save()

    def resume_session(self):
        """Resume the session"""
        if self.status == 'paused' and self.pause_start_time:
            pause_duration = int((timezone.now() - self.pause_start_time).total_seconds() / 60)
            self.total_pause_duration += pause_duration
            self.status = 'active'
            self.pause_start_time = None
            self.save()

    def complete_session(self):
        """Complete the session"""
        self.status = 'completed'
        self.is_completed = True
        self.end_time = timezone.now()
        self.actual_duration = self.elapsed_time
        self.progress_percentage = 100
        self.save()

    def cancel_session(self):
        """Cancel the session"""
        self.status = 'cancelled'
        self.end_time = timezone.now()
        self.save()

class TimerBreak(models.Model):
    """Break sessions within timer sessions"""
    BREAK_TYPE_CHOICES = [
        ('short', 'Short Break'),
        ('long', 'Long Break'),
        ('custom', 'Custom Break'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timer_session = models.ForeignKey(TimerSession, on_delete=models.CASCADE, related_name='breaks')
    
    # Break details
    break_type = models.CharField(max_length=20, choices=BREAK_TYPE_CHOICES, default='short')
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    
    # Duration
    target_duration = models.PositiveIntegerField(help_text='Target break duration in minutes')
    actual_duration = models.PositiveIntegerField(default=0, help_text='Actual break duration in minutes')
    
    # Time tracking
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    # Status
    is_completed = models.BooleanField(default=False)
    is_skipped = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_time']
        verbose_name = "Timer Break"
        verbose_name_plural = "Timer Breaks"

    def __str__(self):
        return f"{self.break_type} break - {self.timer_session.title}"

    def save(self, *args, **kwargs):
        """Handle break completion"""
        if self.actual_duration and self.target_duration:
            if self.actual_duration >= self.target_duration:
                self.is_completed = True
                if not self.end_time:
                    self.end_time = timezone.now()
        super().save(*args, **kwargs)

    @property
    def elapsed_time(self):
        """Calculate elapsed time in minutes"""
        if self.end_time:
            return int((self.end_time - self.start_time).total_seconds() / 60)
        else:
            return int((timezone.now() - self.start_time).total_seconds() / 60)

    @property
    def remaining_time(self):
        """Calculate remaining time in minutes"""
        if self.target_duration:
            return max(0, self.target_duration - self.actual_duration)
        return 0

    def complete_break(self):
        """Complete the break"""
        self.is_completed = True
        self.end_time = timezone.now()
        self.actual_duration = self.elapsed_time
        self.save()

    def skip_break(self):
        """Skip the break"""
        self.is_skipped = True
        self.end_time = timezone.now()
        self.save()

class TimerTemplate(models.Model):
    """Predefined timer templates for quick setup"""
    TEMPLATE_TYPE_CHOICES = [
        ('pomodoro', 'Pomodoro Technique'),
        ('study', 'Study Session'),
        ('work', 'Work Session'),
        ('exercise', 'Exercise Session'),
        ('meditation', 'Meditation Session'),
        ('custom', 'Custom Template'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timer_templates')
    
    # Template details
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPE_CHOICES, default='custom')
    
    # Duration settings
    session_duration = models.PositiveIntegerField(help_text='Session duration in minutes')
    short_break_duration = models.PositiveIntegerField(default=5, help_text='Short break duration in minutes')
    long_break_duration = models.PositiveIntegerField(default=15, help_text='Long break duration in minutes')
    sessions_before_long_break = models.PositiveIntegerField(default=4, help_text='Number of sessions before long break')
    
    # Settings
    auto_start_breaks = models.BooleanField(default=True)
    auto_start_next_session = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=True)
    
    # Usage tracking
    usage_count = models.PositiveIntegerField(default=0)
    is_favorite = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-usage_count', '-created_at']
        verbose_name = "Timer Template"
        verbose_name_plural = "Timer Templates"

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    def increment_usage(self):
        """Increment usage count"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])

class TimerStatistics(models.Model):
    """Statistics and analytics for timer usage"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timer_statistics')
    
    # Daily statistics
    date = models.DateField()
    total_sessions = models.PositiveIntegerField(default=0)
    total_duration = models.PositiveIntegerField(default=0, help_text='Total duration in minutes')
    completed_sessions = models.PositiveIntegerField(default=0)
    cancelled_sessions = models.PositiveIntegerField(default=0)
    
    # Session type breakdown
    study_sessions = models.PositiveIntegerField(default=0)
    work_sessions = models.PositiveIntegerField(default=0)
    break_sessions = models.PositiveIntegerField(default=0)
    exercise_sessions = models.PositiveIntegerField(default=0)
    meditation_sessions = models.PositiveIntegerField(default=0)
    reading_sessions = models.PositiveIntegerField(default=0)
    custom_sessions = models.PositiveIntegerField(default=0)
    
    # Productivity metrics
    average_session_duration = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    productivity_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Timer Statistics"
        verbose_name_plural = "Timer Statistics"
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    def calculate_metrics(self):
        """Calculate productivity metrics"""
        if self.total_sessions > 0:
            self.average_session_duration = self.total_duration / self.total_sessions
            self.completion_rate = (self.completed_sessions / self.total_sessions) * 100
            
            # Simple productivity score based on completion rate and total duration
            self.productivity_score = (self.completion_rate * 0.7) + (min(self.total_duration / 60, 100) * 0.3)
        
        self.save()

class TimerGoal(models.Model):
    """Timer goals and targets for users"""
    GOAL_TYPE_CHOICES = [
        ('daily', 'Daily Goal'),
        ('weekly', 'Weekly Goal'),
        ('monthly', 'Monthly Goal'),
        ('custom', 'Custom Goal'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timer_goals')
    
    # Goal details
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES, default='daily')
    
    # Target settings
    target_duration = models.PositiveIntegerField(help_text='Target duration in minutes')
    target_sessions = models.PositiveIntegerField(default=0, help_text='Target number of sessions')
    target_completion_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=80,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Time period
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Progress tracking
    current_duration = models.PositiveIntegerField(default=0)
    current_sessions = models.PositiveIntegerField(default=0)
    current_completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Timer Goal"
        verbose_name_plural = "Timer Goals"

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    @property
    def progress_percentage(self):
        """Calculate progress percentage"""
        if self.target_duration:
            return min((self.current_duration / self.target_duration) * 100, 100)
        return 0

    @property
    def is_overdue(self):
        """Check if goal is overdue"""
        return timezone.now().date() > self.end_date and not self.is_completed

    def update_progress(self, session_duration, session_completed):
        """Update goal progress"""
        self.current_duration += session_duration
        self.current_sessions += 1
        
        if self.current_sessions > 0:
            completed_sessions = self.current_sessions if session_completed else self.current_sessions - 1
            self.current_completion_rate = (completed_sessions / self.current_sessions) * 100
        
        # Check if goal is completed
        if (self.current_duration >= self.target_duration and 
            self.current_completion_rate >= self.target_completion_rate):
            self.is_completed = True
        
        self.save()
