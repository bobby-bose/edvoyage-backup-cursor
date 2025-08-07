from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post, Comment, PostLike, CommentLike, PostShare, Notification, UserFollow

User = get_user_model()


class CavityModelsTestCase(TestCase):
    """Test cases for Cavity models"""

    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123',
            year_tag='1st year MBBS'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            year_tag='2nd year MBBS'
        )

    def test_user_creation(self):
        """Test user creation"""
        self.assertEqual(self.user1.username, 'testuser1')
        self.assertEqual(self.user1.year_tag, '1st year MBBS')
        self.assertTrue(self.user1.is_active)

    def test_post_creation(self):
        """Test post creation"""
        post = Post.objects.create(
            user=self.user1,
            content='Test post content',
            is_anonymous=False
        )
        self.assertEqual(post.user, self.user1)
        self.assertEqual(post.content, 'Test post content')
        self.assertFalse(post.is_anonymous)
        self.assertEqual(post.status, 'active')

    def test_comment_creation(self):
        """Test comment creation"""
        post = Post.objects.create(
            user=self.user1,
            content='Test post content'
        )
        comment = Comment.objects.create(
            post=post,
            user=self.user2,
            content='Test comment content'
        )
        self.assertEqual(comment.post, post)
        self.assertEqual(comment.user, self.user2)
        self.assertEqual(comment.content, 'Test comment content')

    def test_post_like_creation(self):
        """Test post like creation"""
        post = Post.objects.create(
            user=self.user1,
            content='Test post content'
        )
        like = PostLike.objects.create(
            post=post,
            user=self.user2,
        )
        self.assertEqual(like.post, post)
        self.assertEqual(like.user, self.user2)

    def test_comment_like_creation(self):
        """Test comment like creation"""
        post = Post.objects.create(
            user=self.user1,
            content='Test post content'
        )
        comment = Comment.objects.create(
            post=post,
            user=self.user2,
            content='Test comment content'
        )
        like = CommentLike.objects.create(
            comment=comment,
            user=self.user1,
        )
        self.assertEqual(like.comment, comment)
        self.assertEqual(like.user, self.user1)

    def test_post_share_creation(self):
        """Test post share creation"""
        post = Post.objects.create(
            user=self.user1,
            content='Test post content'
        )
        share = PostShare.objects.create(
            post=post,
            user=self.user2,
            platform='WhatsApp'
        )
        self.assertEqual(share.post, post)
        self.assertEqual(share.user, self.user2)
        self.assertEqual(share.platform, 'WhatsApp')

    def test_notification_creation(self):
        """Test notification creation"""
        notification = Notification.objects.create(
            user=self.user1,
            type='like',
            message='Test notification message',
            reference_id=self.user2.id,
            reference_type='user'
        )
        self.assertEqual(notification.user, self.user1)
        self.assertEqual(notification.type, 'like')
        self.assertEqual(notification.message, 'Test notification message')
        self.assertFalse(notification.is_read)

    def test_user_follow_creation(self):
        """Test user follow creation"""
        follow = UserFollow.objects.create(
            follower=self.user1,
            following=self.user2
        )
        self.assertEqual(follow.follower, self.user1)
        self.assertEqual(follow.following, self.user2)

    def test_post_properties(self):
        """Test post computed properties"""
        post = Post.objects.create(
            user=self.user1,
            content='Test post content'
        )
        
        # Create some likes
        PostLike.objects.create(post=post, user=self.user2)
        
        # Create some comments
        Comment.objects.create(post=post, user=self.user2, content='Test comment')
        
        # Create some shares
        PostShare.objects.create(post=post, user=self.user2, platform='WhatsApp')
        
        self.assertEqual(post.like_count, 1)
        self.assertEqual(post.comment_count, 1)
        self.assertEqual(post.share_count, 1)

    def test_comment_properties(self):
        """Test comment computed properties"""
        post = Post.objects.create(
            user=self.user1,
            content='Test post content'
        )
        comment = Comment.objects.create(
            post=post,
            user=self.user2,
            content='Test comment content'
        )
        
        # Create some likes
        CommentLike.objects.create(comment=comment, user=self.user1, is_active=True)
        
        # Create some replies
        Comment.objects.create(
            post=post,
            user=self.user1,
            parent_comment=comment,
            content='Test reply'
        )
        
        self.assertEqual(comment.like_count, 1)
        self.assertEqual(comment.replies_count, 1)


class CavityAPITestCase(APITestCase):
    """Test cases for Cavity API endpoints"""

    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123',
            year_tag='1st year MBBS'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            year_tag='2nd year MBBS'
        )
        self.client.force_authenticate(user=self.user1)

    def test_get_posts(self):
        """Test getting posts"""
        post = Post.objects.create(
            user=self.user1,
            content='Test post content'
        )
        
        response = self.client.get('/api/v1/cavity/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'Test post content')

    def test_create_post(self):
        """Test creating a post"""
        data = {
            'content': 'New test post content',
            'is_anonymous': False
        }
        
        response = self.client.post('/api/v1/cavity/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().content, 'New test post content')

    def test_get_users(self):
        """Test getting users"""
        response = self.client.get('/api/v1/cavity/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should exclude current user from list
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser2')

    def test_user_profile(self):
        """Test getting user profile"""
        response = self.client.get('/api/v1/cavity/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser1')
        self.assertEqual(response.data['year_tag'], '1st year MBBS')
