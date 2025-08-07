"""
Course URL patterns for EdVoyage API.
Defines routing for course-related endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, SubjectViewSet, CourseApplicationViewSet

# Create router for ViewSets
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'subjects', SubjectViewSet, basename='subjects')
router.register(r'applications', CourseApplicationViewSet, basename='applications')

# URL patterns
urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Additional custom endpoints can be added here if needed
    # Example: path('custom-endpoint/', views.custom_view, name='custom_endpoint'),
] 