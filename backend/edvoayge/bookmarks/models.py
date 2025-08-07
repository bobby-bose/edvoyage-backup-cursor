from django.db import models
from users.models import User
from universities.models import University
from courses.models import Course

class FavouriteUniversity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourite_universities')
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='favourite_universities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Favourite University"
        verbose_name_plural = "Favourite Universities"
        unique_together = ['user', 'university']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.university.name}"

class FavouriteCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourite_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='favourite_courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Favourite Course"
        verbose_name_plural = "Favourite Courses"
        unique_together = ['user', 'course']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"
