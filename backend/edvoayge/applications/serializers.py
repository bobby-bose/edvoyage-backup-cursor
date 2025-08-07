"""
Application serializers for EdVoyage API.
Handles data serialization for application-related endpoints.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Application, ApplicationDocument, ApplicationStatus, ApplicationInterview,
    ApplicationFee, ApplicationCommunication
)


class ApplicationDocumentSerializer(serializers.ModelSerializer):
    """Serializer for application documents."""
    
    application_number = serializers.CharField(source='application.application_number', read_only=True)
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = ApplicationDocument
        fields = [
            'id', 'application_number', 'document_type', 'document_type_display',
            'document_name', 'file', 'file_size', 'file_type', 'status',
            'status_display', 'is_required', 'is_verified', 'verified_by',
            'verified_at', 'verification_notes', 'expiry_date', 'is_expired',
            'uploaded_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'application_number', 'document_type_display', 'status_display',
            'file_size', 'file_type', 'is_expired', 'uploaded_at', 'updated_at'
        ]
    
    def validate_file(self, value):
        """Validate file upload."""
        if value:
            # Check file size (max 10MB)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("File size must be less than 10MB.")
            
            # Check file type
            allowed_types = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png']
            file_extension = value.name.split('.')[-1].lower()
            if file_extension not in allowed_types:
                raise serializers.ValidationError("File type not allowed. Please upload PDF, DOC, DOCX, JPG, JPEG, or PNG files.")
        
        return value


class ApplicationStatusSerializer(serializers.ModelSerializer):
    """Serializer for application status history."""
    
    application_number = serializers.CharField(source='application.application_number', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    changed_by_username = serializers.CharField(source='changed_by.username', read_only=True)
    
    class Meta:
        model = ApplicationStatus
        fields = [
            'id', 'application_number', 'status', 'status_display', 'description',
            'notes', 'changed_by_username', 'changed_at'
        ]
        read_only_fields = [
            'id', 'application_number', 'status_display', 'changed_by_username', 'changed_at'
        ]


class ApplicationInterviewSerializer(serializers.ModelSerializer):
    """Serializer for application interviews."""
    
    application_number = serializers.CharField(source='application.application_number', read_only=True)
    interview_type_display = serializers.CharField(source='get_interview_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    recommendation_display = serializers.CharField(source='get_recommendation_display', read_only=True)
    
    class Meta:
        model = ApplicationInterview
        fields = [
            'id', 'application_number', 'interview_type', 'interview_type_display',
            'status', 'status_display', 'scheduled_date', 'duration_minutes',
            'interviewer_name', 'interviewer_email', 'interviewer_phone',
            'location', 'platform', 'meeting_link', 'preparation_notes',
            'interview_notes', 'feedback', 'score', 'recommendation',
            'recommendation_display', 'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'application_number', 'interview_type_display', 'status_display',
            'recommendation_display', 'created_at', 'updated_at', 'completed_at'
        ]
    
    def validate_scheduled_date(self, value):
        """Validate scheduled date is in the future."""
        from django.utils import timezone
        if value and value <= timezone.now():
            raise serializers.ValidationError("Interview must be scheduled for a future date.")
        return value
    
    def validate_score(self, value):
        """Validate interview score."""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Score must be between 0 and 100.")
        return value


class ApplicationFeeSerializer(serializers.ModelSerializer):
    """Serializer for application fees."""
    
    application_number = serializers.CharField(source='application.application_number', read_only=True)
    fee_type_display = serializers.CharField(source='get_fee_type_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = ApplicationFee
        fields = [
            'id', 'application_number', 'fee_type', 'fee_type_display', 'amount',
            'currency', 'payment_status', 'payment_status_display', 'payment_method',
            'transaction_id', 'due_date', 'paid_at', 'description', 'notes',
            'is_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'application_number', 'fee_type_display', 'payment_status_display',
            'is_overdue', 'created_at', 'updated_at'
        ]
    
    def validate_amount(self, value):
        """Validate fee amount."""
        if value <= 0:
            raise serializers.ValidationError("Fee amount must be greater than zero.")
        return value


class ApplicationCommunicationSerializer(serializers.ModelSerializer):
    """Serializer for application communications."""
    
    application_number = serializers.CharField(source='application.application_number', read_only=True)
    communication_type_display = serializers.CharField(source='get_communication_type_display', read_only=True)
    direction_display = serializers.CharField(source='get_direction_display', read_only=True)
    
    class Meta:
        model = ApplicationCommunication
        fields = [
            'id', 'application_number', 'communication_type', 'communication_type_display',
            'direction', 'direction_display', 'subject', 'message', 'from_email',
            'to_email', 'from_phone', 'to_phone', 'is_sent', 'is_delivered',
            'is_read', 'sent_at', 'delivered_at', 'read_at', 'created_at'
        ]
        read_only_fields = [
            'id', 'application_number', 'communication_type_display', 'direction_display',
            'is_sent', 'is_delivered', 'is_read', 'sent_at', 'delivered_at', 'read_at', 'created_at'
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for application information."""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    university_name = serializers.CharField(source='university.name', read_only=True)
    program_name = serializers.CharField(source='program.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    days_since_submission = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    
    # Related data
    documents = ApplicationDocumentSerializer(many=True, read_only=True)
    status_history = ApplicationStatusSerializer(many=True, read_only=True)
    interviews = ApplicationInterviewSerializer(many=True, read_only=True)
    fees = ApplicationFeeSerializer(many=True, read_only=True)
    communications = ApplicationCommunicationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'user_username', 'user_email', 'university_name', 'program_name',
            'application_number', 'status', 'status_display', 'priority', 'priority_display',
            'intended_start_date', 'intended_start_semester', 'academic_year',
            'personal_statement', 'research_proposal', 'references', 'additional_info',
            'notes', 'submitted_at', 'reviewed_at', 'decision_date', 'is_complete',
            'is_verified', 'days_since_submission', 'is_overdue', 'documents',
            'status_history', 'interviews', 'fees', 'communications', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user_username', 'user_email', 'university_name', 'program_name',
            'status_display', 'priority_display', 'days_since_submission', 'is_overdue',
            'documents', 'status_history', 'interviews', 'fees', 'communications',
            'created_at', 'updated_at'
        ]
    
    def validate_intended_start_date(self, value):
        """Validate intended start date."""
        from django.utils import timezone
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Intended start date cannot be in the past.")
        return value


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating applications."""
    
    class Meta:
        model = Application
        fields = [
            'university', 'program', 'intended_start_date', 'intended_start_semester',
            'academic_year', 'personal_statement', 'research_proposal', 'references',
            'additional_info', 'notes', 'priority'
        ]
        read_only_fields = ['application_number']  # Make application_number read-only
    
    def validate(self, data):
        """Validate application data."""
        # Check if user already has an application for this university and program
        user = self.context['request'].user
        university = data.get('university')
        program = data.get('program')
        
        if Application.objects.filter(
            user=user,
            university=university,
            program=program
        ).exists():
            raise serializers.ValidationError(
                "You already have an application for this university and program."
            )
        
        return data
    
    def create(self, validated_data):
        """Create application with auto-generated application number."""
        user = self.context['request'].user
        
        # Generate application number
        import uuid
        application_number = f"APP-{uuid.uuid4().hex[:8].upper()}"
        
        # Ensure unique application number
        while Application.objects.filter(application_number=application_number).exists():
            application_number = f"APP-{uuid.uuid4().hex[:8].upper()}"
        
        validated_data['user'] = user
        validated_data['application_number'] = application_number
        
        print(f"🔍 DEBUG: Creating application with number: {application_number}")
        print(f"🔍 DEBUG: User: {user.username} (ID: {user.id})")
        print(f"🔍 DEBUG: University: {validated_data.get('university')}")
        print(f"🔍 DEBUG: Program: {validated_data.get('program')}")
        
        return super().create(validated_data)


class ApplicationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating applications."""
    
    class Meta:
        model = Application
        fields = [
            'priority', 'intended_start_date', 'intended_start_semester',
            'academic_year', 'personal_statement', 'research_proposal',
            'references', 'additional_info', 'notes'
        ]
    
    def validate(self, data):
        """Validate update data."""
        instance = self.instance
        
        # Prevent updates to submitted applications
        if instance.status in ['submitted', 'under_review', 'accepted', 'rejected']:
            raise serializers.ValidationError(
                "Cannot update application after submission."
            )
        
        return data


class ApplicationSubmitSerializer(serializers.Serializer):
    """Serializer for submitting applications."""
    
    confirm_submission = serializers.BooleanField(
        help_text="Confirm that you want to submit this application"
    )
    
    def validate_confirm_submission(self, value):
        """Validate confirmation."""
        if not value:
            raise serializers.ValidationError("You must confirm submission to proceed.")
        return value


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating application status."""
    
    class Meta:
        model = ApplicationStatus
        fields = ['status', 'description', 'notes']
    
    def create(self, validated_data):
        """Create status update and update application status."""
        application = self.context['application']
        user = self.context['request'].user
        
        # Update application status
        application.status = validated_data['status']
        if validated_data['status'] == 'submitted' and not application.submitted_at:
            application.submitted_at = timezone.now()
        application.save()
        
        # Create status history entry
        validated_data['application'] = application
        validated_data['changed_by'] = user
        
        return super().create(validated_data)


class ApplicationDocumentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating application documents."""
    
    class Meta:
        model = ApplicationDocument
        fields = [
            'document_type', 'document_name', 'file', 'is_required',
            'expiry_date', 'description'
        ]
    
    def create(self, validated_data):
        """Create document with application context."""
        application = self.context['application']
        validated_data['application'] = application
        
        # Set file size and type
        if validated_data.get('file'):
            validated_data['file_size'] = validated_data['file'].size
            validated_data['file_type'] = validated_data['file'].name.split('.')[-1].lower()
        
        return super().create(validated_data)


class ApplicationInterviewCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating application interviews."""
    
    class Meta:
        model = ApplicationInterview
        fields = [
            'interview_type', 'scheduled_date', 'duration_minutes',
            'interviewer_name', 'interviewer_email', 'interviewer_phone',
            'location', 'platform', 'meeting_link', 'preparation_notes'
        ]
    
    def create(self, validated_data):
        """Create interview with application context."""
        application = self.context['application']
        validated_data['application'] = application
        return super().create(validated_data)


class ApplicationFeeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating application fees."""
    
    class Meta:
        model = ApplicationFee
        fields = [
            'fee_type', 'amount', 'currency', 'due_date', 'description', 'notes'
        ]
    
    def create(self, validated_data):
        """Create fee with application context."""
        application = self.context['application']
        validated_data['application'] = application
        return super().create(validated_data)


class ApplicationSearchSerializer(serializers.Serializer):
    """Serializer for application search."""
    
    status = serializers.ChoiceField(
        choices=Application.APPLICATION_STATUS_CHOICES,
        required=False
    )
    priority = serializers.ChoiceField(
        choices=Application.PRIORITY_CHOICES,
        required=False
    )
    university = serializers.IntegerField(required=False)
    program = serializers.IntegerField(required=False)
    is_complete = serializers.BooleanField(required=False)
    is_verified = serializers.BooleanField(required=False)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)


class ApplicationStatsSerializer(serializers.Serializer):
    """Serializer for application statistics."""
    
    total_applications = serializers.IntegerField()
    submitted_applications = serializers.IntegerField()
    accepted_applications = serializers.IntegerField()
    rejected_applications = serializers.IntegerField()
    pending_applications = serializers.IntegerField()
    applications_by_status = serializers.DictField()
    applications_by_university = serializers.DictField()
    recent_applications = ApplicationSerializer(many=True)
    overdue_applications = ApplicationSerializer(many=True)


class ApplicationDashboardSerializer(serializers.Serializer):
    """Serializer for application dashboard."""
    
    user_applications = ApplicationSerializer(many=True)
    recent_status_updates = ApplicationStatusSerializer(many=True)
    upcoming_interviews = ApplicationInterviewSerializer(many=True)
    pending_fees = ApplicationFeeSerializer(many=True)
    recent_communications = ApplicationCommunicationSerializer(many=True)
    application_stats = ApplicationStatsSerializer()


class FrontendApplicationSerializer(serializers.ModelSerializer):
    """Custom serializer for frontend compatibility."""
    
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    name = serializers.CharField(source='application_number')
    email_id = serializers.CharField(source='user.email')
    user = serializers.IntegerField(source='user.id')
    university_id = serializers.IntegerField(source='university.id')
    created_by = serializers.CharField(source='user.username')
    university = serializers.SerializerMethodField()
    university_name = serializers.CharField(source='university.name', read_only=True)
    program_name = serializers.CharField(source='program.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'month', 'year', 'name', 'email_id', 'user', 'university_id',
            'created_by', 'university', 'university_name', 'program_name', 'status_display'
        ]
    
    def get_month(self, obj):
        """Get month from created_at date."""
        if obj.created_at:
            return obj.created_at.strftime('%B')
        return 'Unknown'
    
    def get_year(self, obj):
        """Get year from created_at date."""
        if obj.created_at:
            return str(obj.created_at.year)
        return 'Unknown'
    
    def get_university(self, obj):
        """Get university data in expected format."""
        if obj.university:
            return {
                'University_name': obj.university.name
            }
        return {'University_name': 'Unknown University'} 