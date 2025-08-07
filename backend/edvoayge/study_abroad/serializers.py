from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    StudyAbroadProgram, StudyAbroadApplication, StudyAbroadExperience,
    StudyAbroadResource, StudyAbroadEvent, StudyAbroadEventRegistration
)

User = get_user_model()

class StudyAbroadProgramSerializer(serializers.ModelSerializer):
    """Serializer for StudyAbroadProgram model"""
    total_cost = serializers.ReadOnlyField()
    duration_days = serializers.ReadOnlyField()
    is_application_open = serializers.ReadOnlyField()
    available_spots = serializers.ReadOnlyField()

    class Meta:
        model = StudyAbroadProgram
        fields = [
            'id', 'name', 'description', 'program_type', 'status', 'country', 'city',
            'institution', 'campus_location', 'academic_level', 'field_of_study',
            'credits_offered', 'language_requirement', 'start_date', 'end_date',
            'application_deadline', 'tuition_cost', 'accommodation_cost', 'other_costs',
            'currency', 'scholarships_available', 'scholarship_amount', 'max_participants',
            'min_gpa_requirement', 'language_proficiency_required', 'visa_required',
            'highlights', 'requirements', 'application_process', 'contact_email',
            'contact_phone', 'program_image', 'brochure_file', 'is_featured',
            'is_active', 'total_cost', 'duration_days', 'is_application_open',
            'available_spots', 'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, data):
        """Validate program data"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        application_deadline = data.get('application_deadline')

        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("End date must be after start date.")

        if application_deadline and start_date and application_deadline >= start_date:
            raise serializers.ValidationError("Application deadline must be before program start date.")

        if data.get('min_gpa_requirement'):
            gpa = data['min_gpa_requirement']
            if gpa < 0 or gpa > 4:
                raise serializers.ValidationError("Minimum GPA must be between 0 and 4.")

        return data

class StudyAbroadApplicationSerializer(serializers.ModelSerializer):
    """Serializer for StudyAbroadApplication model"""
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    program = serializers.PrimaryKeyRelatedField(queryset=StudyAbroadProgram.objects.all())
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = StudyAbroadApplication
        fields = [
            'id', 'user', 'program', 'status', 'application_date', 'review_date',
            'decision_date', 'current_institution', 'current_major', 'current_gpa',
            'graduation_date', 'academic_standing', 'language_proficiency',
            'relevant_coursework', 'academic_goals', 'personal_statement',
            'motivation_letter', 'resume_file', 'transcript_file',
            'recommendation_letters', 'financial_aid_needed', 'scholarship_applied',
            'additional_funding_sources', 'reviewer_notes', 'reviewer',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'application_date', 'review_date', 'decision_date', 'created_at', 'updated_at')

    def validate(self, data):
        """Validate application data"""
        current_gpa = data.get('current_gpa')
        if current_gpa and (current_gpa < 0 or current_gpa > 4):
            raise serializers.ValidationError("Current GPA must be between 0 and 4.")

        # Check if user already has an application for this program
        user = data.get('user')
        program = data.get('program')
        if user and program:
            existing = StudyAbroadApplication.objects.filter(user=user, program=program)
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise serializers.ValidationError("You have already applied to this program.")

        return data

    def create(self, validated_data):
        """Create application with validation"""
        user = validated_data['user']
        program = validated_data['program']
        
        # Check if program is accepting applications
        if not program.is_application_open:
            raise serializers.ValidationError("Applications for this program are closed.")
        
        # Check if spots are available
        if program.available_spots is not None and program.available_spots <= 0:
            raise serializers.ValidationError("No spots available for this program.")
        
        return super().create(validated_data)

class StudyAbroadExperienceSerializer(serializers.ModelSerializer):
    """Serializer for StudyAbroadExperience model"""
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    program = serializers.PrimaryKeyRelatedField(queryset=StudyAbroadProgram.objects.all())

    class Meta:
        model = StudyAbroadExperience
        fields = [
            'id', 'user', 'program', 'title', 'experience_type', 'content', 'rating',
            'photos', 'video_url', 'is_approved', 'is_featured', 'is_public',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_rating(self, value):
        """Validate rating"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        """Validate experience data"""
        # Check if user has participated in the program
        user = data.get('user')
        program = data.get('program')
        if user and program:
            application = StudyAbroadApplication.objects.filter(
                user=user, 
                program=program, 
                status='accepted'
            ).first()
            if not application:
                raise serializers.ValidationError("You must have been accepted to the program to share an experience.")
        
        return data

class StudyAbroadResourceSerializer(serializers.ModelSerializer):
    """Serializer for StudyAbroadResource model"""
    class Meta:
        model = StudyAbroadResource
        fields = [
            'id', 'title', 'resource_type', 'description', 'content', 'file_attachment',
            'categories', 'tags', 'is_active', 'is_featured', 'requires_authentication',
            'download_count', 'view_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'download_count', 'view_count', 'created_at', 'updated_at')

    def validate(self, data):
        """Validate resource data"""
        categories = data.get('categories', '')
        tags = data.get('tags', '')
        
        # Validate categories and tags format
        if categories and len(categories.split(',')) > 10:
            raise serializers.ValidationError("Maximum 10 categories allowed.")
        
        if tags and len(tags.split(',')) > 20:
            raise serializers.ValidationError("Maximum 20 tags allowed.")
        
        return data

class StudyAbroadEventSerializer(serializers.ModelSerializer):
    """Serializer for StudyAbroadEvent model"""
    is_registration_open = serializers.ReadOnlyField()
    available_spots = serializers.ReadOnlyField()

    class Meta:
        model = StudyAbroadEvent
        fields = [
            'id', 'title', 'event_type', 'description', 'start_datetime', 'end_datetime',
            'location', 'is_virtual', 'virtual_meeting_url', 'max_attendees',
            'registration_required', 'registration_deadline', 'is_active', 'is_featured',
            'is_registration_open', 'available_spots', 'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, data):
        """Validate event data"""
        start_datetime = data.get('start_datetime')
        end_datetime = data.get('end_datetime')
        registration_deadline = data.get('registration_deadline')

        if start_datetime and end_datetime and start_datetime >= end_datetime:
            raise serializers.ValidationError("End datetime must be after start datetime.")

        if registration_deadline and start_datetime and registration_deadline >= start_datetime:
            raise serializers.ValidationError("Registration deadline must be before event start.")

        return data

class StudyAbroadEventRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for StudyAbroadEventRegistration model"""
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    event = serializers.PrimaryKeyRelatedField(queryset=StudyAbroadEvent.objects.all())

    class Meta:
        model = StudyAbroadEventRegistration
        fields = [
            'id', 'user', 'event', 'status', 'registration_date', 'attendance_date',
            'dietary_restrictions', 'special_accommodations', 'questions',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'registration_date', 'attendance_date', 'created_at', 'updated_at')

    def validate(self, data):
        """Validate registration data"""
        user = data.get('user')
        event = data.get('event')
        
        # Check if user is already registered
        if user and event:
            existing = StudyAbroadEventRegistration.objects.filter(user=user, event=event)
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise serializers.ValidationError("You are already registered for this event.")
        
        # Check if event is accepting registrations
        if event and not event.is_registration_open:
            raise serializers.ValidationError("Registration for this event is closed.")
        
        # Check if spots are available
        if event and event.available_spots is not None and event.available_spots <= 0:
            raise serializers.ValidationError("No spots available for this event.")
        
        return data

# Nested serializers for detailed views
class DetailedStudyAbroadProgramSerializer(StudyAbroadProgramSerializer):
    """Detailed serializer with application count"""
    application_count = serializers.SerializerMethodField()
    experience_count = serializers.SerializerMethodField()

    class Meta(StudyAbroadProgramSerializer.Meta):
        fields = StudyAbroadProgramSerializer.Meta.fields + ['application_count', 'experience_count']

    def get_application_count(self, obj):
        """Get count of applications for this program"""
        return obj.applications.count()

    def get_experience_count(self, obj):
        """Get count of experiences for this program"""
        return obj.experiences.filter(is_approved=True).count()

class DetailedStudyAbroadApplicationSerializer(StudyAbroadApplicationSerializer):
    """Detailed serializer with program and user information"""
    program = StudyAbroadProgramSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

class StudyAbroadStatisticsSerializer(serializers.Serializer):
    """Serializer for study abroad statistics"""
    total_programs = serializers.IntegerField()
    active_programs = serializers.IntegerField()
    total_applications = serializers.IntegerField()
    accepted_applications = serializers.IntegerField()
    total_experiences = serializers.IntegerField()
    featured_experiences = serializers.IntegerField()
    upcoming_events = serializers.IntegerField()
    popular_destinations = serializers.ListField(child=serializers.DictField())
    program_types_distribution = serializers.ListField(child=serializers.DictField()) 