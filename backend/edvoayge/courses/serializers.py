"""
Course serializers for EdVoyage API.
Handles data serialization for course-related endpoints.
"""

from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from .models import (
    Course, Subject, CourseSubject, FeeStructure, 
    CourseRequirement, CourseApplication, CourseRating
)


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer for Subject model."""
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'description', 'credits', 'is_core', 'created_at']
        read_only_fields = ['id', 'created_at']


class CourseSubjectSerializer(serializers.ModelSerializer):
    """Serializer for Course-Subject relationship."""
    
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = CourseSubject
        fields = ['id', 'subject', 'subject_id', 'semester', 'is_optional']
        read_only_fields = ['id']


class FeeStructureSerializer(serializers.ModelSerializer):
    """Serializer for detailed fee structure."""
    
    total_fees = serializers.ReadOnlyField()
    
    class Meta:
        model = FeeStructure
        fields = [
            'id', 'tuition_fee', 'tuition_fee_per_semester', 'accommodation_fee',
            'meal_plan_fee', 'transportation_fee', 'health_insurance_fee',
            'books_materials_fee', 'other_fees', 'currency', 'payment_terms',
            'total_fees', 'created_at'
        ]
        read_only_fields = ['id', 'total_fees', 'created_at']


class CourseRequirementSerializer(serializers.ModelSerializer):
    """Serializer for course requirements."""
    
    class Meta:
        model = CourseRequirement
        fields = [
            'id', 'requirement_type', 'title', 'description', 
            'is_mandatory', 'order', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CourseRatingSerializer(serializers.ModelSerializer):
    """Serializer for course ratings and reviews."""
    
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = CourseRating
        fields = [
            'id', 'rating', 'review', 'is_verified', 'user_name', 
            'user_email', 'created_at'
        ]
        read_only_fields = ['id', 'is_verified', 'user_name', 'user_email', 'created_at']
    
    def validate_rating(self, value):
        """Validate rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    
    def validate(self, data):
        """Validate that user hasn't already rated this course."""
        user = self.context['request'].user
        course = data.get('course')
        
        if CourseRating.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("You have already rated this course.")
        
        return data


class CourseListSerializer(serializers.ModelSerializer):
    """Minimal serializer for course listing."""
    
    university_name = serializers.CharField(source='university.name', read_only=True)
    university_country = serializers.CharField(source='university.country', read_only=True)
    average_rating = serializers.ReadOnlyField()
    total_applications = serializers.ReadOnlyField()
    subjects_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'name', 'code', 'short_description', 'university_name', 
            'university_country', 'level', 'duration', 'tuition_fee', 'currency',
            'average_rating', 'total_applications', 'subjects_count', 'is_featured',
            'is_popular', 'status', 'image', 'created_at'
        ]
        read_only_fields = ['id', 'average_rating', 'total_applications', 'subjects_count', 'created_at']
    
    def get_subjects_count(self, obj):
        """Get count of subjects for this course."""
        return obj.subjects.count()


class CourseDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for course information."""
    
    university_name = serializers.CharField(source='university.name', read_only=True)
    university_country = serializers.CharField(source='university.country', read_only=True)
    university_city = serializers.CharField(source='university.city', read_only=True)
    university_website = serializers.CharField(source='university.website', read_only=True)
    
    subjects = SubjectSerializer(many=True, read_only=True)
    fee_structure = FeeStructureSerializer(read_only=True)
    requirements = CourseRequirementSerializer(many=True, read_only=True)
    ratings = CourseRatingSerializer(many=True, read_only=True)
    
    average_rating = serializers.ReadOnlyField()
    total_applications = serializers.ReadOnlyField()
    total_ratings = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'name', 'code', 'description', 'short_description',
            'university_name', 'university_country', 'university_city', 'university_website',
            'level', 'duration', 'credits', 'subjects', 'tuition_fee', 'currency',
            'minimum_gpa', 'language_requirements', 'fee_structure', 'requirements',
            'ratings', 'average_rating', 'total_applications', 'total_ratings',
            'is_featured', 'is_popular', 'status', 'image', 'brochure',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'average_rating', 'total_applications', 'total_ratings',
            'created_at', 'updated_at'
        ]
    
    def get_total_ratings(self, obj):
        """Get total number of ratings for this course."""
        return obj.ratings.count()


class CourseCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new courses."""
    
    class Meta:
        model = Course
        fields = [
            'name', 'code', 'description', 'short_description', 'university',
            'level', 'duration', 'credits', 'tuition_fee', 'currency',
            'minimum_gpa', 'language_requirements', 'is_featured', 'is_popular',
            'status', 'image', 'brochure'
        ]
    
    def validate_code(self, value):
        """Validate course code is unique."""
        if Course.objects.filter(code=value).exists():
            raise serializers.ValidationError("Course code must be unique.")
        return value
    
    def validate_tuition_fee(self, value):
        """Validate tuition fee is positive."""
        if value <= 0:
            raise serializers.ValidationError("Tuition fee must be positive.")
        return value


class CourseUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating existing courses."""
    
    class Meta:
        model = Course
        fields = [
            'name', 'description', 'short_description', 'level', 'duration',
            'credits', 'tuition_fee', 'currency', 'minimum_gpa', 
            'language_requirements', 'is_featured', 'is_popular', 'status',
            'image', 'brochure'
        ]


class CourseApplicationSerializer(serializers.ModelSerializer):
    """Serializer for course applications."""
    
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    university_name = serializers.CharField(source='course.university.name', read_only=True)
    
    class Meta:
        model = CourseApplication
        fields = [
            'id', 'user_name', 'user_email', 'course_name', 'university_name',
            'status', 'personal_statement', 'expected_start_date', 'documents',
            'review_notes', 'reviewed_by', 'reviewed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user_name', 'user_email', 'course_name', 'university_name',
            'reviewed_by', 'reviewed_at', 'created_at', 'updated_at'
        ]
    
    def validate_expected_start_date(self, value):
        """Validate expected start date is in the future."""
        from django.utils import timezone
        if value and value <= timezone.now().date():
            raise serializers.ValidationError("Expected start date must be in the future.")
        return value


class CourseApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating course applications."""
    
    class Meta:
        model = CourseApplication
        fields = [
            'course', 'personal_statement', 'expected_start_date', 'documents'
        ]
    
    def validate(self, data):
        """Validate application doesn't already exist."""
        user = self.context['request'].user
        course = data.get('course')
        
        if CourseApplication.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("You have already applied to this course.")
        
        return data


class CourseSearchSerializer(serializers.Serializer):
    """Serializer for course search parameters."""
    
    query = serializers.CharField(max_length=255, required=False, help_text="Search query")
    university = serializers.IntegerField(required=False, help_text="University ID")
    level = serializers.ChoiceField(choices=Course.LEVEL_CHOICES, required=False)
    duration = serializers.ChoiceField(choices=Course.DURATION_CHOICES, required=False)
    min_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    subject = serializers.CharField(max_length=255, required=False, help_text="Subject name")
    country = serializers.CharField(max_length=100, required=False, help_text="Country")
    featured_only = serializers.BooleanField(default=False)
    popular_only = serializers.BooleanField(default=False)
    
    def validate(self, data):
        """Validate search parameters."""
        min_fee = data.get('min_fee')
        max_fee = data.get('max_fee')
        
        if min_fee and max_fee and min_fee > max_fee:
            raise serializers.ValidationError("Minimum fee cannot be greater than maximum fee.")
        
        return data


class CourseFilterSerializer(serializers.Serializer):
    """Serializer for course filtering parameters."""
    
    universities = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="List of university IDs"
    )
    levels = serializers.ListField(
        child=serializers.ChoiceField(choices=Course.LEVEL_CHOICES),
        required=False,
        help_text="List of course levels"
    )
    durations = serializers.ListField(
        child=serializers.ChoiceField(choices=Course.DURATION_CHOICES),
        required=False,
        help_text="List of course durations"
    )
    subjects = serializers.ListField(
        child=serializers.CharField(max_length=255),
        required=False,
        help_text="List of subject names"
    )
    countries = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        help_text="List of countries"
    )
    fee_range = serializers.DictField(
        child=serializers.DecimalField(max_digits=10, decimal_places=2),
        required=False,
        help_text="Fee range with min and max values"
    )
    rating_min = serializers.IntegerField(
        min_value=1, max_value=5, required=False,
        help_text="Minimum rating (1-5)"
    )
    status = serializers.ChoiceField(
        choices=Course.STATUS_CHOICES, required=False
    )


class CourseStatsSerializer(serializers.Serializer):
    """Serializer for course statistics."""
    
    total_courses = serializers.IntegerField()
    total_applications = serializers.IntegerField()
    average_rating = serializers.FloatField()
    total_ratings = serializers.IntegerField()
    courses_by_level = serializers.DictField()
    courses_by_duration = serializers.DictField()
    top_courses = CourseListSerializer(many=True)
    featured_courses = CourseListSerializer(many=True)
    popular_courses = CourseListSerializer(many=True) 