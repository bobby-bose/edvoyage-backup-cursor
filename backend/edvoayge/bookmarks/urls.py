from django.urls import path
from .views import (
    FavouriteUniversityView, 
    FavouriteCourseView,
    AddFavouriteUniversity, 
    AddFavouriteCourse
)

urlpatterns = [
    # Enhanced endpoints
    path('universities/', FavouriteUniversityView.as_view(), name='favourite-universities'),
    path('courses/', FavouriteCourseView.as_view(), name='favourite-courses'),
    
    # Legacy endpoints for backward compatibility
    path('add-favourite-university/', AddFavouriteUniversity.as_view(), name='add-favourite-university'),
    path('add-favourite-course/', AddFavouriteCourse.as_view(), name='add-favourite-course'),
]