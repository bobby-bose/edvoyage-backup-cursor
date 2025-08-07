import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class ChatUser(models.Model):
    """Chat User model extending the base User model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chat_profile')
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)
    profile_image = models.URLField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    specialization = models.CharField(max_length=100, blank=True, help_text="Medical specialization")
    institution = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=100, blank=True, help_text="MBBS Student, Intern, GP, etc.")
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chat_users'
        verbose_name = 'Chat User'
        verbose_name_plural = 'Chat Users'

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username


class ChatRoom(models.Model):
    """Chat Room model for direct and group chats"""
    ROOM_TYPES = (
        ('direct', 'Direct'),
        ('group', 'Group'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, blank=True, help_text="For group chats")
    type = models.CharField(max_length=10, choices=ROOM_TYPES, default='direct')
    created_by = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='created_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chat_rooms'
        verbose_name = 'Chat Room'
        verbose_name_plural = 'Chat Rooms'

    def __str__(self):
        return f"{self.name} ({self.type})" if self.name else f"Room {self.id}"


class ChatRoomParticipant(models.Model):
    """Chat Room Participant model for room membership"""
    PARTICIPANT_ROLES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='room_participations')
    role = models.CharField(max_length=10, choices=PARTICIPANT_ROLES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'chat_room_participants'
        verbose_name = 'Chat Room Participant'
        verbose_name_plural = 'Chat Room Participants'
        unique_together = ('room', 'user')

    def __str__(self):
        return f"{self.user.user.username} in {self.room.name}"


class Message(models.Model):
    """Message model for chat messages"""
    MESSAGE_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
        ('audio', 'Audio'),
        ('video', 'Video'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    media_url = models.URLField(max_length=500, blank=True, null=True)
    file_name = models.CharField(max_length=200, blank=True, null=True)
    file_size = models.IntegerField(blank=True, null=True)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    is_edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chat_messages'
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender.user.username} in {self.room.name}"


class MessageStatus(models.Model):
    """Message Status model for tracking message delivery"""
    STATUS_CHOICES = (
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='statuses')
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='message_statuses')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chat_message_status'
        verbose_name = 'Message Status'
        verbose_name_plural = 'Message Statuses'
        unique_together = ('message', 'user')

    def __str__(self):
        return f"{self.message.id} - {self.user.user.username} - {self.status}"


class Contact(models.Model):
    """Contact model for user contacts"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='contacts')
    contact = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='contacted_by')
    nickname = models.CharField(max_length=100, blank=True, null=True)
    is_favorite = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chat_contacts'
        verbose_name = 'Chat Contact'
        verbose_name_plural = 'Chat Contacts'
        unique_together = ('user', 'contact')

    def __str__(self):
        return f"{self.user.user.username} -> {self.contact.user.username}"


class ChatNotification(models.Model):
    """Chat Notification model for real-time notifications"""
    NOTIFICATION_TYPES = (
        ('new_message', 'New Message'),
        ('message_reply', 'Message Reply'),
        ('contact_request', 'Contact Request'),
        ('group_invite', 'Group Invite'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_notifications'
        verbose_name = 'Chat Notification'
        verbose_name_plural = 'Chat Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.type} notification for {self.user.user.username}"
