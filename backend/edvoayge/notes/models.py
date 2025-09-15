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
    
    def __str__(self):
        return self.name
    
    

class NotesVideoMain(models.Model):
    category = models.ForeignKey(NotesCategory, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=255, verbose_name="Topic Title")
    
    def __str__(self):
        return f"{self.category.name} - {self.title}"
    
class NotesVideoSub(models.Model):
    title = models.ForeignKey(NotesVideoMain, on_delete=models.CASCADE, related_name='topics')
    name= models.CharField(max_length=255, verbose_name="Video Title")
    doctor = models.CharField(max_length=255, verbose_name="Doctor Name")
    duration = models.PositiveIntegerField(verbose_name="Duration (Seconds)")
    logo = models.ImageField(upload_to='video_logos/', blank=True, verbose_name="Logo")
    free = models.BooleanField(default=True, verbose_name="Is Free")
    
    def __str__(self):
        return f"{self.title} - {self.doctor}"
    
class NotesVideoPlayer(models.Model):
    video = models.OneToOneField(NotesVideoSub, on_delete=models.CASCADE, related_name='player')
    completed = models.BooleanField(default=False, verbose_name="Completed")
    url = models.URLField(max_length=500, verbose_name="Video URL")

    def __str__(self):
        return f"Video Player for {self.video.title}-{self.video.name}"




