import uuid
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatUser, ChatRoom, ChatRoomParticipant, Message, MessageStatus, Contact, ChatNotification

User = get_user_model()


class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal user serializer for chat"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ChatUserSerializer(serializers.ModelSerializer):
    """Full chat user serializer"""
    user = UserMinimalSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatUser
        fields = [
            'id', 'user', 'is_online', 'last_seen', 'profile_image', 
            'bio', 'specialization', 'institution', 'role', 'is_verified',
            'created_at', 'updated_at', 'full_name'
        ]
    
    def get_full_name(self, obj):
        return obj.full_name


class ChatUserMinimalSerializer(serializers.ModelSerializer):
    """Minimal chat user serializer for lists"""
    user = UserMinimalSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatUser
        fields = ['id', 'user', 'is_online', 'last_seen', 'profile_image', 'full_name']
    
    def get_full_name(self, obj):
        return obj.full_name


class ChatRoomParticipantSerializer(serializers.ModelSerializer):
    """Chat room participant serializer"""
    chat_user = ChatUserMinimalSerializer(read_only=True)
    
    class Meta:
        model = ChatRoomParticipant
        fields = ['id', 'chat_room', 'chat_user', 'joined_at', 'is_admin']


class MessageSerializer(serializers.ModelSerializer):
    """Message serializer"""
    sender = ChatUserMinimalSerializer(read_only=True)
    reply_to = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'chat_room', 'sender', 'content', 'message_type',
            'media_urls', 'reply_to', 'created_at', 'updated_at'
        ]
    
    def get_reply_to(self, obj):
        if obj.reply_to:
            return MessageSerializer(obj.reply_to, read_only=True).data
        return None


class MessageCreateSerializer(serializers.ModelSerializer):
    """Message creation serializer"""
    class Meta:
        model = Message
        fields = ['chat_room', 'content', 'message_type', 'media_urls', 'reply_to']


class MessageStatusSerializer(serializers.ModelSerializer):
    """Message status serializer"""
    message = MessageSerializer(read_only=True)
    recipient = ChatUserMinimalSerializer(read_only=True)
    
    class Meta:
        model = MessageStatus
        fields = ['id', 'message', 'recipient', 'status', 'read_at']


class ChatRoomSerializer(serializers.ModelSerializer):
    """Chat room serializer"""
    participants = ChatRoomParticipantSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = [
            'id', 'name', 'room_type', 'participants', 'last_message',
            'unread_count', 'created_at', 'updated_at'
        ]
    
    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-created_at').first()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None
    
    def get_unread_count(self, obj):
        # This would be calculated based on current user
        return 0


class ChatRoomCreateSerializer(serializers.ModelSerializer):
    """Chat room creation serializer"""
    class Meta:
        model = ChatRoom
        fields = ['name', 'room_type']


class ContactSerializer(serializers.ModelSerializer):
    """Contact serializer"""
    chat_user = ChatUserMinimalSerializer(read_only=True)
    is_favorite = serializers.SerializerMethodField()
    is_blocked = serializers.SerializerMethodField()
    
    class Meta:
        model = Contact
        fields = [
            'id', 'chat_user', 'is_favorite', 'is_blocked',
            'created_at', 'updated_at'
        ]
    
    def get_is_favorite(self, obj):
        return getattr(obj, 'is_favorite', False)
    
    def get_is_blocked(self, obj):
        return getattr(obj, 'is_blocked', False)


class ContactCreateSerializer(serializers.ModelSerializer):
    """Contact creation serializer"""
    class Meta:
        model = Contact
        fields = ['chat_user']


class ChatNotificationSerializer(serializers.ModelSerializer):
    """Chat notification serializer"""
    sender = ChatUserMinimalSerializer(read_only=True)
    recipient = ChatUserMinimalSerializer(read_only=True)
    
    class Meta:
        model = ChatNotification
        fields = [
            'id', 'sender', 'recipient', 'notification_type',
            'title', 'message', 'is_read', 'created_at'
        ]


class ChatNotificationCreateSerializer(serializers.ModelSerializer):
    """Chat notification creation serializer"""
    class Meta:
        model = ChatNotification
        fields = ['recipient', 'notification_type', 'title', 'message']


class ChatUserStatusSerializer(serializers.ModelSerializer):
    """Chat user status serializer"""
    class Meta:
        model = ChatUser
        fields = ['id', 'is_online', 'last_seen']


class ContactFavoriteSerializer(serializers.ModelSerializer):
    """Contact favorite serializer"""
    class Meta:
        model = Contact
        fields = ['id', 'is_favorite']


class ContactBlockSerializer(serializers.ModelSerializer):
    """Contact block serializer"""
    class Meta:
        model = Contact
        fields = ['id', 'is_blocked']


class MessageReplySerializer(serializers.ModelSerializer):
    """Message reply serializer"""
    class Meta:
        model = Message
        fields = ['id', 'reply_to']


class MessageSearchSerializer(serializers.ModelSerializer):
    """Message search serializer"""
    sender = ChatUserMinimalSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'content', 'sender', 'created_at']


class UserSearchSerializer(serializers.ModelSerializer):
    """User search serializer"""
    chat_profile = ChatUserMinimalSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'chat_profile'] 