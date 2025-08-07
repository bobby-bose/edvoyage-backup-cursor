from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import SimpleEducation, SimpleWork, SimpleSocial
from .serializers import SimpleEducationSerializer, SimpleWorkSerializer, SimpleSocialSerializer

class SimpleEducationViewSet(viewsets.ModelViewSet):
    """Simple education viewset"""
    serializer_class = SimpleEducationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get education records for current user"""
        return SimpleEducation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set user to current user when creating"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_education(self, request):
        """Get current user's education"""
        education = self.get_queryset().first()
        if education:
            serializer = self.get_serializer(education)
            return Response(serializer.data)
        else:
            return Response({'message': 'No education record found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def update_education(self, request):
        """Update or create education record"""
        education = self.get_queryset().first()
        
        if education:
            # Update existing record
            serializer = self.get_serializer(education, data=request.data, partial=True)
        else:
            # Create new record
            serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SimpleWorkViewSet(viewsets.ModelViewSet):
    """Simple work viewset"""
    serializer_class = SimpleWorkSerializer
    # Removed permission_classes = [IsAuthenticated] - no authentication required
    
    def get_queryset(self):
        """Get work records for current user"""
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            return SimpleWork.objects.filter(user=self.request.user)
        else:
            # Return all work records if no user is authenticated
            return SimpleWork.objects.all()
    
    def perform_create(self, serializer):
        """Set user to current user when creating"""
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            # Create without user for now
            serializer.save()
    
    @action(detail=False, methods=['get'])
    def my_work(self, request):
        """Get current user's work"""
        work = self.get_queryset().first()
        if work:
            serializer = self.get_serializer(work)
            return Response(serializer.data)
        else:
            return Response({'message': 'No work record found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def update_work(self, request):
        """Update or create work record"""
        work = self.get_queryset().first()
        
        if work:
            # Update existing record
            serializer = self.get_serializer(work, data=request.data, partial=True)
        else:
            # Create new record
            serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            if hasattr(request, 'user') and request.user.is_authenticated:
                serializer.save(user=request.user)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SimpleSocialViewSet(viewsets.ModelViewSet):
    """Simple social viewset"""
    serializer_class = SimpleSocialSerializer
    # Removed permission_classes = [IsAuthenticated] - no authentication required
    
    def get_queryset(self):
        """Get social records for current user"""
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            return SimpleSocial.objects.filter(user=self.request.user)
        else:
            # Return all social records if no user is authenticated
            return SimpleSocial.objects.all()
    
    def perform_create(self, serializer):
        """Set user to current user when creating"""
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            # Create without user for now
            serializer.save()
    
    @action(detail=False, methods=['get'])
    def my_social(self, request):
        """Get current user's social links"""
        social = self.get_queryset().first()
        if social:
            serializer = self.get_serializer(social)
            return Response(serializer.data)
        else:
            return Response({'message': 'No social record found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def update_social(self, request):
        """Update or create social record"""
        social = self.get_queryset().first()
        
        if social:
            # Update existing record
            serializer = self.get_serializer(social, data=request.data, partial=True)
        else:
            # Create new record
            serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            if hasattr(request, 'user') and request.user.is_authenticated:
                serializer.save(user=request.user)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
