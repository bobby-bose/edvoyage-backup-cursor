from rest_framework import serializers
from .models import User, Post, PostLike, Comment, CommentLike, PostShare, Notification, UserFollow


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    full_name = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'full_name', 
            'is_active', 'follower_count', 'following_count', 'post_count',
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

    def get_full_name(self, obj):
        print("NNNNNNNN",obj.first_name , obj.last_name , obj.username)
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

    def get_follower_count(self, obj):
        return obj.cavity_followers.count()

    def get_following_count(self, obj):
        return obj.cavity_following.count()

    def get_post_count(self, obj):
        return obj.cavity_posts.count()


class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal user serializer for nested objects"""
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name']

    def get_full_name(self, obj):
        print("NNNNNNNN",obj.first_name , obj.last_name , obj.username)
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username


class PostLikeSerializer(serializers.ModelSerializer):
    """Serializer for PostLike model"""
    user = UserMinimalSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']


class CommentLikeSerializer(serializers.ModelSerializer):
    """Serializer for CommentLike model"""
    user = UserMinimalSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    user = UserMinimalSerializer(source='author', read_only=True)
    like_count = serializers.ReadOnlyField()
    replies_count = serializers.ReadOnlyField()
    is_liked_by_user = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'user', 'parent_comment', 'content',
            'is_edited', 'like_count', 'replies_count',
            'is_liked_by_user', 'replies', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_replies(self, obj):
        # Only include replies if this is a top-level comment
        if obj.parent_comment is None:
            replies = obj.replies.order_by('created_at')
            return CommentSerializer(replies, many=True, context=self.context).data
        return []


class PostShareSerializer(serializers.ModelSerializer):
    """Serializer for PostShare model"""
    user = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = PostShare
        fields = ['id', 'user', 'share_text', 'created_at']
        read_only_fields = ['id', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model"""
    user = UserMinimalSerializer(source='author', read_only=True)
    like_count = serializers.ReadOnlyField()
    comment_count = serializers.ReadOnlyField()
    share_count = serializers.ReadOnlyField()
    is_liked_by_user = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'content', 'year', 'media_urls', 'is_anonymous',
            'is_edited', 'like_count', 'comment_count',
            'share_count', 'is_liked_by_user', 'comments',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_comments(self, obj):
        # Only include top-level comments
        comments = obj.comments.filter(parent_comment=None).order_by('created_at')
        return CommentSerializer(comments, many=True, context=self.context).data


class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating posts"""
    user_id = serializers.CharField(required=False, write_only=True)
    
    def __init__(self, *args, **kwargs):
        print(f"🔍 DEBUG: PostCreateSerializer.__init__ called")
        print(f"🔍 DEBUG: args: {args}")
        print(f"🔍 DEBUG: kwargs: {kwargs}")
        super().__init__(*args, **kwargs)
    
    def validate(self, attrs):
        print(f"🔍 DEBUG: PostCreateSerializer.validate called")
        print(f"🔍 DEBUG: attrs: {attrs}")
        print(f"🔍 DEBUG: self.initial_data: {self.initial_data}")
        print(f"🔍 DEBUG: self.context: {self.context}")
        
        # Call parent validation
        validated_data = super().validate(attrs)
        print(f"🔍 DEBUG: Parent validation completed")
        print(f"🔍 DEBUG: validated_data: {validated_data}")
        
        return validated_data
    
    def create(self, validated_data):
        print(f"🔍 DEBUG: PostCreateSerializer.create called")
        print(f"🔍 DEBUG: validated_data: {validated_data}")
        print(f"🔍 DEBUG: self.context: {self.context}")
        
        # Extract user_id from validated data
        user_id = validated_data.pop('user_id', None)
        print(f"🔍 DEBUG: user_id from request: {user_id}")
        
        # Get the request from context
        request = self.context.get('request')
        print(f"🔍 DEBUG: request: {request}")
        if request:
            print(f"🔍 DEBUG: request.user: {request.user}")
            print(f"🔍 DEBUG: request.user.is_authenticated: {request.user.is_authenticated}")
        
        # Determine which user to assign
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if user_id:
            # Use provided user_id
            try:
                user = User.objects.get(id=user_id)
                print(f"🔍 DEBUG: Found user by ID: {user}")
            except User.DoesNotExist:
                print(f"❌ ERROR: User with ID {user_id} not found")
                # Fallback to default user
                user = User.objects.first()
                if not user:
                    user = User.objects.create_user(
                        username='default_user',
                        email='default@example.com',
                        password='defaultpass123'
                    )
                print(f"🔍 DEBUG: Using fallback user: {user}")
        elif request and request.user.is_authenticated:
            # Use authenticated user
            user = request.user
            print(f"🔍 DEBUG: Using authenticated user: {user}")
        else:
            # Use default user
            user = User.objects.first()
            if not user:
                user = User.objects.create_user(
                    username='default_user',
                    email='default@example.com',
                    password='defaultpass123'
                )
            print(f"🔍 DEBUG: Using default user: {user}")
        
        # Create the post with the determined user
        validated_data['author'] = user
        post = super().create(validated_data)
        print(f"🔍 DEBUG: Post created: {post}")
        print(f"🔍 DEBUG: Post ID: {post.id}")
        print(f"🔍 DEBUG: Post content: {post.content}")
        print(f"🔍 DEBUG: Post year: {post.year}")
        print(f"🔍 DEBUG: Post author: {post.author}")
        
        return post
    
    class Meta:
        model = Post
        fields = ['content', 'year', 'media_urls', 'is_anonymous', 'user_id']

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Comment, Post

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'post_title',
            'author',
            'author_name',
            'user',
            'user_name',
            'content',
            'parent_comment',
            'is_edited',
            'edit_history',
            'created_at',
            'updated_at',
            'like_count'
        ]
        read_only_fields = [
            'id',
            'author',
            'user',
            'is_edited',
            'edit_history',
            'created_at',
            'updated_at',
            'like_count'
        ]

class CommentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post','content', 'parent_comment', 'email', 'created_at', 'updated_at']

    def create(self, validated_data):
        email = validated_data.pop('email')
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "No user found with this email"})
        validated_data['author'] = user
        return super().create(validated_data)



class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    recipient = UserMinimalSerializer(read_only=True)
    sender = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'sender', 'notification_type', 'post', 'comment',
            'message', 'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserFollowSerializer(serializers.ModelSerializer):
    """Serializer for UserFollow model"""
    follower = UserMinimalSerializer(read_only=True)
    following = UserMinimalSerializer(read_only=True)

    class Meta:
        model = UserFollow
        fields = ['id', 'follower', 'following', 'created_at']
        read_only_fields = ['id', 'created_at']


class PostLikeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating post likes"""
    class Meta:
        model = PostLike
        fields = ['post']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        # Check if like already exists
        like, created = PostLike.objects.get_or_create(
            user=validated_data['user'],
            post=validated_data['post']
        )
        return like


class CommentLikeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating comment likes"""
    class Meta:
        model = CommentLike
        fields = ['comment']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        # Check if like already exists
        like, created = CommentLike.objects.get_or_create(
            user=validated_data['user'],
            comment=validated_data['comment']
        )
        return like


class PostShareCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating post shares"""
    class Meta:
        model = PostShare
        fields = ['post']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data) 