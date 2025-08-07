from django.contrib import admin
from .models import FavouriteUniversity, FavouriteCourse

@admin.register(FavouriteUniversity)
class FavouriteUniversityAdmin(admin.ModelAdmin):
    list_display = ['user', 'university', 'created_at']
    list_filter = ['created_at', 'university__country', 'university__university_type']
    search_fields = ['user__username', 'user__email', 'university__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    list_per_page = 25

@admin.register(FavouriteCourse)
class FavouriteCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'course_university', 'created_at']
    list_filter = ['created_at', 'course__level', 'course__university__country']
    search_fields = ['user__username', 'user__email', 'course__name', 'course__university__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    list_per_page = 25
    
    def course_university(self, obj):
        return obj.course.university.name
    course_university.short_description = 'University'