from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SimpleEducationViewSet, SimpleWorkViewSet, SimpleSocialViewSet

# Create router for ViewSets
router = DefaultRouter()
router.register(r'education', SimpleEducationViewSet, basename='simple-education')
router.register(r'work', SimpleWorkViewSet, basename='simple-work')
router.register(r'social', SimpleSocialViewSet, basename='simple-social')

app_name = 'simple_education'

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
] 