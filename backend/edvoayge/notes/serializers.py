from rest_framework import serializers
from .models import (
    NotesCategory, NotesTopic, NotesModule, NotesVideo, 
    NotesMCQ, NotesMCQOption, NotesClinicalCase, 
    NotesQBank, NotesFlashCard, NotesStatistics
)


class VideoLectureSerializer(serializers.ModelSerializer):
    """
    Serializer for video lectures that maps to frontend requirements.
    """
    # Map backend fields to frontend requirements
    doctor = serializers.CharField(source='instructor', read_only=True)
    duration = serializers.SerializerMethodField()
    thumbnailUrl = serializers.CharField(source='video.thumbnail_url', read_only=True)
    accessType = serializers.CharField(source='access_type', read_only=True)
    videoId = serializers.CharField(source='video.video_url', read_only=True)
    
    class Meta:
        model = NotesModule
        fields = [
            'id', 'title', 'doctor', 'duration', 'thumbnailUrl', 
            'accessType', 'videoId', 'description', 'views_count', 
            'likes_count', 'is_premium'
        ]
    
    def get_duration(self, obj):
        """Convert duration_minutes to frontend format."""
        if obj.duration_minutes:
            return f"{obj.duration_minutes} Min"
        return "0 Min"


class NotesMCQOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesMCQOption
        fields = ['id', 'option_text', 'is_correct', 'order']


class NotesMCQSerializer(serializers.ModelSerializer):
    options = NotesMCQOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = NotesMCQ
        fields = ['id', 'question_text', 'explanation', 'attempts_count', 'correct_answers_count', 'options']


class NotesVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesVideo
        fields = ['id', 'video_url', 'thumbnail_url', 'duration_seconds', 'quality', 'views_count', 'likes_count']


class NotesClinicalCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesClinicalCase
        fields = ['id', 'case_title', 'patient_history', 'clinical_findings', 'diagnosis', 'treatment', 'views_count']


class NotesQBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesQBank
        fields = ['id', 'question_text', 'explanation', 'difficulty_level', 'attempts_count', 'correct_answers_count']


class NotesFlashCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesFlashCard
        fields = ['id', 'front_text', 'back_text', 'category', 'views_count', 'mastery_level']


class NotesModuleSerializer(serializers.ModelSerializer):
    video = NotesVideoSerializer(read_only=True)
    mcq = NotesMCQSerializer(read_only=True)
    clinical_case = NotesClinicalCaseSerializer(read_only=True)
    q_bank = NotesQBankSerializer(read_only=True)
    flash_card = NotesFlashCardSerializer(read_only=True)
    
    class Meta:
        model = NotesModule
        fields = [
            'id', 'title', 'module_type', 'description', 'content_url', 
            'duration_minutes', 'views_count', 'likes_count', 'is_active', 
            'is_premium', 'order', 'video', 'mcq', 'clinical_case', 
            'q_bank', 'flash_card', 'instructor', 'access_type'
        ]


class NotesTopicSerializer(serializers.ModelSerializer):
    modules = NotesModuleSerializer(many=True, read_only=True)
    
    class Meta:
        model = NotesTopic
        fields = [
            'id', 'title', 'description', 'modules_count', 'videos_count',
            'is_active', 'is_featured', 'order', 'modules'
        ]


class NotesCategorySerializer(serializers.ModelSerializer):
    topics = NotesTopicSerializer(many=True, read_only=True)
    
    class Meta:
        model = NotesCategory
        fields = [
            'id', 'name', 'display_name', 'description', 'topics_count',
            'modules_count', 'videos_count', 'is_active', 'is_featured',
            'topics'
        ]


class NotesStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesStatistics
        fields = [
            'id', 'date', 'total_views', 'total_modules_accessed', 
            'total_unique_users', 'video_views', 'mcq_attempts', 
            'clinical_case_views', 'q_bank_attempts', 'flash_card_views'
        ]


# Request/Response serializers for API documentation
class TrackViewRequestSerializer(serializers.Serializer):
    module_id = serializers.IntegerField(help_text="ID of the module to track view")


class TrackMCQAttemptRequestSerializer(serializers.Serializer):
    mcq_id = serializers.IntegerField(help_text="ID of the MCQ question")
    selected_option_id = serializers.IntegerField(help_text="ID of the selected option")
    is_correct = serializers.BooleanField(help_text="Whether the selected answer is correct")


# Response serializers for API documentation
class CategoriesResponseSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="Response status")
    data = serializers.DictField(help_text="Categories data with counts")


class TopicsResponseSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="Response status")
    data = serializers.ListField(help_text="List of topics")


class ModulesResponseSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="Response status")
    data = serializers.ListField(help_text="List of modules")


class StatisticsResponseSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="Response status")
    data = serializers.DictField(help_text="Statistics data")


class FeaturedContentResponseSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="Response status")
    data = serializers.DictField(help_text="Featured content data")


class VideoLecturesResponseSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="Response status")
    data = serializers.ListField(help_text="List of video lectures") 