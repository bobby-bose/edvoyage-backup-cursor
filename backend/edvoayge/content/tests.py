from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import (
    Content, ContentCategory, ContentTag, ContentView, ContentRating,
    ContentComment, ContentShare, ContentDownload, ContentBookmark, ContentAnalytics
)
from .serializers import (
    ContentSerializer, ContentListSerializer, ContentCreateSerializer,
    ContentCategorySerializer, ContentTagSerializer
)
import json
from datetime import datetime, timedelta
from decimal import Decimal

User = get_user_model()

class ContentCategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_category_creation(self):
        """Test content category creation"""
        category = ContentCategory.objects.create(
            name='Test Category',
            description='Test Description',
            color='#FF5733',
            icon='test-icon'
        )
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.description, 'Test Description')
        self.assertEqual(category.color, '#FF5733')
        self.assertEqual(category.icon, 'test-icon')
        self.assertTrue(category.is_active)

    def test_category_str_representation(self):
        """Test category string representation"""
        category = ContentCategory.objects.create(name='Test Category')
        self.assertEqual(str(category), 'Test Category')

    def test_category_content_count(self):
        """Test category content count property"""
        category = ContentCategory.objects.create(name='Test Category')
        content = Content.objects.create(
            title='Test Content',
            description='Test Description',
            category=category,
            author=self.user
        )
        self.assertEqual(category.content_count, 1)

class ContentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = ContentCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )

    def test_content_creation(self):
        """Test content creation with all required fields"""
        content = Content.objects.create(
            title='Test Content',
            description='Test Description',
            content_type='article',
            category=self.category,
            author=self.user,
            file_url='https://example.com/file.pdf',
            file_size=1024,
            duration=300,
            thumbnail_url='https://example.com/thumb.jpg',
            status='draft',
            is_public=False,
            is_featured=False,
            is_premium=False,
            meta_title='Test Meta Title',
            meta_description='Test Meta Description',
            keywords='test, content, article'
        )
        self.assertEqual(content.title, 'Test Content')
        self.assertEqual(content.category, self.category)
        self.assertEqual(content.author, self.user)
        self.assertEqual(content.content_type, 'article')
        self.assertEqual(content.status, 'draft')
        self.assertFalse(content.is_public)
        self.assertFalse(content.is_featured)
        self.assertFalse(content.is_premium)

    def test_content_str_representation(self):
        """Test content string representation"""
        content = Content.objects.create(
            title='Test Content',
            description='Test Description',
            category=self.category,
            author=self.user
        )
        self.assertEqual(str(content), 'Test Content')

    def test_content_is_active(self):
        """Test content is_active property"""
        content = Content.objects.create(
            title='Test Content',
            description='Test Description',
            category=self.category,
            author=self.user,
            status='published',
            is_public=True
        )
        self.assertTrue(content.is_active)

    def test_content_publish(self):
        """Test content publishing sets published_at"""
        content = Content.objects.create(
            title='Test Content',
            description='Test Description',
            category=self.category,
            author=self.user,
            status='draft'
        )
        self.assertIsNone(content.published_at)
        
        content.status = 'published'
        content.save()
        self.assertIsNotNone(content.published_at)

    def test_content_tags_list(self):
        """Test content tags_list property"""
        content = Content.objects.create(
            title='Test Content',
            description='Test Description',
            category=self.category,
            author=self.user
        )
        tag1 = ContentTag.objects.create(name='Tag1', color='#FF5733')
        tag2 = ContentTag.objects.create(name='Tag2', color='#33FF57')
        content.tags.add(tag1, tag2)
        
        self.assertEqual(len(content.tags_list), 2)
        self.assertIn('Tag1', content.tags_list)
        self.assertIn('Tag2', content.tags_list)

class ContentTagModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_tag_creation(self):
        """Test content tag creation"""
        tag = ContentTag.objects.create(
            name='Test Tag',
            color='#33FF57',
            description='Test Description'
        )
        self.assertEqual(tag.name, 'Test Tag')
        self.assertEqual(tag.color, '#33FF57')
        self.assertEqual(tag.description, 'Test Description')

    def test_tag_str_representation(self):
        """Test tag string representation"""
        tag = ContentTag.objects.create(name='Test Tag')
        self.assertEqual(str(tag), 'Test Tag')

    def test_tag_content_count(self):
        """Test tag content count property"""
        tag = ContentTag.objects.create(name='Test Tag')
        category = ContentCategory.objects.create(name='Test Category')
        content = Content.objects.create(
            title='Test Content',
            description='Test Description',
            category=category,
            author=self.user
        )
        content.tags.add(tag)
        self.assertEqual(tag.content_count, 1)

class ContentViewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = ContentCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )
        self.content = Content.objects.create(
            title='Test Content',
            description='Test Description',
            category=self.category,
            author=self.user
        )

    def test_view_creation(self):
        """Test content view creation"""
        view = ContentView.objects.create(
            content=self.content,
            user=self.user,
            ip_address='127.0.0.1',
            user_agent='Test User Agent',
            referrer='https://example.com',
            session_id='test-session',
            view_duration=60
        )
        self.assertEqual(view.content, self.content)
        self.assertEqual(view.user, self.user)
        self.assertEqual(view.ip_address, '127.0.0.1')
        self.assertEqual(view.view_duration, 60)

    def test_view_str_representation(self):
        """Test view string representation"""
        view = ContentView.objects.create(
            content=self.content,
            user=self.user
        )
        self.assertEqual(str(view), f'{self.content.title} - {view.created_at}')

class ContentRatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = ContentCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )
        self.content = Content.objects.create(
            title='Test Content',
            description='Test Description',
            category=self.category,
            author=self.user
        )

    def test_rating_creation(self):
        """Test content rating creation"""
        rating = ContentRating.objects.create(
            content=self.content,
            user=self.user,
            rating=5,
            review='Great content!',
            is_helpful=True
        )
        self.assertEqual(rating.content, self.content)
        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.rating, 5)
        self.assertEqual(rating.review, 'Great content!')
        self.assertTrue(rating.is_helpful)

    def test_rating_str_representation(self):
        """Test rating string representation"""
        rating = ContentRating.objects.create(
            content=self.content,
            user=self.user,
            rating=4
        )
        self.assertEqual(str(rating), f'{self.content.title} - {self.user.username} - 4')

    def test_rating_update_content_average(self):
        """Test rating updates content average rating"""
        rating1 = ContentRating.objects.create(
            content=self.content,
            user=self.user,
            rating=5
        )
        rating2 = ContentRating.objects.create(
            content=self.content,
            user=User.objects.create_user(username='user2', email='user2@example.com'),
            rating=3
        )
        
        self.content.refresh_from_db()
        self.assertEqual(self.content.average_rating, Decimal('4.00'))
        self.assertEqual(self.content.rating_count, 2)

class ContentCommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = ContentCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )
        self.content = Content.objects.create(
            title='Test Content',
            description='Test Description',
            category=self.category,
            author=self.user
        )

    def test_comment_creation(self):
        """Test content comment creation"""
        comment = ContentComment.objects.create(
            content=self.content,
            user=self.user,
            comment='Great article!',
            is_approved=True
        )
        self.assertEqual(comment.content, self.content)
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.comment, 'Great article!')
        self.assertTrue(comment.is_approved)
        self.assertFalse(comment.is_edited)

    def test_comment_str_representation(self):
        """Test comment string representation"""
        comment = ContentComment.objects.create(
            content=self.content,
            user=self.user,
            comment='Test comment'
        )
        self.assertEqual(str(comment), f'{self.content.title} - {self.user.username} - Test comment')

    def test_comment_reply(self):
        """Test comment reply functionality"""
        parent_comment = ContentComment.objects.create(
            content=self.content,
            user=self.user,
            comment='Parent comment'
        )
        reply = ContentComment.objects.create(
            content=self.content,
            user=self.user,
            parent=parent_comment,
            comment='Reply to parent'
        )
        
        self.assertTrue(reply.is_reply)
        self.assertEqual(reply.parent, parent_comment)
        self.assertEqual(parent_comment.replies_count, 1)

class ContentAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = ContentCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )
        self.content = Content.objects.create(
            title='Test Content',
            description='Test Description',
            category=self.category,
            author=self.user,
            status='published',
            is_public=True
        )
        self.client.force_authenticate(user=self.user)

    def test_get_contents_list(self):
        """Test getting list of contents"""
        url = reverse('content-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_content_detail(self):
        """Test getting content detail"""
        url = reverse('content-detail', args=[self.content.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Content')

    def test_create_content(self):
        """Test creating a new content"""
        url = reverse('content-list')
        data = {
            'title': 'New Content',
            'description': 'New Description',
            'content_type': 'article',
            'category_id': self.category.id,
            'file_url': 'https://example.com/file.pdf',
            'file_size': 1024,
            'duration': 300,
            'thumbnail_url': 'https://example.com/thumb.jpg',
            'status': 'draft',
            'is_public': False,
            'is_featured': False,
            'is_premium': False,
            'meta_title': 'New Meta Title',
            'meta_description': 'New Meta Description',
            'keywords': 'new, content, article'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Content.objects.count(), 2)

    def test_update_content(self):
        """Test updating a content"""
        url = reverse('content-detail', args=[self.content.id])
        data = {
            'title': 'Updated Content',
            'description': 'Updated Description',
            'content_type': 'video',
            'category_id': self.category.id,
            'file_url': 'https://example.com/video.mp4',
            'file_size': 2048,
            'duration': 600,
            'thumbnail_url': 'https://example.com/thumb2.jpg',
            'status': 'published',
            'is_public': True,
            'is_featured': True,
            'is_premium': True,
            'meta_title': 'Updated Meta Title',
            'meta_description': 'Updated Meta Description',
            'keywords': 'updated, content, video'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.content.refresh_from_db()
        self.assertEqual(self.content.title, 'Updated Content')

    def test_delete_content(self):
        """Test deleting a content"""
        url = reverse('content-detail', args=[self.content.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Content.objects.count(), 0)

    def test_view_content(self):
        """Test viewing content"""
        url = reverse('content-view', args=[self.content.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContentView.objects.count(), 1)

    def test_rate_content(self):
        """Test rating content"""
        url = reverse('content-rate', args=[self.content.id])
        data = {
            'content_id': self.content.id,
            'rating': 5,
            'review': 'Excellent content!',
            'is_helpful': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ContentRating.objects.count(), 1)

    def test_comment_content(self):
        """Test commenting on content"""
        url = reverse('content-comment', args=[self.content.id])
        data = {
            'content_id': self.content.id,
            'comment': 'Great article!'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ContentComment.objects.count(), 1)

    def test_share_content(self):
        """Test sharing content"""
        url = reverse('content-share', args=[self.content.id])
        data = {
            'content_id': self.content.id,
            'share_type': 'link',
            'message': 'Check out this content!'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ContentShare.objects.count(), 1)

    def test_download_content(self):
        """Test downloading content"""
        url = reverse('content-download', args=[self.content.id])
        data = {
            'content_id': self.content.id,
            'download_url': 'https://example.com/download.pdf',
            'file_size': 1024
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ContentDownload.objects.count(), 1)

    def test_bookmark_content(self):
        """Test bookmarking content"""
        url = reverse('content-bookmark', args=[self.content.id])
        data = {
            'content_id': self.content.id,
            'notes': 'Save for later'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ContentBookmark.objects.count(), 1)

    def test_search_contents(self):
        """Test searching contents"""
        url = reverse('content-search')
        response = self.client.get(url, {'q': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_content_statistics(self):
        """Test getting content statistics"""
        url = reverse('content-statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_content', response.data)

    def test_featured_contents(self):
        """Test getting featured contents"""
        url = reverse('content-featured')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recent_contents(self):
        """Test getting recent contents"""
        url = reverse('content-recent')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_popular_contents(self):
        """Test getting popular contents"""
        url = reverse('content-popular')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ContentCategoryAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = ContentCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_categories_list(self):
        """Test getting list of categories"""
        url = reverse('content-category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_category_detail(self):
        """Test getting category detail"""
        url = reverse('content-category-detail', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Category')

    def test_create_category(self):
        """Test creating a new category"""
        url = reverse('content-category-list')
        data = {
            'name': 'New Category',
            'description': 'New Description',
            'color': '#33FF57',
            'icon': 'new-icon',
            'is_active': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContentCategory.objects.count(), 2)

    def test_update_category(self):
        """Test updating a category"""
        url = reverse('content-category-detail', args=[self.category.id])
        data = {
            'name': 'Updated Category',
            'description': 'Updated Description',
            'color': '#FF3357',
            'icon': 'updated-icon',
            'is_active': True
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')

    def test_delete_category(self):
        """Test deleting a category"""
        url = reverse('content-category-detail', args=[self.category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ContentCategory.objects.count(), 0)

    def test_category_contents(self):
        """Test getting contents in a category"""
        url = reverse('category-contents', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_statistics(self):
        """Test getting category statistics"""
        url = reverse('category-statistics', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ContentTagAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.tag = ContentTag.objects.create(
            name='Test Tag',
            color='#33FF57'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_tags_list(self):
        """Test getting list of tags"""
        url = reverse('content-tag-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_tag_detail(self):
        """Test getting tag detail"""
        url = reverse('content-tag-detail', args=[self.tag.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Tag')

    def test_create_tag(self):
        """Test creating a new tag"""
        url = reverse('content-tag-list')
        data = {
            'name': 'New Tag',
            'color': '#FF3357',
            'description': 'New Description'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContentTag.objects.count(), 2)

    def test_update_tag(self):
        """Test updating a tag"""
        url = reverse('content-tag-detail', args=[self.tag.id])
        data = {
            'name': 'Updated Tag',
            'color': '#FF5733',
            'description': 'Updated Description'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, 'Updated Tag')

    def test_delete_tag(self):
        """Test deleting a tag"""
        url = reverse('content-tag-detail', args=[self.tag.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ContentTag.objects.count(), 0)

    def test_tag_contents(self):
        """Test getting contents with this tag"""
        url = reverse('tag-contents', args=[self.tag.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ContentSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = ContentCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )
        self.content = Content.objects.create(
            title='Test Content',
            description='Test Description',
            category=self.category,
            author=self.user
        )

    def test_content_serializer(self):
        """Test content serializer"""
        serializer = ContentSerializer(self.content)
        data = serializer.data
        self.assertEqual(data['title'], 'Test Content')
        self.assertEqual(data['description'], 'Test Description')
        self.assertEqual(data['category']['name'], 'Test Category')

    def test_category_serializer(self):
        """Test category serializer"""
        serializer = ContentCategorySerializer(self.category)
        data = serializer.data
        self.assertEqual(data['name'], 'Test Category')
        self.assertEqual(data['color'], '#FF5733')

    def test_tag_serializer(self):
        """Test tag serializer"""
        tag = ContentTag.objects.create(
            name='Test Tag',
            color='#33FF57'
        )
        serializer = ContentTagSerializer(tag)
        data = serializer.data
        self.assertEqual(data['name'], 'Test Tag')
        self.assertEqual(data['color'], '#33FF57')

class ContentIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = ContentCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )

    def test_content_workflow(self):
        """Test complete content workflow"""
        # Create content
        content = Content.objects.create(
            title='Integration Test Content',
            description='Integration Test Description',
            category=self.category,
            author=self.user,
            status='published',
            is_public=True
        )
        
        # Create tag
        tag = ContentTag.objects.create(
            name='Test Tag',
            color='#33FF57'
        )
        content.tags.add(tag)
        
        # Create view
        view = ContentView.objects.create(
            content=content,
            user=self.user,
            ip_address='127.0.0.1',
            view_duration=60
        )
        
        # Create rating
        rating = ContentRating.objects.create(
            content=content,
            user=self.user,
            rating=5,
            review='Great content!'
        )
        
        # Create comment
        comment = ContentComment.objects.create(
            content=content,
            user=self.user,
            comment='Excellent article!'
        )
        
        # Create share
        share = ContentShare.objects.create(
            content=content,
            shared_by=self.user,
            share_type='link',
            message='Check this out!'
        )
        
        # Create download
        download = ContentDownload.objects.create(
            content=content,
            user=self.user,
            download_url='https://example.com/download.pdf',
            file_size=1024
        )
        
        # Create bookmark
        bookmark = ContentBookmark.objects.create(
            content=content,
            user=self.user,
            notes='Save for later'
        )
        
        # Verify workflow
        self.assertEqual(Content.objects.count(), 1)
        self.assertEqual(ContentView.objects.count(), 1)
        self.assertEqual(ContentRating.objects.count(), 1)
        self.assertEqual(ContentComment.objects.count(), 1)
        self.assertEqual(ContentShare.objects.count(), 1)
        self.assertEqual(ContentDownload.objects.count(), 1)
        self.assertEqual(ContentBookmark.objects.count(), 1)
        
        # Test relationships
        self.assertEqual(content.views.first(), view)
        self.assertEqual(content.ratings.first(), rating)
        self.assertEqual(content.comments.first(), comment)
        self.assertEqual(content.shares.first(), share)
        self.assertEqual(content.downloads.first(), download)
        self.assertEqual(content.bookmarks.first(), bookmark)
        self.assertEqual(content.tags.first(), tag)

class ContentPerformanceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = ContentCategory.objects.create(
            name='Test Category',
            color='#FF5733'
        )

    def test_bulk_content_creation(self):
        """Test bulk content creation performance"""
        contents = []
        for i in range(100):
            content = Content(
                title=f'Content {i}',
                description=f'Description {i}',
                category=self.category,
                author=self.user,
                status='draft'
            )
            contents.append(content)
        
        Content.objects.bulk_create(contents)
        self.assertEqual(Content.objects.count(), 100)

    def test_content_query_performance(self):
        """Test content query performance with select_related"""
        # Create multiple contents
        for i in range(50):
            Content.objects.create(
                title=f'Content {i}',
                description=f'Description {i}',
                category=self.category,
                author=self.user,
                status='published'
            )
        
        # Test query performance
        with self.assertNumQueries(1):  # Should use select_related
            contents = Content.objects.select_related('category', 'author').all()
            for content in contents:
                _ = content.category.name
                _ = content.author.username
