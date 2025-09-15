from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import date, timedelta
import json

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# import API_VIEW
from rest_framework.views import APIView
from .models import (
    NotesCategory,  NotesVideoMain, NotesVideoSub,NotesVideoPlayer
)
from .serializers import (
    NotesCategorySerializer, NotesVideoMainSerializer, NotesVideoSubSerializer, NotesVideoPlayerSerializer
)

# -------------------------- new part


# 1. Total count of sub topics and videos under category "video"
@api_view(['GET'])
def video_overview(request):
    try:
        category = NotesCategory.objects.get(name="video")
    except NotesCategory.DoesNotExist:
        return Response({"error": "Video category not found"}, status=404)

    total_topics = NotesVideoMain.objects.filter(category=category).count()
    total_videos = NotesVideoSub.objects.filter(title__category=category).count()

    return Response({
        "category": category.name,
        "total_topics": total_topics,
        "total_videos": total_videos
    })


# 2. Count of videos under each sub-topic
@api_view(['GET'])
def video_topic_breakdown(request):
    topics = NotesVideoMain.objects.all()
    data = []
    for topic in topics:
        video_count = NotesVideoSub.objects.filter(title=topic).count()
        data.append({
            "topic": topic.title,
            "videos": video_count
        })
    return Response(data)


# 3. Details of each video
@api_view(['GET'])
def video_details(request):
    videos = NotesVideoSub.objects.all()
    serializer = NotesVideoSubSerializer(videos, many=True, context={'request': request})
    return Response(serializer.data)


# 4. Video URLs (logo file URL or placeholder if missing)
@api_view(['GET'])
def video_urls(request):
    videos = NotesVideoSub.objects.all()
    data = []
    for video in videos:
        data.append({
            "id": video.id,
            "title": video.title.title,
            "video_url": request.build_absolute_uri(video.logo.url) if video.logo else None
        })
    return Response(data)



     