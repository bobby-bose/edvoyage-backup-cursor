from rest_framework import serializers
from .models import SimpleEducation, SimpleWork, SimpleSocial

class SimpleEducationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = SimpleEducation
        fields = [
            'id', 'user', 
            'higher_start_year', 'higher_end_year', 'higher_gpa',
            'lower_start_year', 'lower_end_year', 'lower_gpa',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate(self, data):
        """Validate education data"""
        # Validate higher education years
        if data.get('higher_start_year') and data.get('higher_end_year'):
            if data['higher_start_year'] > data['higher_end_year']:
                raise serializers.ValidationError("Higher education start year cannot be after end year")
        
        # Validate lower education years
        if data.get('lower_start_year') and data.get('lower_end_year'):
            if data['lower_start_year'] > data['lower_end_year']:
                raise serializers.ValidationError("Lower education start year cannot be after end year")
        
        # Validate GPA ranges
        if data.get('higher_gpa') and (data['higher_gpa'] < 0 or data['higher_gpa'] > 5):
            raise serializers.ValidationError("Higher education GPA must be between 0 and 5")
        
        if data.get('lower_gpa') and (data['lower_gpa'] < 0 or data['lower_gpa'] > 5):
            raise serializers.ValidationError("Lower education GPA must be between 0 and 5")
        
        return data

class SimpleWorkSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    
    class Meta:
        model = SimpleWork
        fields = [
            'id', 'user', 'position', 'start_year', 'end_year', 'pursuing',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate(self, data):
        """Validate work data"""
        # Validate years if both are provided
        if data.get('start_year') and data.get('end_year'):
            if data['start_year'] > data['end_year']:
                raise serializers.ValidationError("Start year cannot be after end year")
        
        # If pursuing is True, end_year should be null
        if data.get('pursuing') and data.get('end_year'):
            raise serializers.ValidationError("End year should not be set when pursuing is True")
        
        return data

class SimpleSocialSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    
    class Meta:
        model = SimpleSocial
        fields = [
            'id', 'user', 'facebook_link', 'linkedin_link', 'twitter_link', 'instagram_link',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate(self, data):
        """Validate social links data"""
        # You can add URL validation here if needed
        return data 