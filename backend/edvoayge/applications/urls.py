"""
URL patterns for applications app.
Defines API endpoints for application management and related data.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import (
    ApplicationViewSet, ApplicationDocumentViewSet, ApplicationStatusViewSet,
    ApplicationInterviewViewSet, ApplicationFeeViewSet, ApplicationCommunicationViewSet
)

# Create main router for applications
router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='application')

# Create nested routers for related data
application_router = routers.NestedDefaultRouter(router, r'applications', lookup='application')
application_router.register(r'documents', ApplicationDocumentViewSet, basename='application-document')
application_router.register(r'status', ApplicationStatusViewSet, basename='application-status')
application_router.register(r'interviews', ApplicationInterviewViewSet, basename='application-interview')
application_router.register(r'fees', ApplicationFeeViewSet, basename='application-fee')
application_router.register(r'communications', ApplicationCommunicationViewSet, basename='application-communication')

app_name = 'applications'

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    path('', include(application_router.urls)),
] 