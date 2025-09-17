"""
University serializers for EdVoyage API.
Handles data serialization for university-related endpoints.
"""

from rest_framework import serializers
from .models import (
    University, Campus, UniversityRanking, UniversityProgram,
    UniversityFaculty, UniversityResearch, UniversityPartnership, UniversityGallery , Feed
)

# adjust import if Feed is in another app


class FeedSerializer(serializers.ModelSerializer):
    university_id = serializers.PrimaryKeyRelatedField(
        source="university", queryset=University.objects.all(), write_only=True
    )
    university_name = serializers.CharField(source="university.name", read_only=True)
    time_ago = serializers.ReadOnlyField()
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        fields = [
            "id",
            "university_id",   # ✅ renamed
            "university_name",
            "user_name",
            "profile_image_url",
            "title",
            "description",
            "created_at",
            "time_ago",
        ]

    def get_profile_image_url(self, obj):
        request = self.context.get("request")
        if obj.profile_image and request:
            return request.build_absolute_uri(obj.profile_image.url)
        return None



class UniversityGallerySerializer(serializers.ModelSerializer):
    """Serializer for university gallery images."""
    
    university_name = serializers.CharField(source='university.name', read_only=True)
    image1_url = serializers.SerializerMethodField()
    image2_url = serializers.SerializerMethodField()
    image3_url = serializers.SerializerMethodField()
    image4_url = serializers.SerializerMethodField()
    image5_url = serializers.SerializerMethodField()
    image6_url = serializers.SerializerMethodField()
    
    class Meta:
        model = UniversityGallery
        fields = [
            'id', 'university_name', 'image1', 'image1_url', 'image2', 'image2_url',
            'image3', 'image3_url', 'image4', 'image4_url', 'image5', 'image5_url',
            'image6', 'image6_url', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'university_name', 'image1_url', 'image2_url', 'image3_url',
            'image4_url', 'image5_url', 'image6_url', 'created_at', 'updated_at'
        ]
    
    def get_image1_url(self, obj):
        """Get the full URL for image1."""
        if obj.image1:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image1.url)
            return obj.image1.url
        return None
    
    def get_image2_url(self, obj):
        """Get the full URL for image2."""
        if obj.image2:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image2.url)
            return obj.image2.url
        return None
    
    def get_image3_url(self, obj):
        """Get the full URL for image3."""
        if obj.image3:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image3.url)
            return obj.image3.url
        return None
    
    def get_image4_url(self, obj):
        """Get the full URL for image4."""
        if obj.image4:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image4.url)
            return obj.image4.url
        return None
    
    def get_image5_url(self, obj):
        """Get the full URL for image5."""
        if obj.image5:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image5.url)
            return obj.image5.url
        return None
    
    def get_image6_url(self, obj):
        """Get the full URL for image6."""
        if obj.image6:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image6.url)
            return obj.image6.url
        return None


class CampusSerializer(serializers.ModelSerializer):
    """Serializer for campus information."""
    
    university_name = serializers.CharField(source='university.name', read_only=True)
    
    class Meta:
        model = Campus
        fields = [
            'id', 'university_name', 'name', 'campus_type', 'address', 'city',
            'state', 'country', 'postal_code', 'phone', 'email', 'website',
            'facilities', 'accommodation', 'transportation', 'images',
            'virtual_tour_url', 'is_active', 'is_main_campus',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'university_name', 'created_at', 'updated_at']


class UniversityRankingSerializer(serializers.ModelSerializer):
    """Serializer for university rankings."""
    
    university_name = serializers.CharField(source='university.name', read_only=True)
    
    class Meta:
        model = UniversityRanking
        fields = [
            'id', 'university_name', 'ranking_type', 'ranking_source', 'rank',
            'total_institutions', 'score', 'year', 'methodology', 'criteria',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'university_name', 'created_at', 'updated_at']
    
    def validate_rank(self, value):
        """Validate rank is positive."""
        if value <= 0:
            raise serializers.ValidationError("Rank must be a positive number.")
        return value
    
    def validate_year(self, value):
        """Validate year is reasonable."""
        from django.utils import timezone
        current_year = timezone.now().year
        if value < 1900 or value > current_year + 1:
            raise serializers.ValidationError("Year must be between 1900 and next year.")
        return value


class UniversityProgramSerializer(serializers.ModelSerializer):
    """Serializer for university programs."""
    
    university_name = serializers.CharField(source='university.name', read_only=True)
    
    class Meta:
        model = UniversityProgram
        fields = [
            'id', 'university_name', 'name', 'program_level', 'program_type',
            'description', 'objectives', 'outcomes', 'duration_years',
            'total_credits', 'semesters', 'entry_requirements',
            'language_requirements', 'is_active', 'is_featured',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'university_name', 'created_at', 'updated_at']
    
    def validate_duration_years(self, value):
        """Validate duration is reasonable."""
        if value < 1 or value > 10:
            raise serializers.ValidationError("Duration must be between 1 and 10 years.")
        return value


class UniversityFacultySerializer(serializers.ModelSerializer):
    """Serializer for university faculties."""
    
    university_name = serializers.CharField(source='university.name', read_only=True)
    
    class Meta:
        model = UniversityFaculty
        fields = [
            'id', 'university_name', 'name', 'short_name', 'description',
            'mission', 'email', 'phone', 'website', 'student_count',
            'faculty_count', 'logo', 'images', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'university_name', 'created_at', 'updated_at']


class UniversityResearchSerializer(serializers.ModelSerializer):
    """Serializer for university research."""
    
    university_name = serializers.CharField(source='university.name', read_only=True)
    
    class Meta:
        model = UniversityResearch
        fields = [
            'id', 'university_name', 'title', 'research_area', 'description',
            'objectives', 'methodology', 'funding_amount', 'funding_source',
            'start_date', 'end_date', 'status', 'publications',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'university_name', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate start and end dates."""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError("End date cannot be before start date.")
        
        return data


class UniversityPartnershipSerializer(serializers.ModelSerializer):
    """Serializer for university partnerships."""
    
    university_name = serializers.CharField(source='university.name', read_only=True)
    
    class Meta:
        model = UniversityPartnership
        fields = [
            'id', 'university_name', 'partner_name', 'partnership_type',
            'description', 'objectives', 'partner_contact', 'partner_email',
            'partner_website', 'start_date', 'end_date', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'university_name', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate start and end dates."""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError("End date cannot be before start date.")
        
        return data


class UniversitySerializer(serializers.ModelSerializer):
    """Serializer for university information."""
    
    campuses = CampusSerializer(many=True, read_only=True)
    rankings = UniversityRankingSerializer(many=True, read_only=True)
    programs = UniversityProgramSerializer(many=True, read_only=True)
    faculties = UniversityFacultySerializer(many=True, read_only=True)
    research = UniversityResearchSerializer(many=True, read_only=True)
    partnerships = UniversityPartnershipSerializer(many=True, read_only=True)
    gallery = UniversityGallerySerializer(read_only=True)
    feed = serializers.SerializerMethodField()
    age = serializers.ReadOnlyField()
    international_student_percentage = serializers.ReadOnlyField()
    logo_url = serializers.SerializerMethodField()
    banner_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = University
        fields = [
            'id', 'name', 'short_name', 'slug', 'description', 'mission_statement',
            'vision_statement', 'university_type', 'founded_year', 'accreditation',
            'website', 'email', 'phone', 'country', 'state', 'city', 'address',
            'postal_code', 'logo', 'logo_url', 'banner_image', 'banner_image_url', 'gallery', 'total_students',
            'international_students', 'faculty_count', 'is_active', 'is_featured',
            'is_verified', 'age', 'international_student_percentage', 'campuses',
            'rankings', 'programs', 'faculties', 'research', 'partnerships',
            'gallery', 'feed', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'age', 'international_student_percentage', 'campuses',
            'rankings', 'programs', 'faculties', 'research', 'partnerships',
            'gallery', 'feed', 'created_at', 'updated_at'
        ]
    
    def validate_founded_year(self, value):
        """Validate founded year is reasonable."""
        from django.utils import timezone
        current_year = timezone.now().year
        if value and (value < 1000 or value > current_year):
            raise serializers.ValidationError("Founded year must be between 1000 and current year.")
        return value
    
    def validate_total_students(self, value):
        """Validate total students count."""
        if value and value < 0:
            raise serializers.ValidationError("Total students cannot be negative.")
        return value

    def get_feed(self, obj):
        """Get feeds directly linked to this university."""
        feeds = obj.feeds.all().order_by("-created_at")[:5]
        return FeedSerializer(feeds, many=True, context=self.context).data

    def get_logo_url(self, obj):
        """Get the full URL for the university logo."""
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None

    def get_banner_image_url(self, obj):
        """Get the full URL for the university banner image."""
        if obj.banner_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.banner_image.url)
            return obj.banner_image.url
        return None


class UniversityCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating universities."""
    
    class Meta:
        model = University
        fields = [
            'name', 'short_name', 'slug', 'description', 'mission_statement',
            'vision_statement', 'university_type', 'founded_year', 'accreditation',
            'website', 'email', 'phone', 'country', 'state', 'city', 'address',
            'postal_code', 'logo', 'banner_image', 'total_students',
            'international_students', 'faculty_count', 'is_active', 'is_featured',
            'is_verified'
        ]
    
    def validate_slug(self, value):
        """Validate slug uniqueness."""
        if University.objects.filter(slug=value).exists():
            raise serializers.ValidationError("A university with this slug already exists.")
        return value


class UniversityUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating universities."""
    
    class Meta:
        model = University
        fields = [
            'name', 'short_name', 'description', 'mission_statement',
            'vision_statement', 'university_type', 'founded_year', 'accreditation',
            'website', 'email', 'phone', 'country', 'state', 'city', 'address',
            'postal_code', 'logo', 'banner_image', 'total_students',
            'international_students', 'faculty_count', 'is_active', 'is_featured',
            'is_verified'
        ]


class CampusCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating campuses."""
    
    class Meta:
        model = Campus
        fields = [
            'university', 'name', 'campus_type', 'address', 'city', 'state',
            'country', 'postal_code', 'phone', 'email', 'website', 'facilities',
            'accommodation', 'transportation', 'images', 'virtual_tour_url',
            'is_active', 'is_main_campus'
        ]


class CampusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating campuses."""
    
    class Meta:
        model = Campus
        fields = [
            'name', 'campus_type', 'address', 'city', 'state', 'country',
            'postal_code', 'phone', 'email', 'website', 'facilities',
            'accommodation', 'transportation', 'images', 'virtual_tour_url',
            'is_active', 'is_main_campus'
        ]


class UniversityRankingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating university rankings."""
    
    class Meta:
        model = UniversityRanking
        fields = [
            'university', 'ranking_type', 'ranking_source', 'rank',
            'total_institutions', 'score', 'year', 'methodology', 'criteria'
        ]
    
    def validate(self, data):
        """Validate ranking uniqueness."""
        university = data.get('university')
        ranking_type = data.get('ranking_type')
        ranking_source = data.get('ranking_source')
        year = data.get('year')
        
        if UniversityRanking.objects.filter(
            university=university,
            ranking_type=ranking_type,
            ranking_source=ranking_source,
            year=year
        ).exists():
            raise serializers.ValidationError(
                "A ranking for this university, type, source, and year already exists."
            )
        
        return data


class UniversityProgramCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating university programs."""
    
    class Meta:
        model = UniversityProgram
        fields = [
            'university', 'name', 'program_level', 'program_type', 'description',
            'objectives', 'outcomes', 'duration_years', 'total_credits',
            'semesters', 'entry_requirements', 'language_requirements',
            'is_active', 'is_featured'
        ]


class UniversityFacultyCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating university faculties."""
    
    class Meta:
        model = UniversityFaculty
        fields = [
            'university', 'name', 'short_name', 'description', 'mission',
            'email', 'phone', 'website', 'student_count', 'faculty_count',
            'logo', 'images', 'is_active'
        ]


class UniversityResearchCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating university research."""
    
    class Meta:
        model = UniversityResearch
        fields = [
            'university', 'title', 'research_area', 'description', 'objectives',
            'methodology', 'funding_amount', 'funding_source', 'start_date',
            'end_date', 'status', 'publications'
        ]


class UniversityPartnershipCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating university partnerships."""
    
    class Meta:
        model = UniversityPartnership
        fields = [
            'university', 'partner_name', 'partnership_type', 'description',
            'objectives', 'partner_contact', 'partner_email', 'partner_website',
            'start_date', 'end_date', 'status'
        ]


class UniversitySearchSerializer(serializers.Serializer):
    """Serializer for university search."""
    
    query = serializers.CharField(max_length=255, required=False)
    country = serializers.CharField(max_length=100, required=False)
    university_type = serializers.ChoiceField(
        choices=University.UNIVERSITY_TYPE_CHOICES,
        required=False
    )
    min_rank = serializers.IntegerField(required=False, min_value=1)
    max_rank = serializers.IntegerField(required=False, min_value=1)
    has_programs = serializers.BooleanField(required=False)
    is_featured = serializers.BooleanField(required=False)
    is_verified = serializers.BooleanField(required=False)
    
    def validate(self, data):
        """Validate search parameters."""
        min_rank = data.get('min_rank')
        max_rank = data.get('max_rank')
        
        if min_rank and max_rank and min_rank > max_rank:
            raise serializers.ValidationError("Min rank cannot be greater than max rank.")
        
        return data


class UniversityStatsSerializer(serializers.Serializer):
    """Serializer for university statistics."""
    
    total_universities = serializers.IntegerField()
    active_universities = serializers.IntegerField()
    featured_universities = serializers.IntegerField()
    verified_universities = serializers.IntegerField()
    universities_by_country = serializers.DictField()
    universities_by_type = serializers.DictField()
    top_ranked_universities = UniversitySerializer(many=True)
    recent_universities = UniversitySerializer(many=True)


class UniversityComparisonSerializer(serializers.Serializer):
    """Serializer for university comparison."""
    
    universities = UniversitySerializer(many=True)
    comparison_data = serializers.DictField()
    ranking_comparison = serializers.ListField()
    program_comparison = serializers.ListField()
    cost_comparison = serializers.ListField() 