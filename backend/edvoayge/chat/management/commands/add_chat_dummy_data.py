from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from chat.models import ChatUser, ChatRoom, ChatRoomParticipant, Message, MessageStatus, Contact, ChatNotification
from datetime import datetime, timedelta
import uuid


class Command(BaseCommand):
    help = 'Add dummy data for Chat app'

    def handle(self, *args, **options):
        self.stdout.write('Creating dummy data for Chat app...')

        # Create chat users
        users_data = [
            {
                'username': 'dr_aisha',
                'email': 'aisha@example.com',
                'first_name': 'Aisha',
                'last_name': 'Rehman',
                'role': 'MBBS Student',
                'institution': 'Amrita Institute of Medical Sciences',
                'specialization': 'Cardiology',
                'bio': 'Medical student passionate about cardiology',
                'is_verified': True,
            },
            {
                'username': 'med_student_john',
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'role': 'MBBS Student',
                'institution': 'AIIMS Delhi',
                'specialization': 'Anatomy',
                'bio': 'Learning anatomy and physiology',
                'is_verified': False,
            },
            {
                'username': 'orthopedic_intern',
                'email': 'rohit@example.com',
                'first_name': 'Rohit',
                'last_name': 'Sharma',
                'role': 'Orthopedic Intern',
                'institution': 'AIIMS Delhi',
                'specialization': 'Orthopedics',
                'bio': 'Currently doing internship in surgery',
                'is_verified': True,
            },
            {
                'username': 'gp_doctor',
                'email': 'sneha@example.com',
                'first_name': 'Sneha',
                'last_name': 'Rao',
                'role': 'General Practitioner',
                'institution': 'Kasturba Medical College',
                'specialization': 'General Medicine',
                'bio': 'Experienced GP with focus on preventive care',
                'is_verified': True,
            },
            {
                'username': 'pediatric_resident',
                'email': 'fatima@example.com',
                'first_name': 'Fatima',
                'last_name': 'Noor',
                'role': 'Pediatric Resident',
                'institution': 'JIPMER',
                'specialization': 'Pediatrics',
                'bio': 'Resident in pediatrics department',
                'is_verified': True,
            },
        ]

        chat_users = []
        for user_data in users_data:
            # Create or get the base user
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'password': make_password('password123'),
                }
            )
            
            # Create chat user profile
            chat_user, created = ChatUser.objects.get_or_create(
                user=user,
                defaults={
                    'role': user_data['role'],
                    'institution': user_data['institution'],
                    'specialization': user_data['specialization'],
                    'bio': user_data['bio'],
                    'is_verified': user_data['is_verified'],
                    'is_online': True,
                }
            )
            chat_users.append(chat_user)
            if created:
                self.stdout.write(f'Created chat user: {chat_user.user.username}')

        # Create chat rooms (direct chats)
        rooms = []
        for i in range(len(chat_users) - 1):
            room = ChatRoom.objects.create(
                name=f"Direct Chat {i+1}",
                type='direct',
                created_by=chat_users[i]
            )
            rooms.append(room)
            
            # Add participants
            ChatRoomParticipant.objects.create(
                room=room,
                user=chat_users[i],
                role='admin'
            )
            ChatRoomParticipant.objects.create(
                room=room,
                user=chat_users[i+1],
                role='member'
            )
            self.stdout.write(f'Created room: {room.name}')

        # Create a group chat
        group_room = ChatRoom.objects.create(
            name="Medical Students Group",
            type='group',
            created_by=chat_users[0]
        )
        rooms.append(group_room)
        
        # Add all users to group chat
        for chat_user in chat_users:
            ChatRoomParticipant.objects.create(
                room=group_room,
                user=chat_user,
                role='member'
            )
        self.stdout.write(f'Created group room: {group_room.name}')

        # Create messages
        messages_data = [
            {
                'room': rooms[0],
                'sender': chat_users[0],
                'content': 'Hello! How are you doing with your studies?',
                'message_type': 'text',
            },
            {
                'room': rooms[0],
                'sender': chat_users[1],
                'content': 'Going well! Just finished anatomy lab. The brachial plexus was challenging.',
                'message_type': 'text',
            },
            {
                'room': rooms[0],
                'sender': chat_users[0],
                'content': 'That\'s great! Anatomy is indeed challenging. Any tips for memorizing nerve pathways?',
                'message_type': 'text',
            },
            {
                'room': rooms[1],
                'sender': chat_users[1],
                'content': 'Hi! I heard you\'re doing your internship. How is it going?',
                'message_type': 'text',
            },
            {
                'room': rooms[1],
                'sender': chat_users[2],
                'content': 'Yes, it\'s been amazing! Assisted in an appendectomy today. Surgery is incredible.',
                'message_type': 'text',
            },
            {
                'room': group_room,
                'sender': chat_users[0],
                'content': 'Hello everyone! How are your studies going?',
                'message_type': 'text',
            },
            {
                'room': group_room,
                'sender': chat_users[1],
                'content': 'Great! Just finished my cardiology rotation.',
                'message_type': 'text',
            },
            {
                'room': group_room,
                'sender': chat_users[3],
                'content': 'That sounds interesting! Cardiology is fascinating.',
                'message_type': 'text',
            },
        ]

        messages = []
        for i, msg_data in enumerate(messages_data):
            # Create messages with different timestamps
            created_at = datetime.now() - timedelta(hours=i*2)
            message = Message.objects.create(
                room=msg_data['room'],
                sender=msg_data['sender'],
                content=msg_data['content'],
                message_type=msg_data['message_type'],
                created_at=created_at,
            )
            messages.append(message)
            self.stdout.write(f'Created message: {message.content[:50]}...')

        # Create message statuses
        for message in messages:
            participants = message.room.participants.filter(is_active=True)
            for participant in participants:
                # Skip sender's status
                if participant.user != message.sender:
                    MessageStatus.objects.create(
                        message=message,
                        user=participant.user,
                        status='sent'
                    )

        # Create contacts
        contacts_data = [
            (chat_users[0], chat_users[1], 'John'),
            (chat_users[0], chat_users[2], 'Rohit'),
            (chat_users[1], chat_users[0], 'Aisha'),
            (chat_users[1], chat_users[3], 'Sneha'),
            (chat_users[2], chat_users[0], 'Aisha'),
            (chat_users[3], chat_users[1], 'John'),
        ]

        for user, contact, nickname in contacts_data:
            contact_obj, created = Contact.objects.get_or_create(
                user=user,
                contact=contact,
                defaults={'nickname': nickname}
            )
            if created:
                self.stdout.write(f'{user.user.username} added {contact.user.username} as contact')

        # Create some notifications
        notifications_data = [
            (chat_users[1], messages[0], 'new_message'),
            (chat_users[2], messages[3], 'new_message'),
            (chat_users[0], messages[1], 'message_reply'),
            (chat_users[1], messages[2], 'message_reply'),
        ]

        for user, message, notification_type in notifications_data:
            ChatNotification.objects.create(
                user=user,
                message=message,
                type=notification_type
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully created dummy data for Chat app!')
        )
        self.stdout.write(f'Created {len(chat_users)} chat users')
        self.stdout.write(f'Created {len(rooms)} chat rooms')
        self.stdout.write(f'Created {len(messages)} messages')
        self.stdout.write(f'Created {len(contacts_data)} contacts')
        self.stdout.write(f'Created {len(notifications_data)} notifications') 