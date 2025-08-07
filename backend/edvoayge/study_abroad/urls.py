from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudyAbroadProgramViewSet, StudyAbroadApplicationViewSet, StudyAbroadExperienceViewSet,
    StudyAbroadResourceViewSet, StudyAbroadEventViewSet, StudyAbroadEventRegistrationViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'study-abroad-programs', StudyAbroadProgramViewSet, basename='study-abroad-program')
router.register(r'study-abroad-applications', StudyAbroadApplicationViewSet, basename='study-abroad-application')
router.register(r'study-abroad-experiences', StudyAbroadExperienceViewSet, basename='study-abroad-experience')
router.register(r'study-abroad-resources', StudyAbroadResourceViewSet, basename='study-abroad-resource')
router.register(r'study-abroad-events', StudyAbroadEventViewSet, basename='study-abroad-event')
router.register(r'study-abroad-event-registrations', StudyAbroadEventRegistrationViewSet, basename='study-abroad-event-registration')

# Custom URL patterns for specific actions
urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Custom action URLs for better organization
    path('study-abroad-programs/active/', 
         StudyAbroadProgramViewSet.as_view({'get': 'active_programs'}), 
         name='study-abroad-programs-active'),
    
    path('study-abroad-programs/featured/', 
         StudyAbroadProgramViewSet.as_view({'get': 'featured_programs'}), 
         name='study-abroad-programs-featured'),
    
    path('study-abroad-programs/by-country/', 
         StudyAbroadProgramViewSet.as_view({'get': 'by_country'}), 
         name='study-abroad-programs-by-country'),
    
    path('study-abroad-programs/by-type/', 
         StudyAbroadProgramViewSet.as_view({'get': 'by_type'}), 
         name='study-abroad-programs-by-type'),
    
    path('study-abroad-applications/my-applications/', 
         StudyAbroadApplicationViewSet.as_view({'get': 'my_applications'}), 
         name='study-abroad-applications-my-applications'),
    
    path('study-abroad-applications/by-status/', 
         StudyAbroadApplicationViewSet.as_view({'get': 'by_status'}), 
         name='study-abroad-applications-by-status'),
    
    path('study-abroad-experiences/my-experiences/', 
         StudyAbroadExperienceViewSet.as_view({'get': 'my_experiences'}), 
         name='study-abroad-experiences-my-experiences'),
    
    path('study-abroad-experiences/approved/', 
         StudyAbroadExperienceViewSet.as_view({'get': 'approved_experiences'}), 
         name='study-abroad-experiences-approved'),
    
    path('study-abroad-experiences/featured/', 
         StudyAbroadExperienceViewSet.as_view({'get': 'featured_experiences'}), 
         name='study-abroad-experiences-featured'),
    
    path('study-abroad-resources/active/', 
         StudyAbroadResourceViewSet.as_view({'get': 'active_resources'}), 
         name='study-abroad-resources-active'),
    
    path('study-abroad-resources/featured/', 
         StudyAbroadResourceViewSet.as_view({'get': 'featured_resources'}), 
         name='study-abroad-resources-featured'),
    
    path('study-abroad-events/upcoming/', 
         StudyAbroadEventViewSet.as_view({'get': 'upcoming_events'}), 
         name='study-abroad-events-upcoming'),
    
    path('study-abroad-events/featured/', 
         StudyAbroadEventViewSet.as_view({'get': 'featured_events'}), 
         name='study-abroad-events-featured'),
    
    path('study-abroad-events/by-type/', 
         StudyAbroadEventViewSet.as_view({'get': 'by_type'}), 
         name='study-abroad-events-by-type'),
    
    path('study-abroad-event-registrations/my-registrations/', 
         StudyAbroadEventRegistrationViewSet.as_view({'get': 'my_registrations'}), 
         name='study-abroad-event-registrations-my-registrations'),
] 