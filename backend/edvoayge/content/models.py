from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

User = get_user_model()

class ContentCategory(models.Model):
    """Model for organizing content into categories"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#FF5733')  # Hex color
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Content Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def content_count(self):
        return self.contents.count()

class Content(models.Model):
    """Main content model"""
    CONTENT_TYPES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
        ('image', 'Image'),
        ('presentation', 'Presentation'),
        ('ebook', 'E-Book'),
        ('infographic', 'Infographic'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES, default='article')
    category = models.ForeignKey(ContentCategory, on_delete=models.CASCADE, related_name='contents')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_contents')
    
    # Content details
    file_url = models.URLField(blank=True, help_text='URL to the content file')
    file_size = models.PositiveIntegerField(null=True, blank=True, help_text='File size in bytes')
    duration = models.PositiveIntegerField(null=True, blank=True, help_text='Duration in seconds (for video/audio)')
    thumbnail_url = models.URLField(blank=True, help_text='URL to thumbnail image')
    
    # Content properties
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_public = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    
    # SEO and metadata
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    keywords = models.TextField(blank=True, help_text='Comma-separated keywords')
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    rating_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        return self.status == 'published' and self.is_public

    @property
    def tags_list(self):
        return [tag.name for tag in self.tags.all()]

class ContentTag(models.Model):
    """Model for content tagging"""
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#33FF57')  # Hex color
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def content_count(self):
        return self.contents.count()

class ContentView(models.Model):
    """Model for tracking content views"""
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_views', null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    view_duration = models.PositiveIntegerField(null=True, blank=True, help_text='View duration in seconds')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.content.title} - {self.created_at}"

class ContentRating(models.Model):
    """Model for content ratings"""
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_ratings')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 to 5'
    )
    review = models.TextField(blank=True)
    is_helpful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['content', 'user']

    def __str__(self):
        return f"{self.content.title} - {self.user.username} - {self.rating}"

    def save(self, *args, **kwargs):
        # Update content average rating
        super().save(*args, **kwargs)
        self.update_content_rating()

    def update_content_rating(self):
        """Update content average rating"""
        ratings = ContentRating.objects.filter(content=self.content)
        if ratings.exists():
            avg_rating = ratings.aggregate(avg=models.Avg('rating'))['avg']
            self.content.average_rating = round(avg_rating, 2)
            self.content.rating_count = ratings.count()
            self.content.save()

class ContentComment(models.Model):
    """Model for content comments"""
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.content.title} - {self.user.username} - {self.comment[:50]}"

    @property
    def is_reply(self):
        return self.parent is not None

    @property
    def replies_count(self):
        return self.replies.count()

class ContentShare(models.Model):
    """Model for content sharing"""
    SHARE_TYPES = [
        ('link', 'Link'),
        ('email', 'Email'),
        ('social', 'Social Media'),
        ('embed', 'Embed'),
    ]

    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='shares')
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_shares_sent')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_shares_received', null=True, blank=True)
    share_type = models.CharField(max_length=10, choices=SHARE_TYPES)
    message = models.TextField(blank=True)
    share_url = models.URLField(blank=True)
    is_viewed = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.content.title} shared by {self.shared_by.username}"

class ContentDownload(models.Model):
    """Model for tracking content downloads"""
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='downloads')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_downloads', null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    download_url = models.URLField()
    file_size = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.content.title} - {self.created_at}"

class ContentBookmark(models.Model):
    """Model for content bookmarks"""
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_bookmarks')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['content', 'user']

    def __str__(self):
        return f"{self.content.title} bookmarked by {self.user.username}"

class ContentAnalytics(models.Model):
    """Model for detailed content analytics"""
    ACTION_TYPES = [
        ('view', 'View'),
        ('download', 'Download'),
        ('share', 'Share'),
        ('rate', 'Rate'),
        ('comment', 'Comment'),
        ('bookmark', 'Bookmark'),
    ]

    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='analytics')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_analytics', null=True, blank=True)
    action_type = models.CharField(max_length=15, choices=ACTION_TYPES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    metadata = models.JSONField(default=dict, blank=True, help_text='Additional analytics data')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Content Analytics'

    def __str__(self):
        return f"{self.content.title} - {self.action_type} - {self.created_at}"

# Many-to-many relationships
class ContentTagThrough(models.Model):
    """Through model for content-tag relationships"""
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    tag = models.ForeignKey(ContentTag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['content', 'tag']

    def __str__(self):
        return f"{self.content.title} - {self.tag.name}"

# Add many-to-many relationships
Content.tags = models.ManyToManyField(ContentTag, through=ContentTagThrough, related_name='contents')


class Feed(models.Model):
    user_name = models.CharField(max_length=100)
    avatar_url = models.URLField()
    date_posted = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        ordering = ['-date_posted']
        verbose_name = 'Feed'
        verbose_name_plural = 'Feeds'

    def __str__(self):
        return f"{self.title} by {self.user_name}"
