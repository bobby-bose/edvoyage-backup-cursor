from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import (
    ChatUser, ChatRoom, ChatRoomParticipant, Message, 
    MessageStatus, Contact, ChatNotification
)

User = get_user_model()


class ChatModelsTestCase(TestCase):
    """Test cases for Chat models"""

    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User1'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User2'
        )
        
        self.chat_user1 = ChatUser.objects.create(
            user=self.user1,
            role='MBBS Student',
            institution='Test University',
            specialization='Cardiology',
            bio='Test bio',
            is_verified=True
        )
        self.chat_user2 = ChatUser.objects.create(
            user=self.user2,
            role='Intern',
            institution='Test Hospital',
            specialization='Surgery',
            bio='Test bio 2',
            is_verified=False
        )

    def test_chat_user_creation(self):
        """Test ChatUser model creation"""
        self.assertEqual(self.chat_user1.user.username, 'testuser1')
        self.assertEqual(self.chat_user1.role, 'MBBS Student')
        self.assertEqual(self.chat_user1.full_name, 'Test User1')
        self.assertTrue(self.chat_user1.is_verified)
        self.assertFalse(self.chat_user2.is_verified)

    def test_chat_room_creation(self):
        """Test ChatRoom model creation"""
        room = ChatRoom.objects.create(
            name='Test Room',
            type='direct',
            created_by=self.chat_user1
        )
        self.assertEqual(room.name, 'Test Room')
        self.assertEqual(room.type, 'direct')
        self.assertEqual(room.created_by, self.chat_user1)

    def test_message_creation(self):
        """Test Message model creation"""
        room = ChatRoom.objects.create(
            name='Test Room',
            type='direct',
            created_by=self.chat_user1
        )
        
        message = Message.objects.create(
            room=room,
            sender=self.chat_user1,
            content='Test message',
            message_type='text'
        )
        
        self.assertEqual(message.content, 'Test message')
        self.assertEqual(message.sender, self.chat_user1)
        self.assertEqual(message.room, room)
        self.assertEqual(message.message_type, 'text')

    def test_contact_creation(self):
        """Test Contact model creation"""
        contact = Contact.objects.create(
            user=self.chat_user1,
            contact=self.chat_user2,
            nickname='John'
        )
        
        self.assertEqual(contact.user, self.chat_user1)
        self.assertEqual(contact.contact, self.chat_user2)
        self.assertEqual(contact.nickname, 'John')
        self.assertFalse(contact.is_favorite)
        self.assertFalse(contact.is_blocked)

    def test_message_status_creation(self):
        """Test MessageStatus model creation"""
        room = ChatRoom.objects.create(
            name='Test Room',
            type='direct',
            created_by=self.chat_user1
        )
        
        message = Message.objects.create(
            room=room,
            sender=self.chat_user1,
            content='Test message',
            message_type='text'
        )
        
        status_obj = MessageStatus.objects.create(
            message=message,
            user=self.chat_user2,
            status='sent'
        )
        
        self.assertEqual(status_obj.message, message)
        self.assertEqual(status_obj.user, self.chat_user2)
        self.assertEqual(status_obj.status, 'sent')


class ChatAPITestCase(APITestCase):
    """Test cases for Chat API endpoints"""

    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User1'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User2'
        )
        
        self.chat_user1 = ChatUser.objects.create(
            user=self.user1,
            role='MBBS Student',
            institution='Test University',
            specialization='Cardiology',
            bio='Test bio',
            is_verified=True
        )
        self.chat_user2 = ChatUser.objects.create(
            user=self.user2,
            role='Intern',
            institution='Test Hospital',
            specialization='Surgery',
            bio='Test bio 2',
            is_verified=False
        )
        
        self.client.force_authenticate(user=self.user1)

    def test_get_chat_users(self):
        """Test getting chat users"""
        response = self.client.get('/api/v1/chat/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_chat_user_detail(self):
        """Test getting specific chat user"""
        response = self.client.get(f'/api/v1/chat/api/users/{self.chat_user1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser1')

    def test_create_chat_room(self):
        """Test creating a chat room"""
        data = {
            'name': 'Test Room',
            'type': 'direct'
        }
        response = self.client.post('/api/v1/chat/api/rooms/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Room')

    def test_create_message(self):
        """Test creating a message"""
        # First create a room
        room = ChatRoom.objects.create(
            name='Test Room',
            type='direct',
            created_by=self.chat_user1
        )
        ChatRoomParticipant.objects.create(
            room=room,
            user=self.chat_user1,
            role='admin'
        )
        
        data = {
            'content': 'Test message',
            'message_type': 'text'
        }
        response = self.client.post(f'/api/v1/chat/api/rooms/{room.id}/messages/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Test message')

    def test_create_contact(self):
        """Test creating a contact"""
        data = {
            'contact': self.chat_user2.id,
            'nickname': 'John'
        }
        response = self.client.post('/api/v1/chat/api/contacts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nickname'], 'John')

    def test_search_users(self):
        """Test searching users"""
        response = self.client.get('/api/v1/chat/api/search/users/?query=test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_user_status_update(self):
        """Test updating user status"""
        data = {
            'is_online': True,
            'last_seen': '2024-01-15T10:30:00Z'
        }
        response = self.client.put(f'/api/v1/chat/api/users/{self.chat_user1.id}/status/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_online'])

    def test_contact_favorite_toggle(self):
        """Test toggling contact favorite status"""
        contact = Contact.objects.create(
            user=self.chat_user1,
            contact=self.chat_user2,
            nickname='John'
        )
        
        response = self.client.post(f'/api/v1/chat/api/contacts/{contact.id}/favorite/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_favorite'])

    def test_contact_block_toggle(self):
        """Test toggling contact block status"""
        contact = Contact.objects.create(
            user=self.chat_user1,
            contact=self.chat_user2,
            nickname='John'
        )
        
        response = self.client.post(f'/api/v1/chat/api/contacts/{contact.id}/block/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_blocked'])

    def test_get_notifications(self):
        """Test getting notifications"""
        # Create a notification
        room = ChatRoom.objects.create(
            name='Test Room',
            type='direct',
            created_by=self.chat_user1
        )
        message = Message.objects.create(
            room=room,
            sender=self.chat_user2,
            content='Test message',
            message_type='text'
        )
        notification = ChatNotification.objects.create(
            user=self.chat_user1,
            message=message,
            type='new_message'
        )
        
        response = self.client.get('/api/v1/chat/api/notifications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_mark_notification_read(self):
        """Test marking notification as read"""
        notification = ChatNotification.objects.create(
            user=self.chat_user1,
            message=None,
            type='contact_request'
        )
        
        response = self.client.put(f'/api/v1/chat/api/notifications/{notification.id}/read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_read'])

    def test_unread_notification_count(self):
        """Test getting unread notification count"""
        # Create unread notifications
        ChatNotification.objects.create(
            user=self.chat_user1,
            message=None,
            type='contact_request',
            is_read=False
        )
        ChatNotification.objects.create(
            user=self.chat_user1,
            message=None,
            type='contact_request',
            is_read=False
        )
        
        response = self.client.get('/api/v1/chat/api/notifications/unread-count/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 2)
