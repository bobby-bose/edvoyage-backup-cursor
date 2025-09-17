from django.db import models
from django.utils import timezone
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name





class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    category = models.ForeignKey(Category, related_name='videos', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    duration_in_minutes = models.PositiveIntegerField()
    is_free = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='video_logos/')
    doctor = models.ForeignKey(Doctor, related_name='videos', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class MCQ(models.Model):
    category = models.ForeignKey(Category, related_name='mcqs', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='mcqs', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    is_free = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='mcq_logos/')

    def __str__(self):
        return f"{self.subject.name} - {self.title}"



class Question(models.Model):
    """
    This model represents a single question within an MCQ set.
    It is linked to a specific MCQ.
    """
    mcq = models.ForeignKey(MCQ, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField(help_text="The text of the question.")

    def __str__(self):
        # Returns the first 50 characters of the question for a clean admin display
        return self.text[:50]

class Option(models.Model):
    """
    This model represents one of the possible answers for a Question.
    It is linked to a specific Question and has a flag to mark the correct answer.
    """
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, help_text="The text for this answer option.")
    is_correct = models.BooleanField(default=False, help_text="Mark this if it is the correct answer.")

    def __str__(self):
        return f"Option for question: {self.question.id} | {self.text}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'is_correct'],
                condition=models.Q(is_correct=True),
                name='unique_correct_option_for_question'
            )
        ]




class ClinicalCase(models.Model):
    """
    Represents a clinical case examination with detailed sections for data entry.
    Each section is a TextField to accommodate large amounts of text.
    """
    
    # A title field to easily identify each case

    category = models.ForeignKey(Category, related_name='cases', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='cases', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='cases', on_delete=models.CASCADE)
    case_title = models.CharField(max_length=255, help_text="Enter the title for this clinical case, e.g., 'Cardiovascular Examination of Patient X'.")

    # The fields you requested for large text input
    gather_equipments = models.TextField(
        verbose_name="Gather Equipments",
        help_text="List all necessary equipment for the examination."
    )
    
    introduction = models.TextField(
        verbose_name="Introduction",
        help_text="Describe the introduction to the patient, including consent."
    )
    
    general_inspection = models.TextField(
        verbose_name="General Inspection",
        help_text="Detail the findings from the general inspection of the patient."
    )
    
    closer_inspection = models.TextField(
        verbose_name="Closer Inspection",
        help_text="Detail the findings from a closer, more focused inspection."
    )
    
    palpation = models.TextField(
        verbose_name="Palpation",
        help_text="Record the findings from palpation."
    )
    
    final_examination = models.TextField(
        verbose_name="Final Examination",
        help_text="Describe any final examination steps, like auscultation or percussion."
    )
    
    references = models.TextField(
        verbose_name="References",
        help_text="List any references or sources cited.",
        blank=True, # This field is optional
        null=True
    )

    # Timestamps for tracking when the record was created or updated
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a human-readable string representation of the case,
        which is used in the Django admin site.
        """
        return self.case_title

    class Meta:
        verbose_name = "Clinical Case"
        verbose_name_plural = "Clinical Cases"
        ordering = ['-created_at'] # Show the most recent cases first




class Flashcard(models.Model):
    category = models.ForeignKey(Category, related_name='flashcards', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='flashcards', on_delete=models.CASCADE)
    description = models.TextField(
        blank=True,
        help_text="Optional: A brief description or the 'back' of the main card."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject.name

class FlashcardImage(models.Model):
    flashcard = models.ForeignKey(
        Flashcard,
        related_name='images',  # Allows you to access images from a flashcard object like: my_flashcard.images.all()
        on_delete=models.CASCADE  # Deletes all images if the parent flashcard is deleted.
    )
    # This field stores the uploaded image.
    image = models.ImageField(upload_to='flashcards/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        # Provides a helpful name in the admin panel.
        return f"Image for '{self.flashcard.subject.name}'"