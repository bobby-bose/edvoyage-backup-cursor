from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Content, ContentCategory, ContentTag, ContentView, ContentRating,
    ContentComment, ContentShare, ContentDownload, ContentBookmark, ContentAnalytics, Feed
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user information"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ContentCategorySerializer(serializers.ModelSerializer):
    """Serializer for content categories"""
    content_count = serializers.ReadOnlyField()
    
    class Meta:
        model = ContentCategory
        fields = [
            'id', 'name', 'description', 'color', 'icon', 
            'is_active', 'content_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ContentCategoryListSerializer(serializers.ModelSerializer):
    """List serializer for content categories with minimal data"""
    content_count = serializers.ReadOnlyField()
    
    class Meta:
        model = ContentCategory
        fields = ['id', 'name', 'color', 'icon', 'content_count', 'is_active']

class ContentTagSerializer(serializers.ModelSerializer):
    """Serializer for content tags"""
    content_count = serializers.ReadOnlyField()
    
    class Meta:
        model = ContentTag
        fields = [
            'id', 'name', 'color', 'description', 'content_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ContentTagListSerializer(serializers.ModelSerializer):
    """List serializer for content tags with minimal data"""
    content_count = serializers.ReadOnlyField()
    
    class Meta:
        model = ContentTag
        fields = ['id', 'name', 'color', 'content_count']

class ContentViewSerializer(serializers.ModelSerializer):
    """Serializer for content views"""
    content = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ContentView
        fields = [
            'id', 'content', 'user', 'ip_address', 'user_agent',
            'referrer', 'session_id', 'view_duration', 'created_at'
        ]
        read_only_fields = ['created_at']

class ContentRatingSerializer(serializers.ModelSerializer):
    """Serializer for content ratings"""
    content = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ContentRating
        fields = [
            'id', 'content', 'user', 'rating', 'review', 'is_helpful',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ContentRatingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating content ratings"""
    content_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ContentRating
        fields = ['content_id', 'rating', 'review', 'is_helpful']

    def validate_content_id(self, value):
        """Validate that content exists"""
        try:
            Content.objects.get(id=value)
        except Content.DoesNotExist:
            raise serializers.ValidationError("Content does not exist")
        return value

    def create(self, validated_data):
        """Create rating with current user"""
        content_id = validated_data.pop('content_id')
        content = Content.objects.get(id=content_id)
        validated_data['content'] = content
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ContentCommentSerializer(serializers.ModelSerializer):
    """Serializer for content comments"""
    content = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    replies_count = serializers.ReadOnlyField()
    is_reply = serializers.ReadOnlyField()
    
    class Meta:
        model = ContentComment
        fields = [
            'id', 'content', 'user', 'parent', 'comment', 'is_approved',
            'is_edited', 'edited_at', 'replies', 'replies_count', 'is_reply',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'edited_at']

    def get_replies(self, obj):
        """Get nested replies"""
        replies = obj.replies.all()
        return ContentCommentSerializer(replies, many=True).data

class ContentCommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating content comments"""
    content_id = serializers.IntegerField(write_only=True)
    parent_id = serializers.IntegerField(required=False)
    
    class Meta:
        model = ContentComment
        fields = ['content_id', 'parent_id', 'comment']

    def validate_content_id(self, value):
        """Validate that content exists"""
        try:
            Content.objects.get(id=value)
        except Content.DoesNotExist:
            raise serializers.ValidationError("Content does not exist")
        return value

    def validate_parent_id(self, value):
        """Validate that parent comment exists"""
        if value:
            try:
                ContentComment.objects.get(id=value)
            except ContentComment.DoesNotExist:
                raise serializers.ValidationError("Parent comment does not exist")
        return value

    def create(self, validated_data):
        """Create comment with current user"""
        content_id = validated_data.pop('content_id')
        content = Content.objects.get(id=content_id)
        validated_data['content'] = content
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ContentShareSerializer(serializers.ModelSerializer):
    """Serializer for content shares"""
    content = serializers.PrimaryKeyRelatedField(read_only=True)
    shared_by = UserSerializer(read_only=True)
    shared_with = UserSerializer(read_only=True)
    
    class Meta:
        model = ContentShare
        fields = [
            'id', 'content', 'shared_by', 'shared_with', 'share_type',
            'message', 'share_url', 'is_viewed', 'viewed_at', 'created_at'
        ]
        read_only_fields = ['shared_by', 'share_url', 'is_viewed', 'viewed_at', 'created_at']

class ContentShareCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating content shares"""
    content_id = serializers.IntegerField()
    shared_with_id = serializers.IntegerField(required=False)
    
    class Meta:
        model = ContentShare
        fields = ['content_id', 'shared_with_id', 'share_type', 'message']

    def validate_content_id(self, value):
        """Validate content exists"""
        try:
            Content.objects.get(id=value)
        except Content.DoesNotExist:
            raise serializers.ValidationError("Content does not exist")
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

class ContentDownloadSerializer(serializers.ModelSerializer):
    """Serializer for content downloads"""
    content = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ContentDownload
        fields = [
            'id', 'content', 'user', 'ip_address', 'user_agent',
            'download_url', 'file_size', 'created_at'
        ]
        read_only_fields = ['created_at']

class ContentBookmarkSerializer(serializers.ModelSerializer):
    """Serializer for content bookmarks"""
    content = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ContentBookmark
        fields = ['id', 'content', 'user', 'notes', 'created_at']
        read_only_fields = ['created_at']

class ContentBookmarkCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating content bookmarks"""
    content_id = serializers.IntegerField()
    
    class Meta:
        model = ContentBookmark
        fields = ['content_id', 'notes']

    def validate_content_id(self, value):
        """Validate that content exists"""
        try:
            Content.objects.get(id=value)
        except Content.DoesNotExist:
            raise serializers.ValidationError("Content does not exist")
        return value

    def create(self, validated_data):
        """Create bookmark with current user"""
        content_id = validated_data.pop('content_id')
        content = Content.objects.get(id=content_id)
        validated_data['content'] = content
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ContentAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for content analytics"""
    content = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ContentAnalytics
        fields = [
            'id', 'content', 'user', 'action_type', 'ip_address',
            'user_agent', 'referrer', 'session_id', 'metadata', 'created_at'
        ]
        read_only_fields = ['created_at']

class ContentSerializer(serializers.ModelSerializer):
    """Full serializer for content"""
    category = ContentCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    author = UserSerializer(read_only=True)
    tags = ContentTagListSerializer(many=True, read_only=True)
    is_active = serializers.ReadOnlyField()
    tags_list = serializers.ReadOnlyField()
    
    class Meta:
        model = Content
        fields = [
            'id', 'title', 'description', 'content_type', 'category', 'category_id',
            'author', 'file_url', 'file_size', 'duration', 'thumbnail_url',
            'status', 'is_public', 'is_featured', 'is_premium', 'meta_title',
            'meta_description', 'keywords', 'view_count', 'download_count',
            'share_count', 'average_rating', 'rating_count', 'is_active',
            'tags', 'tags_list', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = [
            'author', 'view_count', 'download_count', 'share_count',
            'average_rating', 'rating_count', 'created_at', 'updated_at', 'published_at'
        ]

class ContentListSerializer(serializers.ModelSerializer):
    """List serializer for content with minimal data"""
    category = ContentCategoryListSerializer(read_only=True)
    author = UserSerializer(read_only=True)
    tags = ContentTagListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Content
        fields = [
            'id', 'title', 'description', 'content_type', 'category', 'author',
            'thumbnail_url', 'status', 'is_public', 'is_featured', 'is_premium',
            'view_count', 'download_count', 'share_count', 'average_rating',
            'rating_count', 'tags', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'author', 'view_count', 'download_count', 'share_count',
            'average_rating', 'rating_count', 'created_at', 'updated_at'
        ]

class ContentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating content"""
    category_id = serializers.IntegerField()
    tag_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    
    class Meta:
        model = Content
        fields = [
            'title', 'description', 'content_type', 'category_id', 'file_url',
            'file_size', 'duration', 'thumbnail_url', 'status', 'is_public',
            'is_featured', 'is_premium', 'meta_title', 'meta_description',
            'keywords', 'tag_ids'
        ]

    def validate_category_id(self, value):
        """Validate that category exists"""
        try:
            ContentCategory.objects.get(id=value)
        except ContentCategory.DoesNotExist:
            raise serializers.ValidationError("Category does not exist")
        return value

    def validate_tag_ids(self, value):
        """Validate that tags exist"""
        if value:
            existing_tags = ContentTag.objects.filter(id__in=value)
            if len(existing_tags) != len(value):
                raise serializers.ValidationError("Some tags do not exist")
        return value

    def create(self, validated_data):
        """Create content with current user as author"""
        tag_ids = validated_data.pop('tag_ids', [])
        validated_data['author'] = self.context['request'].user
        content = super().create(validated_data)
        
        # Add tags
        if tag_ids:
            tags = ContentTag.objects.filter(id__in=tag_ids)
            content.tags.set(tags)
        
        return content

class ContentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating content"""
    category_id = serializers.IntegerField(required=False)
    tag_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    
    class Meta:
        model = Content
        fields = [
            'title', 'description', 'content_type', 'category_id', 'file_url',
            'file_size', 'duration', 'thumbnail_url', 'status', 'is_public',
            'is_featured', 'is_premium', 'meta_title', 'meta_description',
            'keywords', 'tag_ids'
        ]

    def validate_category_id(self, value):
        """Validate that category exists"""
        try:
            ContentCategory.objects.get(id=value)
        except ContentCategory.DoesNotExist:
            raise serializers.ValidationError("Category does not exist")
        return value

    def validate_tag_ids(self, value):
        """Validate that tags exist"""
        if value:
            existing_tags = ContentTag.objects.filter(id__in=value)
            if len(existing_tags) != len(value):
                raise serializers.ValidationError("Some tags do not exist")
        return value

    def update(self, instance, validated_data):
        """Update content and tags"""
        tag_ids = validated_data.pop('tag_ids', None)
        content = super().update(instance, validated_data)
        
        # Update tags if provided
        if tag_ids is not None:
            tags = ContentTag.objects.filter(id__in=tag_ids)
            content.tags.set(tags)
        
        return content

class ContentSearchSerializer(serializers.Serializer):
    """Serializer for content search"""
    q = serializers.CharField(max_length=200, required=False)
    category = serializers.IntegerField(required=False)
    content_type = serializers.ChoiceField(choices=Content.CONTENT_TYPES, required=False)
    status = serializers.ChoiceField(choices=Content.STATUS_CHOICES, required=False)
    is_public = serializers.BooleanField(required=False)
    is_featured = serializers.BooleanField(required=False)
    is_premium = serializers.BooleanField(required=False)
    author = serializers.IntegerField(required=False)
    tags = serializers.ListField(child=serializers.IntegerField(), required=False)

class ContentStatisticsSerializer(serializers.Serializer):
    """Serializer for content statistics"""
    total_content = serializers.IntegerField()
    total_views = serializers.IntegerField()
    total_downloads = serializers.IntegerField()
    total_shares = serializers.IntegerField()
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    popular_content = ContentListSerializer(many=True)
    recent_content = ContentListSerializer(many=True)
    category_stats = serializers.ListField()

class ContentViewCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating content views"""
    content_id = serializers.IntegerField()
    
    class Meta:
        model = ContentView
        fields = ['content_id', 'view_duration']

    def validate_content_id(self, value):
        """Validate that content exists"""
        try:
            Content.objects.get(id=value)
        except Content.DoesNotExist:
            raise serializers.ValidationError("Content does not exist")
        return value

    def create(self, validated_data):
        """Create view with current user"""
        content_id = validated_data.pop('content_id')
        content = Content.objects.get(id=content_id)
        validated_data['content'] = content
        validated_data['user'] = self.context['request'].user
        validated_data['ip_address'] = self.context['request'].META.get('REMOTE_ADDR')
        validated_data['user_agent'] = self.context['request'].META.get('HTTP_USER_AGENT', '')
        return super().create(validated_data)

class ContentDownloadCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating content downloads"""
    content_id = serializers.IntegerField()
    
    class Meta:
        model = ContentDownload
        fields = ['content_id', 'download_url', 'file_size']

    def validate_content_id(self, value):
        """Validate that content exists"""
        try:
            Content.objects.get(id=value)
        except Content.DoesNotExist:
            raise serializers.ValidationError("Content does not exist")
        return value

    def create(self, validated_data):
        """Create download with current user"""
        content_id = validated_data.pop('content_id')
        content = Content.objects.get(id=content_id)
        validated_data['content'] = content
        validated_data['user'] = self.context['request'].user
        validated_data['ip_address'] = self.context['request'].META.get('REMOTE_ADDR')
        validated_data['user_agent'] = self.context['request'].META.get('HTTP_USER_AGENT', '')
        return super().create(validated_data)

class ContentBulkActionSerializer(serializers.Serializer):
    """Serializer for bulk content actions"""
    content_ids = serializers.ListField(child=serializers.IntegerField())
    action = serializers.ChoiceField(choices=['publish', 'archive', 'delete', 'feature', 'unfeature', 'make_public', 'make_private'])

class ContentExportSerializer(serializers.Serializer):
    """Serializer for content export"""
    format = serializers.ChoiceField(choices=['json', 'csv', 'pdf'], default='json')
    include_analytics = serializers.BooleanField(default=False)
    include_comments = serializers.BooleanField(default=False)
    include_ratings = serializers.BooleanField(default=False)

class ContentImportSerializer(serializers.Serializer):
    """Serializer for content import"""
    file = serializers.FileField()
    category_id = serializers.IntegerField(required=False)
    overwrite = serializers.BooleanField(default=False) 

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ['user_name', 'avatar_url', 'date_posted', 'title', 'description'] 