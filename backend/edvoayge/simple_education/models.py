from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

User = get_user_model()

class SimpleEducation(models.Model):
    """Simple education model with higher and lower education"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education')
    
    # Higher Education
    higher_start_year = models.IntegerField(null=True, blank=True)
    higher_end_year = models.IntegerField(null=True, blank=True)
    higher_gpa = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('5.00'))]
    )
    
    # Lower Education
    lower_start_year = models.IntegerField(null=True, blank=True)
    lower_end_year = models.IntegerField(null=True, blank=True)
    lower_gpa = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('5.00'))]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Simple Education"
        verbose_name_plural = "Simple Education"

    def __str__(self):
        return f"{self.user.username}'s Education"

class SimpleWork(models.Model):
    """Simple work model with basic work details"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work', null=True, blank=True)
    
    position = models.CharField(max_length=200, blank=True, null=True)
    start_year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    pursuing = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Simple Work"
        verbose_name_plural = "Simple Work"

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'}'s Work - {self.position or 'No Position'}"

class SimpleSocial(models.Model):
    """Simple social links model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social', null=True, blank=True)
    
    facebook_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Simple Social"
        verbose_name_plural = "Simple Social"

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'}'s Social Links"
