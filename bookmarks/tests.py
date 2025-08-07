import uuid
import json
from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    Bookmark,
    BookmarkCategory,
    BookmarkNote,
    BookmarkCollection,
    BookmarkShare,
    BookmarkAnalytics,
    BookmarkTag,
    BookmarkAccessLog,
)

User = get_user_model()


class BookmarkModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.category = BookmarkCategory.objects.create(
            user=self.user,
            name='Test Category',
            description='Test category description',
            color='#FF0000'
        )
        self.tag = BookmarkTag.objects.create(
            user=self.user,
            name='Test Tag',
            color='#00FF00'
        )

    def test_bookmark_creation(self):
        bookmark = Bookmark.objects.create(
            user=self.user,
            title='Test Bookmark',
            description='Test bookmark description',
            url='https://example.com',
            category=self.category
        )
        bookmark.tags.add(self.tag)
        
        self.assertEqual(bookmark.title, 'Test Bookmark')
        self.assertEqual(bookmark.user, self.user)
        self.assertEqual(bookmark.category, self.category)
        self.assertEqual(bookmark.access_count, 0)
        self.assertFalse(bookmark.is_favorite)
        self.assertFalse(bookmark.is_public)
        self.assertEqual(bookmark.status, 'active')
        self.assertIn(self.tag, bookmark.tags.all())

    def test_bookmark_str_representation(self):
        bookmark = Bookmark.objects.create(
            user=self.user,
            title='Test Bookmark',
            url='https://example.com'
        )
        self.assertEqual(str(bookmark), 'Test Bookmark')

    def test_bookmark_access_count_increment(self):
        bookmark = Bookmark.objects.create(
            user=self.user,
            title='Test Bookmark',
            url='https://example.com'
        )
        
        initial_count = bookmark.access_count
        bookmark.access_count += 1
        bookmark.save()
        
        updated_bookmark = Bookmark.objects.get(id=bookmark.id)
        self.assertEqual(updated_bookmark.access_count, initial_count + 1)

    def test_bookmark_favorite_toggle(self):
        bookmark = Bookmark.objects.create(
            user=self.user,
            title='Test Bookmark',
            url='https://example.com'
        )
        
        self.assertFalse(bookmark.is_favorite)
        bookmark.is_favorite = True
        bookmark.save()
        
        updated_bookmark = Bookmark.objects.get(id=bookmark.id)
        self.assertTrue(updated_bookmark.is_favorite)


class BookmarkCategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_category_creation(self):
        category = BookmarkCategory.objects.create(
            user=self.user,
            name='Test Category',
            description='Test category description',
            color='#FF0000',
            is_default=True
        )
        
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.user, self.user)
        self.assertTrue(category.is_default)
        self.assertEqual(category.color, '#FF0000')

    def test_category_str_representation(self):
        category = BookmarkCategory.objects.create(
            user=self.user,
            name='Test Category'
        )
        self.assertEqual(str(category), 'Test Category')

    def test_default_category_uniqueness(self):
        # Create first default category
        category1 = BookmarkCategory.objects.create(
            user=self.user,
            name='Category 1',
            is_default=True
        )
        
        # Create second default category
        category2 = BookmarkCategory.objects.create(
            user=self.user,
            name='Category 2',
            is_default=True
        )
        
        # The second category should automatically become default
        category1.refresh_from_db()
        self.assertFalse(category1.is_default)
        self.assertTrue(category2.is_default)


class BookmarkCollectionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_collection_creation(self):
        collection = BookmarkCollection.objects.create(
            user=self.user,
            name='Test Collection',
            description='Test collection description',
            is_public=True
        )
        
        self.assertEqual(collection.name, 'Test Collection')
        self.assertEqual(collection.user, self.user)
        self.assertTrue(collection.is_public)

    def test_collection_str_representation(self):
        collection = BookmarkCollection.objects.create(
            user=self.user,
            name='Test Collection'
        )
        self.assertEqual(str(collection), 'Test Collection')

    def test_collection_bookmark_relationship(self):
        collection = BookmarkCollection.objects.create(
            user=self.user,
            name='Test Collection'
        )
        
        bookmark = Bookmark.objects.create(
            user=self.user,
            title='Test Bookmark',
            url='https://example.com'
        )
        
        collection.bookmarks.add(bookmark)
        self.assertIn(bookmark, collection.bookmarks.all())


class BookmarkShareModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='testpass123'
        )
        self.bookmark = Bookmark.objects.create(
            user=self.user1,
            title='Test Bookmark',
            url='https://example.com'
        )

    def test_share_creation(self):
        share = BookmarkShare.objects.create(
            share_type='bookmark',
            shared_by=self.user1,
            shared_with=self.user2,
            share_code=str(uuid.uuid4()),
            is_active=True
        )
        
        self.assertEqual(share.share_type, 'bookmark')
        self.assertEqual(share.shared_by, self.user1)
        self.assertEqual(share.shared_with, self.user2)
        self.assertTrue(share.is_active)

    def test_share_str_representation(self):
        share = BookmarkShare.objects.create(
            share_type='bookmark',
            shared_by=self.user1,
            shared_with=self.user2,
            share_code=str(uuid.uuid4())
        )
        expected = f"Share by {self.user1.email} to {self.user2.email}"
        self.assertEqual(str(share), expected)

    def test_share_expiry(self):
        share = BookmarkShare.objects.create(
            share_type='bookmark',
            shared_by=self.user1,
            shared_with=self.user2,
            share_code=str(uuid.uuid4()),
            expires_at=timezone.now() + timedelta(days=7)
        )
        
        self.assertIsNotNone(share.expires_at)
        self.assertTrue(share.is_active)


class BookmarkAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        
        self.category = BookmarkCategory.objects.create(
            user=self.user,
            name='Test Category',
            description='Test category description',
            color='#FF0000'
        )
        
        self.tag = BookmarkTag.objects.create(
            user=self.user,
            name='Test Tag',
            color='#00FF00'
        )

    def test_create_bookmark(self):
        url = reverse('bookmark-list')
        data = {
            'title': 'Test Bookmark',
            'description': 'Test bookmark description',
            'url': 'https://example.com',
            'category': self.category.id,
            'tags': [self.tag.id]
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        bookmark = Bookmark.objects.get(id=response.data['id'])
        self.assertEqual(bookmark.title, 'Test Bookmark')
        self.assertEqual(bookmark.user, self.user)
        self.assertEqual(bookmark.category, self.category)

    def test_list_bookmarks(self):
        Bookmark.objects.create(
            user=self.user,
            title='Bookmark 1',
            url='https://example1.com',
            category=self.category
        )
        Bookmark.objects.create(
            user=self.user,
            title='Bookmark 2',
            url='https://example2.com',
            category=self.category
        )
        
        url = reverse('bookmark-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_bookmark(self):
        bookmark = Bookmark.objects.create(
            user=self.user,
            title='Test Bookmark',
            url='https://example.com',
            category=self.category
        )
        
        url = reverse('bookmark-detail', args=[bookmark.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Bookmark')

    def test_update_bookmark(self):
        bookmark = Bookmark.objects.create(
            user=self.user,
            title='Original Title',
            url='https://example.com',
            category=self.category
        )
        
        url = reverse('bookmark-detail', args=[bookmark.id])
        data = {
            'title': 'Updated Title',
            'description': 'Updated description',
            'url': 'https://updated.com',
            'category': self.category.id
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        bookmark.refresh_from_db()
        self.assertEqual(bookmark.title, 'Updated Title')

    def test_delete_bookmark(self):
        bookmark = Bookmark.objects.create(
            user=self.user,
            title='Test Bookmark',
            url='https://example.com',
            category=self.category
        )
        
        url = reverse('bookmark-detail', args=[bookmark.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Bookmark.objects.filter(id=bookmark.id).exists())

    def test_bookmark_toggle_favorite(self):
        bookmark = Bookmark.objects.create(
            user=self.user,
            title='Test Bookmark',
            url='https://example.com',
            category=self.category
        )
        
        url = reverse('bookmark-toggle-favorite', args=[bookmark.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        bookmark.refresh_from_db()
        self.assertTrue(bookmark.is_favorite)

    def test_bookmark_record_access(self):
        bookmark = Bookmark.objects.create(
            user=self.user,
            title='Test Bookmark',
            url='https://example.com',
            category=self.category
        )
        
        initial_count = bookmark.access_count
        url = reverse('bookmark-record-access', args=[bookmark.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        bookmark.refresh_from_db()
        self.assertEqual(bookmark.access_count, initial_count + 1)

    def test_bookmark_search(self):
        Bookmark.objects.create(
            user=self.user,
            title='Python Tutorial',
            description='Learn Python programming',
            url='https://python.org',
            category=self.category
        )
        Bookmark.objects.create(
            user=self.user,
            title='Django Documentation',
            description='Django web framework docs',
            url='https://django.org',
            category=self.category
        )
        
        url = reverse('bookmark-list')
        response = self.client.get(url, {'search': 'Python'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('Python', response.data['results'][0]['title'])

    def test_bookmark_filter_by_category(self):
        category2 = BookmarkCategory.objects.create(
            user=self.user,
            name='Category 2',
            color='#00FF00'
        )
        
        Bookmark.objects.create(
            user=self.user,
            title='Bookmark 1',
            url='https://example1.com',
            category=self.category
        )
        Bookmark.objects.create(
            user=self.user,
            title='Bookmark 2',
            url='https://example2.com',
            category=category2
        )
        
        url = reverse('bookmark-list')
        response = self.client.get(url, {'category': self.category.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['category'], self.category.id)


class BookmarkCategoryAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')

    def test_create_category(self):
        url = reverse('bookmarkcategory-list')
        data = {
            'name': 'Test Category',
            'description': 'Test category description',
            'color': '#FF0000',
            'is_default': True
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        category = BookmarkCategory.objects.get(id=response.data['id'])
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.user, self.user)

    def test_list_categories(self):
        BookmarkCategory.objects.create(
            user=self.user,
            name='Category 1',
            color='#FF0000'
        )
        BookmarkCategory.objects.create(
            user=self.user,
            name='Category 2',
            color='#00FF00'
        )
        
        url = reverse('bookmarkcategory-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_update_category(self):
        category = BookmarkCategory.objects.create(
            user=self.user,
            name='Original Name',
            color='#FF0000'
        )
        
        url = reverse('bookmarkcategory-detail', args=[category.id])
        data = {
            'name': 'Updated Name',
            'description': 'Updated description',
            'color': '#00FF00'
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        category.refresh_from_db()
        self.assertEqual(category.name, 'Updated Name')


class BookmarkCollectionAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')

    def test_create_collection(self):
        url = reverse('bookmarkcollection-list')
        data = {
            'name': 'Test Collection',
            'description': 'Test collection description',
            'is_public': True
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        collection = BookmarkCollection.objects.get(id=response.data['id'])
        self.assertEqual(collection.name, 'Test Collection')
        self.assertEqual(collection.user, self.user)

    def test_add_bookmark_to_collection(self):
        collection = BookmarkCollection.objects.create(
            user=self.user,
            name='Test Collection'
        )
        bookmark = Bookmark.objects.create(
            user=self.user,
            title='Test Bookmark',
            url='https://example.com'
        )
        
        url = reverse('collection-add-bookmark', args=[collection.id])
        data = {'bookmark_id': bookmark.id}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn(bookmark, collection.bookmarks.all())

    def test_remove_bookmark_from_collection(self):
        collection = BookmarkCollection.objects.create(
            user=self.user,
            name='Test Collection'
        )
        bookmark = Bookmark.objects.create(
            user=self.user,
            title='Test Bookmark',
            url='https://example.com'
        )
        collection.bookmarks.add(bookmark)
        
        url = reverse('collection-remove-bookmark', args=[collection.id])
        data = {'bookmark_id': bookmark.id}
        
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertNotIn(bookmark, collection.bookmarks.all())


class BookmarkShareAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='testpass123'
        )
        self.refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        
        self.bookmark = Bookmark.objects.create(
            user=self.user1,
            title='Test Bookmark',
            url='https://example.com'
        )

    def test_share_bookmark(self):
        url = reverse('bookmark-share', args=[self.bookmark.id])
        data = {
            'shared_with': self.user2.id,
            'share_type': 'bookmark',
            'permissions': ['read'],
            'expires_at': (timezone.now() + timedelta(days=7)).isoformat()
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        share = BookmarkShare.objects.get(id=response.data['id'])
        self.assertEqual(share.shared_by, self.user1)
        self.assertEqual(share.shared_with, self.user2)
        self.assertEqual(share.share_type, 'bookmark')

    def test_unshare_bookmark(self):
        share = BookmarkShare.objects.create(
            share_type='bookmark',
            shared_by=self.user1,
            shared_with=self.user2,
            share_code=str(uuid.uuid4()),
            is_active=True
        )
        
        url = reverse('bookmark-unshare', args=[self.bookmark.id])
        data = {'share_id': share.id}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        share.refresh_from_db()
        self.assertFalse(share.is_active)


class BookmarkAnalyticsAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        
        self.bookmark = Bookmark.objects.create(
            user=self.user,
            title='Test Bookmark',
            url='https://example.com'
        )

    def test_record_bookmark_access(self):
        url = reverse('bookmark-record-access', args=[self.bookmark.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if access log was created
        access_log = BookmarkAccessLog.objects.filter(
            bookmark=self.bookmark,
            user=self.user
        ).first()
        self.assertIsNotNone(access_log)
        self.assertEqual(access_log.access_type, 'view')

    def test_get_bookmark_analytics(self):
        # Create some access logs
        BookmarkAccessLog.objects.create(
            bookmark=self.bookmark,
            user=self.user,
            access_type='view',
            ip_address='127.0.0.1'
        )
        
        url = reverse('bookmarkanalytics-detail', args=[self.bookmark.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_count', response.data)


class BookmarkSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.category = BookmarkCategory.objects.create(
            user=self.user,
            name='Test Category',
            color='#FF0000'
        )
        self.tag = BookmarkTag.objects.create(
            user=self.user,
            name='Test Tag',
            color='#00FF00'
        )

    def test_bookmark_serializer_creation(self):
        from .serializers import BookmarkSerializer
        
        data = {
            'title': 'Test Bookmark',
            'description': 'Test description',
            'url': 'https://example.com',
            'category': self.category.id,
            'tags': [self.tag.id],
            'is_favorite': True,
            'is_public': False
        }
        
        serializer = BookmarkSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        bookmark = serializer.save(user=self.user)
        self.assertEqual(bookmark.title, 'Test Bookmark')
        self.assertEqual(bookmark.user, self.user)
        self.assertEqual(bookmark.category, self.category)
        self.assertIn(self.tag, bookmark.tags.all())

    def test_bookmark_serializer_validation(self):
        from .serializers import BookmarkSerializer
        
        # Test invalid URL
        data = {
            'title': 'Test Bookmark',
            'url': 'invalid-url'
        }
        
        serializer = BookmarkSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('url', serializer.errors)

    def test_category_serializer(self):
        from .serializers import BookmarkCategorySerializer
        
        data = {
            'name': 'Test Category',
            'description': 'Test description',
            'color': '#FF0000',
            'is_default': True
        }
        
        serializer = BookmarkCategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        category = serializer.save(user=self.user)
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.user, self.user)

    def test_collection_serializer(self):
        from .serializers import BookmarkCollectionSerializer
        
        data = {
            'name': 'Test Collection',
            'description': 'Test description',
            'is_public': True
        }
        
        serializer = BookmarkCollectionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        collection = serializer.save(user=self.user)
        self.assertEqual(collection.name, 'Test Collection')
        self.assertEqual(collection.user, self.user)


class BookmarkPermissionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='testpass123'
        )

    def test_unauthorized_access(self):
        url = reverse('bookmark-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_only_access_own_bookmarks(self):
        # Create bookmarks for different users
        bookmark1 = Bookmark.objects.create(
            user=self.user1,
            title='User 1 Bookmark',
            url='https://example1.com'
        )
        bookmark2 = Bookmark.objects.create(
            user=self.user2,
            title='User 2 Bookmark',
            url='https://example2.com'
        )
        
        # Authenticate as user1
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        url = reverse('bookmark-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'User 1 Bookmark')

    def test_user_cannot_access_other_user_bookmark(self):
        bookmark = Bookmark.objects.create(
            user=self.user2,
            title='User 2 Bookmark',
            url='https://example.com'
        )
        
        # Authenticate as user1
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        url = reverse('bookmark-detail', args=[bookmark.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 