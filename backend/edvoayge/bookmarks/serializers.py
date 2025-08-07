from rest_framework import serializers
from .models import FavouriteUniversity, FavouriteCourse
from universities.serializers import UniversitySerializer
from courses.serializers import CourseListSerializer

class FavouriteUniversitySerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    university_id = serializers.IntegerField(write_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = FavouriteUniversity
        fields = ['id', 'university', 'university_id', 'user_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'university', 'user_name', 'created_at', 'updated_at']

    def validate_university_id(self, value):
        from universities.models import University
        try:
            University.objects.get(id=value)
        except University.DoesNotExist:
            raise serializers.ValidationError("University does not exist")
        return value

class FavouriteCourseSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = FavouriteCourse
        fields = ['id', 'course', 'course_id', 'user_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'course', 'user_name', 'created_at', 'updated_at']

    def validate_course_id(self, value):
        from courses.models import Course
        try:
            Course.objects.get(id=value)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course does not exist")
        return value
