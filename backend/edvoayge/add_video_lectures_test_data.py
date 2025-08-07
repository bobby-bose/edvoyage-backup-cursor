#!/usr/bin/env python
"""
Script to add test video lectures data to the database.
Run this script to populate the database with sample video lectures.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edvoayge.settings')
django.setup()

from notes.models import NotesCategory, NotesTopic, NotesModule, NotesVideo
from django.contrib.auth.models import User

def create_test_data():
    """Create test video lectures data."""
    print("🔍 Creating test video lectures data...")
    
    # Create or get a test user
    user, created = User.objects.get_or_create(
        username='test_user',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    # Create or get video category
    video_category, created = NotesCategory.objects.get_or_create(
        name='video',
        defaults={
            'display_name': 'Video Lectures',
            'description': 'Comprehensive video lectures for medical students',
            'is_active': True,
            'is_featured': True
        }
    )
    
    # Create test topics
    topics_data = [
        {
            'title': 'Anatomy Basics',
            'description': 'Fundamental anatomy concepts for medical students',
            'order': 1,
            'is_featured': True
        },
        {
            'title': 'Physiology Fundamentals',
            'description': 'Core physiology principles and mechanisms',
            'order': 2,
            'is_featured': False
        },
        {
            'title': 'Clinical Skills',
            'description': 'Essential clinical examination techniques',
            'order': 3,
            'is_featured': True
        }
    ]
    
    topics = []
    for topic_data in topics_data:
        topic, created = NotesTopic.objects.get_or_create(
            category=video_category,
            title=topic_data['title'],
            defaults={
                'description': topic_data['description'],
                'order': topic_data['order'],
                'is_featured': topic_data['is_featured'],
                'is_active': True
            }
        )
        topics.append(topic)
        print(f"✅ Created topic: {topic.title}")
    
    # Create test video modules
    video_modules_data = [
        {
            'title': 'Gametogenesis',
            'description': 'Comprehensive lecture on gametogenesis process',
            'instructor': 'Dr. Sarah Johnson, MD',
            'duration_minutes': 30,
            'access_type': 'free',
            'order': 1,
            'topic': topics[0]
        },
        {
            'title': 'Human Anatomy Overview',
            'description': 'Complete overview of human anatomy systems',
            'instructor': 'Dr. Michael Chen, PhD',
            'duration_minutes': 45,
            'access_type': 'premium',
            'order': 2,
            'topic': topics[0]
        },
        {
            'title': 'Cardiovascular System',
            'description': 'Detailed study of heart and blood vessels',
            'instructor': 'Dr. Emily Rodriguez, MD',
            'duration_minutes': 35,
            'access_type': 'free',
            'order': 3,
            'topic': topics[0]
        },
        {
            'title': 'Nervous System Anatomy',
            'description': 'Comprehensive nervous system structure and function',
            'instructor': 'Dr. David Kim, PhD',
            'duration_minutes': 40,
            'access_type': 'premium',
            'order': 4,
            'topic': topics[0]
        },
        {
            'title': 'Respiratory System',
            'description': 'Lung structure and breathing mechanisms',
            'instructor': 'Dr. Lisa Thompson, MD',
            'duration_minutes': 25,
            'access_type': 'free',
            'order': 5,
            'topic': topics[0]
        },
        {
            'title': 'Cell Physiology',
            'description': 'Basic cell structure and function',
            'instructor': 'Dr. Robert Wilson, PhD',
            'duration_minutes': 50,
            'access_type': 'free',
            'order': 1,
            'topic': topics[1]
        },
        {
            'title': 'Clinical Examination',
            'description': 'Basic clinical examination techniques',
            'instructor': 'Dr. Maria Garcia, MD',
            'duration_minutes': 60,
            'access_type': 'premium',
            'order': 1,
            'topic': topics[2]
        }
    ]
    
    for module_data in video_modules_data:
        module, created = NotesModule.objects.get_or_create(
            topic=module_data['topic'],
            title=module_data['title'],
            defaults={
                'module_type': 'video',
                'description': module_data['description'],
                'instructor': module_data['instructor'],
                'duration_minutes': module_data['duration_minutes'],
                'access_type': module_data['access_type'],
                'order': module_data['order'],
                'is_active': True,
                'is_premium': module_data['access_type'] == 'premium'
            }
        )
        
        # Create video details
        video, created = NotesVideo.objects.get_or_create(
            module=module,
            defaults={
                'video_url': f'https://example.com/videos/{module.id}.mp4',
                'thumbnail_url': 'https://www.topuniversities.com/sites/default/files/harvard_1.jpg',
                'duration_seconds': module_data['duration_minutes'] * 60,
                'quality': '720p'
            }
        )
        
        print(f"✅ Created video module: {module.title} by {module.instructor}")
    
    # Update category statistics
    video_category.topics_count = len(topics)
    video_category.videos_count = NotesModule.objects.filter(
        topic__category=video_category,
        module_type='video',
        is_active=True
    ).count()
    video_category.save()
    
    print(f"\n🎉 Successfully created test data!")
    print(f"📊 Category: {video_category.display_name}")
    print(f"📚 Topics: {video_category.topics_count}")
    print(f"🎥 Videos: {video_category.videos_count}")
    print(f"\n🔗 API Endpoint: http://localhost:8000/api/v1/notes/categories/{video_category.id}/video-lectures/")

if __name__ == '__main__':
    create_test_data()
