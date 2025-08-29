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
    NotesCategory, NotesTopic, NotesModule, NotesVideo, 
    NotesMCQ, NotesMCQOption, NotesClinicalCase, 
    NotesQBank, NotesFlashCard, NotesStatistics
)
from .serializers import (
    NotesCategorySerializer, NotesFlashCardSerializer, NotesMCQSerializer, NotesTopicSerializer, NotesModuleSerializer,
    NotesStatisticsSerializer, TrackViewRequestSerializer, TrackMCQAttemptRequestSerializer,
    CategoriesResponseSerializer, TopicsResponseSerializer, ModulesResponseSerializer,
    StatisticsResponseSerializer, FeaturedContentResponseSerializer, VideoLectureSerializer,
    VideoLecturesResponseSerializer
)


@swagger_auto_schema(
    method='get',
    operation_description="Get video lectures for a specific topic",
    operation_summary="Get Video Lectures by Topic",
    manual_parameters=[
        openapi.Parameter(
            'topic_id',
            openapi.IN_PATH,
            description="ID of the topic",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Successfully retrieved video lectures",
            schema=VideoLecturesResponseSerializer,
            examples={
                "application/json": {
                    "status": "success",
                    "data": [
                        {
                            "id": 1,
                            "title": "Gametogenesis",
                            "doctor": "Dr. Sarah Johnson, MD",
                            "duration": "30 Min",
                            "thumbnailUrl": "https://example.com/thumbnail1.jpg",
                            "accessType": "free",
                            "videoId": "https://example.com/video1.mp4",
                            "description": "Comprehensive lecture on gametogenesis",
                            "views_count": 150,
                            "likes_count": 12,
                            "is_premium": False
                        }
                    ]
                }
            }
        ),
        404: openapi.Response(
            description="Topic not found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="Topic not found")
                }
            )
        ),
        500: openapi.Response(
            description="Internal server error",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="Internal server error")
                }
            )
        )
    },
    tags=['Notes']
)
@api_view(['GET'])
def video_lectures_view(request, topic_id):
    """
    Get video lectures for a specific topic.
    
    Returns a list of video lectures with all necessary fields for the frontend.
    """
    try:
        # Get the topic
        topic = NotesTopic.objects.get(id=topic_id, is_active=True)
        
        # Get video modules for this specific topic
        video_modules = NotesModule.objects.filter(
            topic=topic,
            module_type='video',
            is_active=True
        ).select_related('video').prefetch_related('topic')
        
        serializer = VideoLectureSerializer(video_modules, many=True)
        
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    except NotesTopic.DoesNotExist:
        return Response({'status': 'error', 'message': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error in video_lectures_view: {e}")
        return Response({'status': 'error', 'message': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='get',
    operation_description="Get all notes categories with their statistics",
    operation_summary="Get Notes Categories",
    responses={
        200: openapi.Response(
            description="Successfully retrieved categories",
            schema=CategoriesResponseSerializer,
            examples={
                "application/json": {
                    "status": "success",
                    "data": {
                        "video": {"topics": 23, "videos": 200},
                        "mcq": {"topics": 23, "modules": 230},
                        "clinical_case": {"topics": 23, "modules": 230},
                        "q_bank": {"topics": 23, "modules": 230},
                        "flash_card": {"topics": 23, "modules": 230}
                    }
                }
            }
        ),
        500: openapi.Response(
            description="Internal server error",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="Internal server error")
                }
            )
        )
    },
    tags=['Notes']
)
@api_view(['GET'])
def categories_view(request):
    """
    Get all notes categories with their statistics.
    
    Returns a dictionary with category names as keys and their statistics as values.
    Statistics include topics count and modules/videos count based on category type.
    """
    try:
        categories = NotesCategory.objects.filter(is_active=True)
        
        categories_data = {}
        for category in categories:
            # Get topics count
            topics_count = category.topics.filter(is_active=True).count()
            
            # Get modules/videos count based on category type
            if category.name == 'video':
                modules_count = category.topics.filter(is_active=True).aggregate(
                    total=Sum('videos_count')
                )['total'] or 0
            else:
                modules_count = category.topics.filter(is_active=True).aggregate(
                    total=Sum('modules_count')
                )['total'] or 0
            
            categories_data[category.name] = {
                'topics': topics_count,
                'modules': modules_count if category.name != 'video' else None,
                'videos': modules_count if category.name == 'video' else None,
            }
        
        # Ensure all categories exist in response
        expected_categories = ['video', 'mcq', 'clinical_case', 'q_bank', 'flash_card']
        for cat in expected_categories:
            if cat not in categories_data:
                categories_data[cat] = {
                    'topics': 0,
                    'modules': 0 if cat != 'video' else None,
                    'videos': 0 if cat == 'video' else None,
                }
        
        return Response({
            'status': 'success',
            'data': categories_data
        })
        
    except Exception as e:
        print(f"Error in categories_view: {e}")
        return Response({
            'status': 'error',
            'message': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='get',
    operation_description="Get topics for a specific category",
    operation_summary="Get Topics by Category",
    manual_parameters=[
        openapi.Parameter(
            'category_name',
            openapi.IN_PATH,
            description="Name of the category (video, mcq, clinical_case, q_bank, flash_card)",
            type=openapi.TYPE_STRING,
            required=True,
            enum=['video', 'mcq', 'clinical_case', 'q_bank', 'flash_card']
        )
    ],
    responses={
        200: openapi.Response(
            description="Successfully retrieved topics",
            schema=TopicsResponseSerializer,
            examples={
                "application/json": {
                    "status": "success",
                    "data": [
                        {
                            "id": 1,
                            "title": "Anatomy Basics",
                            "description": "Comprehensive anatomy basics content for medical students.",
                            "modules_count": 12,
                            "videos_count": 8,
                            "is_featured": True,
                            "order": 1
                        }
                    ]
                }
            }
        ),
        404: openapi.Response(
            description="Category not found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="Category not found")
                }
            )
        ),
        500: openapi.Response(
            description="Internal server error",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="Internal server error")
                }
            )
        )
    },
    tags=['Notes']
)
@api_view(['GET'])
def topics_view(request, category_name):
    """
    Get topics for a specific category.
    
    Args:
        category_name (str): Name of the category (video, mcq, clinical_case, q_bank, flash_card)
    
    Returns:
        List of topics with their details and statistics.
    """
    try:
        category = NotesCategory.objects.get(name=category_name, is_active=True)
        topics = category.topics.filter(is_active=True).order_by('order', 'title')
        
        topics_data = []
        for topic in topics:
            topic_data = {
                'id': topic.id,
                'title': topic.title,
                'description': topic.description,
                'modules_count': topic.modules_count,
                'videos_count': topic.videos_count,
                'is_featured': topic.is_featured,
            }
            topics_data.append(topic_data)
        
        return Response({
            'status': 'success',
            'data': topics_data
        })
        
    except NotesCategory.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Category not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='get',
    operation_description="Get modules for a specific topic",
    operation_summary="Get Modules by Topic",
    manual_parameters=[
        openapi.Parameter(
            'topic_id',
            openapi.IN_PATH,
            description="ID of the topic",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Successfully retrieved modules",
            schema=ModulesResponseSerializer,
            examples={
                "application/json": {
                    "status": "success",
                    "data": [
                        {
                            "id": 1,
                            "title": "Anatomy Basics Module 1",
                            "description": "Comprehensive video content for Anatomy Basics.",
                            "module_type": "video",
                            "duration_minutes": 45,
                            "views_count": 150,
                            "likes_count": 12,
                            "is_premium": False,
                            "video": {
                                "video_url": "https://example.com/videos/1.mp4",
                                "thumbnail_url": "https://example.com/thumbnails/1.jpg",
                                "duration_seconds": 2700,
                                "quality": "720p"
                            }
                        }
                    ]
                }
            }
        ),
        404: openapi.Response(
            description="Topic not found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="Topic not found")
                }
            )
        ),
        500: openapi.Response(
            description="Internal server error",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="Internal server error")
                }
            )
        )
    },
    tags=['Notes']
)
@api_view(['GET'])
def modules_view(request, topic_id):
    """
    Get modules for a specific topic.
    
    Args:
        topic_id (int): ID of the topic
    
    Returns:
        List of modules with their details and specific content based on module type.
    """
    try:
        topic = NotesTopic.objects.get(id=topic_id, is_active=True)
        modules = topic.modules.filter(is_active=True).order_by('order', 'title')
        
        modules_data = []
        for module in modules:
            module_data = {
                'id': module.id,
                'title': module.title,
                'description': module.description,
                'module_type': module.module_type,
                'duration_minutes': module.duration_minutes,
                'views_count': module.views_count,
                'likes_count': module.likes_count,
                'is_premium': module.is_premium,
            }
            
            # Add specific content data based on module type
            if module.module_type == 'video' and hasattr(module, 'video'):
                module_data['video_url'] = module.video.video_url
                module_data['thumbnail_url'] = module.video.thumbnail_url
                module_data['duration_seconds'] = module.video.duration_seconds
                module_data['quality'] = module.video.quality
                
            elif module.module_type == 'mcq' and hasattr(module, 'mcq'):
                module_data['question_text'] = module.mcq.question_text
                module_data['explanation'] = module.mcq.explanation
                module_data['options'] = [
                    {
                        'id': option.id,
                        'text': option.option_text,
                        'is_correct': option.is_correct
                    }
                    for option in module.mcq.options.all().order_by('order')
                ]
                
            elif module.module_type == 'clinical_case' and hasattr(module, 'clinical_case'):
                module_data['case_title'] = module.clinical_case.case_title
                module_data['patient_history'] = module.clinical_case.patient_history
                module_data['clinical_findings'] = module.clinical_case.clinical_findings
                module_data['diagnosis'] = module.clinical_case.diagnosis
                module_data['treatment'] = module.clinical_case.treatment
                
            elif module.module_type == 'q_bank' and hasattr(module, 'q_bank'):
                module_data['question_text'] = module.q_bank.question_text
                module_data['explanation'] = module.q_bank.explanation
                module_data['difficulty_level'] = module.q_bank.difficulty_level
                
            elif module.module_type == 'flash_card' and hasattr(module, 'flash_card'):
                module_data['front_text'] = module.flash_card.front_text
                module_data['back_text'] = module.flash_card.back_text
                module_data['category'] = module.flash_card.category
                module_data['mastery_level'] = module.flash_card.mastery_level
            
            modules_data.append(module_data)
        
        return Response({
            'status': 'success',
            'data': modules_data
        })
        
    except NotesTopic.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Topic not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='post',
    operation_description="Track module views for analytics",
    operation_summary="Track Module View",
    request_body=TrackViewRequestSerializer,
    responses={
        200: openapi.Response(
            description="View tracked successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="success"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="View tracked successfully")
                }
            )
        ),
        400: openapi.Response(
            description="Bad request",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="module_id is required")
                }
            )
        ),
        404: openapi.Response(
            description="Module not found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="Module not found")
                }
            )
        ),
        500: openapi.Response(
            description="Internal server error",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="Internal server error")
                }
            )
        )
    },
    tags=['Notes']
)
@api_view(['POST'])
def track_view(request):
    """
    Track module views for analytics.
    
    Args:
        module_id (int): ID of the module to track view
    
    Returns:
        Success message after tracking the view.
    """
    try:
        data = request.data
        module_id = data.get('module_id')
        
        if not module_id:
            return Response({
                'status': 'error',
                'message': 'module_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        module = NotesModule.objects.get(id=module_id)
        module.views_count += 1
        module.save()
        
        # Update video views if applicable
        if module.module_type == 'video' and hasattr(module, 'video'):
            module.video.views_count += 1
            module.video.save()
        
        # Update clinical case views if applicable
        elif module.module_type == 'clinical_case' and hasattr(module, 'clinical_case'):
            module.clinical_case.views_count += 1
            module.clinical_case.save()
        
        # Update flash card views if applicable
        elif module.module_type == 'flash_card' and hasattr(module, 'flash_card'):
            module.flash_card.views_count += 1
            module.flash_card.save()
        
        return Response({
            'status': 'success',
            'message': 'View tracked successfully'
        })
        
    except NotesModule.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Module not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='post',
    operation_description="Track MCQ attempts for analytics",
    operation_summary="Track MCQ Attempt",
    request_body=TrackMCQAttemptRequestSerializer,
    responses={
        200: openapi.Response(
            description="MCQ attempt tracked successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="success"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="MCQ attempt tracked successfully")
                }
            )
        ),
        400: openapi.Response(
            description="Bad request",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="mcq_id is required")
                }
            )
        ),
        404: openapi.Response(
            description="MCQ not found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="MCQ not found")
                }
            )
        ),
        500: openapi.Response(
            description="Internal server error",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="Internal server error")
                }
            )
        )
    },
    tags=['Notes']
)
@api_view(['POST'])
def track_mcq_attempt(request):
    """
    Track MCQ attempts for analytics.
    
    Args:
        mcq_id (int): ID of the MCQ question
        selected_option_id (int): ID of the selected option
        is_correct (bool): Whether the selected answer is correct
    
    Returns:
        Success message after tracking the attempt.
    """
    try:
        data = request.data
        mcq_id = data.get('mcq_id')
        selected_option_id = data.get('selected_option_id')
        is_correct = data.get('is_correct', False)
        
        if not mcq_id:
            return Response({
                'status': 'error',
                'message': 'mcq_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        mcq = NotesMCQ.objects.get(id=mcq_id)
        mcq.attempts_count += 1
        
        if is_correct:
            mcq.correct_answers_count += 1
        
        mcq.save()
        
        return Response({
            'status': 'success',
            'message': 'MCQ attempt tracked successfully'
        })
        
    except NotesMCQ.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'MCQ not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='get',
    operation_description="Get notes usage statistics",
    operation_summary="Get Notes Statistics",
    responses={
        200: openapi.Response(
            description="Successfully retrieved statistics",
            schema=StatisticsResponseSerializer,
            examples={
                "application/json": {
                    "status": "success",
                    "data": {
                        "date": "2024-01-15",
                        "total_views": 850,
                        "total_modules_accessed": 120,
                        "total_unique_users": 45,
                        "categories": {
                            "video": {"topics_count": 23, "modules_count": 0, "total_views": 250},
                            "mcq": {"topics_count": 23, "modules_count": 230, "total_views": 300},
                            "clinical_case": {"topics_count": 23, "modules_count": 230, "total_views": 150},
                            "q_bank": {"topics_count": 23, "modules_count": 230, "total_views": 100},
                            "flash_card": {"topics_count": 23, "modules_count": 230, "total_views": 50}
                        }
                    }
                }
            }
        ),
        500: openapi.Response(
            description="Internal server error",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="Internal server error")
                }
            )
        )
    },
    tags=['Notes']
)
@api_view(['GET'])
def statistics_view(request):
    """
    Get notes usage statistics.
    
    Returns:
        Comprehensive statistics including total views, modules accessed, 
        unique users, and category-wise breakdown.
    """
    try:
        # Get today's statistics
        today = date.today()
        stats, created = NotesStatistics.objects.get_or_create(date=today)
        
        # Get category statistics
        categories_stats = {}
        for category in NotesCategory.objects.filter(is_active=True):
            topics_count = category.topics.filter(is_active=True).count()
            
            if category.name == 'video':
                modules_count = category.topics.filter(is_active=True).aggregate(
                    total=Sum('videos_count')
                )['total'] or 0
            else:
                modules_count = category.topics.filter(is_active=True).aggregate(
                    total=Sum('modules_count')
                )['total'] or 0
            
            categories_stats[category.name] = {
                'topics_count': topics_count,
                'modules_count': modules_count,
                'total_views': stats.video_views if category.name == 'video' else 
                              stats.mcq_attempts if category.name == 'mcq' else
                              stats.clinical_case_views if category.name == 'clinical_case' else
                              stats.q_bank_attempts if category.name == 'q_bank' else
                              stats.flash_card_views,
            }
        
        return Response({
            'status': 'success',
            'data': {
                'date': today.isoformat(),
                'total_views': stats.total_views,
                'total_modules_accessed': stats.total_modules_accessed,
                'total_unique_users': stats.total_unique_users,
                'categories': categories_stats
            }
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='get',
    operation_description="Get featured content across all categories",
    operation_summary="Get Featured Content",
    responses={
        200: openapi.Response(
            description="Successfully retrieved featured content",
            schema=FeaturedContentResponseSerializer,
            examples={
                "application/json": {
                    "status": "success",
                    "data": {
                        "video": {
                            "topics": [
                                {
                                    "id": 1,
                                    "title": "Anatomy Basics",
                                    "description": "Comprehensive anatomy basics content for medical students.",
                                    "modules_count": 12,
                                    "videos_count": 8,
                                    "is_featured": True
                                }
                            ]
                        },
                        "mcq": {
                            "topics": [
                                {
                                    "id": 24,
                                    "title": "Anatomy MCQs",
                                    "description": "Comprehensive anatomy mcqs content for medical students.",
                                    "modules_count": 15,
                                    "videos_count": 0,
                                    "is_featured": True
                                }
                            ]
                        }
                    }
                }
            }
        ),
        500: openapi.Response(
            description="Internal server error",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example="Internal server error")
                }
            )
        )
    },
    tags=['Notes']
)
@api_view(['GET'])
def featured_content_view(request):
    """
    Get featured content across all categories.
    
    Returns:
        Dictionary with category names as keys and lists of featured topics as values.
    """
    try:
        featured_data = {}
        
        for category in NotesCategory.objects.filter(is_active=True):
            # Get featured topics
            featured_topics = category.topics.filter(is_active=True, is_featured=True)[:3]
            topics_data = []
            
            for topic in featured_topics:
                topic_data = {
                    'id': topic.id,
                    'title': topic.title,
                    'description': topic.description,
                    'modules_count': topic.modules_count,
                    'videos_count': topic.videos_count,
                }
                topics_data.append(topic_data)
            
            featured_data[category.name] = {
                'topics': topics_data
            }
        
        return Response({
            'status': 'success',
            'data': featured_data
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


# -------------------------- new part

class VideoLectureListView(APIView):
    """
    API view to fetch all NotesVideo objects along with related NotesModule data.
    Returns JSON response for frontend consumption.
    """
    
    def get(self, request):
        try:
            # Fetch all NotesVideo objects, including related module to reduce DB queries
            videos = NotesVideo.objects.select_related('module').all()
            
            # Serialize the queryset
            serializer = VideoLectureSerializer(videos, many=True)
            
            # Return JSON response
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            # In case of any error
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
@api_view(['GET'])
def get_all_mcqs(request):
    """
    Fetch all MCQs along with their module info and options in JSON format.
    """
    try:
        mcqs = NotesMCQ.objects.all().prefetch_related('options', 'module')
        serializer = NotesMCQSerializer(mcqs, many=True)
        return Response({
            "status": "success",
            "count": mcqs.count(),
            "data": serializer.data
        })
    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)
    

@api_view(['GET'])
def get_all_clinical_cases(request):
    """
    Fetch all clinical cases along with their module info and count.
    """
    try:
        # Fetch all clinical cases with related module
        clinical_cases = NotesClinicalCase.objects.select_related('module').all()

        # Prepare a dict to group by module
        modules_dict = {}

        for case in clinical_cases:
            module_id = case.module.id
            if module_id not in modules_dict:
                modules_dict[module_id] = {
                    "module_id": module_id,
                    "module_title": case.module.title,
                    "module_description": case.module.description,
                    "clinical_cases_count": 0,
                    "clinical_cases": []
                }

            modules_dict[module_id]["clinical_cases_count"] += 1
            modules_dict[module_id]["clinical_cases"].append({
                "id": case.id,
                "case_title": case.case_title,
                "patient_history": case.patient_history,
                "clinical_findings": case.clinical_findings,
                "diagnosis": case.diagnosis,
                "treatment": case.treatment,
                "views_count": case.views_count
            })

        response_data = list(modules_dict.values())

        return Response({
            "status": "success",
            "count": len(response_data),
            "data": response_data
        })

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)
    

@api_view(['GET'])
def get_all_qbank(request):
    """
    Fetch all Q-Bank questions grouped by module, including module title,
    description, and count of questions per module.
    """
    try:
        # Fetch all Q-Bank entries and prefetch related module
        qbanks = NotesQBank.objects.select_related('module').all()

        # Group Q-Bank questions by module
        modules_map = {}
        for q in qbanks:
            module = q.module
            module_id = module.id
            if module_id not in modules_map:
                modules_map[module_id] = {
                    "module_id": module_id,
                    "module_title": module.title,
                    "module_description": module.description,
                    "questions_count": 0,
                    "questions": []
                }
            
            modules_map[module_id]["questions_count"] += 1
            modules_map[module_id]["questions"].append({
                "id": q.id,
                "question_text": q.question_text,
                "explanation": q.explanation,
                "difficulty_level": q.difficulty_level,
                "attempts_count": q.attempts_count,
                "correct_answers_count": q.correct_answers_count
            })

        # Convert to list for JSON response
        modules_list = list(modules_map.values())

        return Response({
            "status": "success",
            "count": len(modules_list),
            "data": modules_list
        })

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)
    

@api_view(['GET'])
def get_all_flashcards(request):
    """
    Fetch all Flash Cards grouped by their module in JSON format.
    """
    try:
        # Fetch all flash cards with related module to avoid N+1 queries
        flashcards = NotesFlashCard.objects.select_related('module').all()

        # Group flashcards by module
        modules_map = {}
        for fc in flashcards:
            module = fc.module
            if module.id not in modules_map:
                modules_map[module.id] = {
                    'module_id': module.id,
                    'module_title': module.title,
                    'module_description': module.description,
                    'flash_cards_count': 1,
                    'flash_cards': [NotesFlashCardSerializer(fc).data]
                }
            else:
                modules_map[module.id]['flash_cards_count'] += 1
                modules_map[module.id]['flash_cards'].append(NotesFlashCardSerializer(fc).data)

        # Prepare final response
        return Response({
            "status": "success",
            "count": len(modules_map),
            "data": list(modules_map.values())
        })

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)