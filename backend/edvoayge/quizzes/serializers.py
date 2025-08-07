from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Quiz, QuizCategory, Question, Option, QuizAttempt, 
    QuizResult, QuizAnalytics, QuizShare, QuizTimer
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user information"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class QuizCategorySerializer(serializers.ModelSerializer):
    """Serializer for quiz categories"""
    quiz_count = serializers.ReadOnlyField()
    
    class Meta:
        model = QuizCategory
        fields = [
            'id', 'name', 'description', 'color', 'icon', 
            'is_active', 'quiz_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class QuizCategoryListSerializer(serializers.ModelSerializer):
    """List serializer for quiz categories with minimal data"""
    quiz_count = serializers.ReadOnlyField()
    
    class Meta:
        model = QuizCategory
        fields = ['id', 'name', 'color', 'icon', 'quiz_count', 'is_active']

class OptionSerializer(serializers.ModelSerializer):
    """Serializer for question options"""
    class Meta:
        model = Option
        fields = ['id', 'option_text', 'is_correct', 'order', 'created_at']
        read_only_fields = ['created_at']

class OptionListSerializer(serializers.ModelSerializer):
    """List serializer for options without correct answer"""
    class Meta:
        model = Option
        fields = ['id', 'option_text', 'order']

class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for questions with options"""
    options = OptionSerializer(many=True, read_only=True)
    correct_options = serializers.ReadOnlyField()
    
    class Meta:
        model = Question
        fields = [
            'id', 'question_text', 'question_type', 'points', 'order',
            'explanation', 'is_active', 'options', 'correct_options',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class QuestionListSerializer(serializers.ModelSerializer):
    """List serializer for questions with minimal data"""
    options = OptionListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'points', 'order', 'options']

class QuizSerializer(serializers.ModelSerializer):
    """Full serializer for quizzes"""
    category = QuizCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    creator = UserSerializer(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    question_count = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'category', 'category_id', 'creator',
            'time_limit', 'passing_score', 'max_attempts', 'difficulty',
            'status', 'is_public', 'is_featured', 'total_attempts',
            'average_score', 'completion_rate', 'question_count', 'is_active',
            'questions', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = [
            'creator', 'total_attempts', 'average_score', 'completion_rate',
            'created_at', 'updated_at', 'published_at'
        ]

class QuizListSerializer(serializers.ModelSerializer):
    """List serializer for quizzes with minimal data"""
    category = QuizCategoryListSerializer(read_only=True)
    creator = UserSerializer(read_only=True)
    question_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'category', 'creator',
            'time_limit', 'difficulty', 'status', 'is_public', 'is_featured',
            'total_attempts', 'average_score', 'question_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'creator', 'total_attempts', 'average_score', 'created_at', 'updated_at'
        ]

class QuizCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating quizzes"""
    category_id = serializers.IntegerField()
    
    class Meta:
        model = Quiz
        fields = [
            'title', 'description', 'category_id', 'time_limit',
            'passing_score', 'max_attempts', 'difficulty', 'status',
            'is_public', 'is_featured'
        ]

    def validate_category_id(self, value):
        """Validate that category exists"""
        try:
            QuizCategory.objects.get(id=value)
        except QuizCategory.DoesNotExist:
            raise serializers.ValidationError("Category does not exist")
        return value

    def create(self, validated_data):
        """Create quiz with current user as creator"""
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

class QuizUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating quizzes"""
    category_id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Quiz
        fields = [
            'title', 'description', 'category_id', 'time_limit',
            'passing_score', 'max_attempts', 'difficulty', 'status',
            'is_public', 'is_featured'
        ]

    def validate_category_id(self, value):
        """Validate that category exists"""
        try:
            QuizCategory.objects.get(id=value)
        except QuizCategory.DoesNotExist:
            raise serializers.ValidationError("Category does not exist")
        return value

class QuizAttemptSerializer(serializers.ModelSerializer):
    """Serializer for quiz attempts"""
    quiz = QuizListSerializer(read_only=True)
    quiz_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    is_passed = serializers.ReadOnlyField()
    
    class Meta:
        model = QuizAttempt
        fields = [
            'id', 'quiz', 'quiz_id', 'user', 'status', 'score', 'percentage',
            'passed', 'started_at', 'completed_at', 'time_taken',
            'questions_attempted', 'questions_correct', 'is_passed',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'user', 'score', 'percentage', 'passed', 'completed_at',
            'time_taken', 'questions_attempted', 'questions_correct',
            'created_at', 'updated_at'
        ]

class QuizAttemptCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating quiz attempts"""
    quiz_id = serializers.IntegerField()
    
    class Meta:
        model = QuizAttempt
        fields = ['quiz_id']

    def validate_quiz_id(self, value):
        """Validate quiz exists and user can attempt it"""
        try:
            quiz = Quiz.objects.get(id=value)
        except Quiz.DoesNotExist:
            raise serializers.ValidationError("Quiz does not exist")
        
        # Check if quiz is active
        if not quiz.is_active:
            raise serializers.ValidationError("Quiz is not available")
        
        # Check attempt limit
        user = self.context['request'].user
        attempts_count = QuizAttempt.objects.filter(quiz=quiz, user=user).count()
        if attempts_count >= quiz.max_attempts:
            raise serializers.ValidationError(f"Maximum attempts ({quiz.max_attempts}) reached")
        
        return value

    def create(self, validated_data):
        """Create attempt with current user"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class QuizResultSerializer(serializers.ModelSerializer):
    """Serializer for quiz results"""
    attempt = QuizAttemptSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)
    
    class Meta:
        model = QuizResult
        fields = [
            'id', 'attempt', 'question', 'user_answer', 'is_correct',
            'points_earned', 'time_taken', 'feedback', 'explanation_shown',
            'created_at'
        ]
        read_only_fields = ['created_at']

class QuizAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for quiz analytics"""
    quiz = QuizListSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = QuizAnalytics
        fields = [
            'id', 'quiz', 'user', 'action_type', 'ip_address',
            'user_agent', 'referrer', 'session_id', 'created_at'
        ]
        read_only_fields = ['created_at']

class QuizShareSerializer(serializers.ModelSerializer):
    """Serializer for quiz sharing"""
    quiz = QuizListSerializer(read_only=True)
    shared_by = UserSerializer(read_only=True)
    shared_with = UserSerializer(read_only=True)
    
    class Meta:
        model = QuizShare
        fields = [
            'id', 'quiz', 'shared_by', 'shared_with', 'share_type',
            'message', 'share_url', 'is_viewed', 'viewed_at', 'created_at'
        ]
        read_only_fields = ['shared_by', 'share_url', 'is_viewed', 'viewed_at', 'created_at']

class QuizShareCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating quiz shares"""
    quiz_id = serializers.IntegerField()
    shared_with_id = serializers.IntegerField(required=False)
    
    class Meta:
        model = QuizShare
        fields = ['quiz_id', 'shared_with_id', 'share_type', 'message']

    def validate_quiz_id(self, value):
        """Validate quiz exists"""
        try:
            Quiz.objects.get(id=value)
        except Quiz.DoesNotExist:
            raise serializers.ValidationError("Quiz does not exist")
        return value

    def validate_shared_with_id(self, value):
        """Validate user exists"""
        if value:
            try:
                User.objects.get(id=value)
            except User.DoesNotExist:
                raise serializers.ValidationError("User does not exist")
        return value

    def create(self, validated_data):
        """Create share with current user as shared_by"""
        validated_data['shared_by'] = self.context['request'].user
        return super().create(validated_data)

class QuizTimerSerializer(serializers.ModelSerializer):
    """Serializer for quiz timers"""
    attempt = QuizAttemptSerializer(read_only=True)
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = QuizTimer
        fields = [
            'id', 'attempt', 'time_limit', 'time_remaining', 'is_paused',
            'paused_at', 'resumed_at', 'total_pause_time', 'is_expired',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class QuizSearchSerializer(serializers.Serializer):
    """Serializer for quiz search"""
    q = serializers.CharField(max_length=200, required=False)
    category = serializers.IntegerField(required=False)
    difficulty = serializers.ChoiceField(choices=Quiz.DIFFICULTY_CHOICES, required=False)
    status = serializers.ChoiceField(choices=Quiz.STATUS_CHOICES, required=False)
    is_public = serializers.BooleanField(required=False)
    is_featured = serializers.BooleanField(required=False)
    time_limit_min = serializers.IntegerField(required=False, min_value=0)
    time_limit_max = serializers.IntegerField(required=False, min_value=0)

class QuizStatisticsSerializer(serializers.Serializer):
    """Serializer for quiz statistics"""
    total_quizzes = serializers.IntegerField()
    total_attempts = serializers.IntegerField()
    average_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    completion_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    popular_quizzes = QuizListSerializer(many=True)
    recent_quizzes = QuizListSerializer(many=True)
    category_stats = serializers.ListField()

class QuizAttemptSubmitSerializer(serializers.Serializer):
    """Serializer for submitting quiz attempts"""
    answers = serializers.DictField()
    
    def validate_answers(self, value):
        """Validate answers format"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Answers must be a dictionary")
        return value

class QuizExportSerializer(serializers.Serializer):
    """Serializer for quiz export"""
    format = serializers.ChoiceField(choices=['json', 'csv', 'pdf'], default='json')
    include_questions = serializers.BooleanField(default=True)
    include_attempts = serializers.BooleanField(default=False)
    include_analytics = serializers.BooleanField(default=False)

class QuizImportSerializer(serializers.Serializer):
    """Serializer for quiz import"""
    file = serializers.FileField()
    category_id = serializers.IntegerField(required=False)
    overwrite = serializers.BooleanField(default=False)

class QuizBulkActionSerializer(serializers.Serializer):
    """Serializer for bulk quiz actions"""
    quiz_ids = serializers.ListField(child=serializers.IntegerField())
    action = serializers.ChoiceField(choices=['publish', 'archive', 'delete', 'feature', 'unfeature']) 