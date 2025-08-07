import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    """Post model for Cavity app"""
    POST_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('link', 'Link'),
        ('poll', 'Poll'),
    ]
    
    YEAR_CHOICES = [
        ('NEET UG 2025', 'NEET UG 2025'),
        ('NEET UG 2024', 'NEET UG 2024'),
        ('NEET UG 2023', 'NEET UG 2023'),
        ('NEET PG 2025', 'NEET PG 2025'),
        ('NEET PG 2024', 'NEET PG 2024'),
        ('NEET PG 2023', 'NEET PG 2023'),
        ('MBBS 1st Year', 'MBBS 1st Year'),
        ('MBBS 2nd Year', 'MBBS 2nd Year'),
        ('MBBS 3rd Year', 'MBBS 3rd Year'),
        ('MBBS 4th Year', 'MBBS 4th Year'),
        ('MBBS (House Surgeon)', 'MBBS (House Surgeon)'),
        ('MBBS PG 1st year', 'MBBS PG 1st year'),
        ('MBBS PG 2nd Year', 'MBBS PG 2nd Year'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cavity_posts')
    content = models.TextField()
    year = models.CharField(max_length=50, choices=YEAR_CHOICES, default='NEET UG 2025', verbose_name="Year")
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='text')
    media_urls = models.JSONField(default=list, blank=True)
    is_anonymous = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    edit_history = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cavity_posts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}"

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def share_count(self):
        return self.shares.count()


class PostLike(models.Model):
    """Post like model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cavity_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cavity_post_likes'
        unique_together = ['post', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"


class Comment(models.Model):
    """Comment model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cavity_comments')
    content = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_edited = models.BooleanField(default=False)
    edit_history = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cavity_comments'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}"

    @property
    def like_count(self):
        return self.likes.count()


class CommentLike(models.Model):
    """Comment like model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cavity_comment_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cavity_comment_likes'
        unique_together = ['comment', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes comment {self.comment.id}"


class PostShare(models.Model):
    """Post share model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cavity_shares')
    share_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cavity_post_shares'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} shared {self.post.id}"


class Notification(models.Model):
    """Notification model"""
    NOTIFICATION_TYPES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('share', 'Share'),
        ('follow', 'Follow'),
        ('mention', 'Mention'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cavity_notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cavity_sent_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cavity_notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username}: {self.notification_type}"


class UserFollow(models.Model):
    """User follow model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cavity_following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cavity_followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cavity_user_follows'
        unique_together = ['follower', 'following']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
