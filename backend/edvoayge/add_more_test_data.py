#!/usr/bin/env python3
"""
Script to add more comprehensive test data for the notes system.
This includes multiple categories, topics, modules, and videos.
"""

import os
import sys
import django
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edvoayge.settings')
django.setup()

from notes.models import NotesCategory, NotesTopic, NotesModule, NotesVideo

def add_comprehensive_test_data():
    """Add comprehensive test data for the notes system."""
    
    print("🔄 Adding comprehensive test data...")
    
    # Create multiple categories
    categories_data = [
        {
            'name': 'video',
            'description': 'Video lectures and tutorials',
            'icon': 'video',
            'color': '#FF6B6B',
            'is_active': True,
            'order': 1
        },
        {
            'name': 'mcq',
            'description': 'Multiple choice questions and practice tests',
            'icon': 'quiz',
            'color': '#4ECDC4',
            'is_active': True,
            'order': 2
        },
        {
            'name': 'clinical_case',
            'description': 'Clinical case studies and scenarios',
            'icon': 'medical',
            'color': '#45B7D1',
            'is_active': True,
            'order': 3
        },
        {
            'name': 'q_bank',
            'description': 'Question bank and practice questions',
            'icon': 'question',
            'color': '#96CEB4',
            'is_active': True,
            'order': 4
        },
        {
            'name': 'flash_card',
            'description': 'Flashcards for quick revision',
            'icon': 'card',
            'color': '#FFEAA7',
            'is_active': True,
            'order': 5
        }
    ]
    
    # Create categories
    categories = {}
    for cat_data in categories_data:
        category, created = NotesCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        categories[cat_data['name']] = category
        print(f"{'✅ Created' if created else '🔄 Updated'} category: {category.name}")
    
    # Create topics for video category
    video_topics_data = [
        {
            'title': 'Human Anatomy',
            'description': 'Comprehensive anatomy content for medical students',
            'is_featured': True,
            'order': 1
        },
        {
            'title': 'Physiology',
            'description': 'Physiology fundamentals and concepts',
            'is_featured': False,
            'order': 2
        },
        {
            'title': 'Biochemistry',
            'description': 'Biochemistry principles and applications',
            'is_featured': False,
            'order': 3
        },
        {
            'title': 'Pharmacology',
            'description': 'Drug mechanisms and therapeutic applications',
            'is_featured': False,
            'order': 4
        },
        {
            'title': 'Pathology',
            'description': 'Disease mechanisms and diagnostic approaches',
            'is_featured': False,
            'order': 5
        },
        {
            'title': 'Psychology Fundamentals',
            'description': 'Basic psychology concepts and theories',
            'is_featured': False,
            'order': 6
        }
    ]
    
    # Create topics for video category
    video_category = categories['video']
    topics = []
    for topic_data in video_topics_data:
        topic, created = NotesTopic.objects.get_or_create(
            title=topic_data['title'],
            category=video_category,
            defaults=topic_data
        )
        topics.append(topic)
        print(f"{'✅ Created' if created else '🔄 Updated'} topic: {topic.title}")
    
    # Create modules and videos for each topic
    for topic in topics:
        # Create 3-5 modules per topic
        for i in range(1, 4):
            module_data = {
                'title': f'{topic.title} - Module {i}',
                'description': f'Module {i} of {topic.title}',
                'module_type': 'video',
                'duration_minutes': 30 + (i * 5),
                'instructor': f'Dr. {topic.title} Instructor',
                'access_type': 'free' if i == 1 else 'premium',
                'is_active': True,
                'order': i
            }
            
            module, created = NotesModule.objects.get_or_create(
                title=module_data['title'],
                topic=topic,
                defaults=module_data
            )
            
            # Create video for this module
            video_data = {
                'title': f'{module.title} - Video',
                'description': f'Video for {module.title}',
                'video_url': f'https://www.youtube.com/watch?v=video_{topic.id}_{i}',
                'thumbnail_url': 'https://www.topuniversities.com/sites/default/files/harvard_1.jpg',
                'duration_seconds': module.duration_minutes * 60,
                'is_active': True
            }
            
            video, created = NotesVideo.objects.get_or_create(
                title=video_data['title'],
                module=module,
                defaults=video_data
            )
            
            print(f"{'✅ Created' if created else '🔄 Updated'} module: {module.title} with video")
    
    # Update category statistics
    for category in categories.values():
        topics_count = NotesTopic.objects.filter(category=category, is_active=True).count()
        videos_count = NotesModule.objects.filter(
            topic__category=category,
            module_type='video',
            is_active=True
        ).count()
        
        category.topics_count = topics_count
        category.videos_count = videos_count
        category.save()
        
        print(f"📊 Category '{category.name}': {topics_count} topics, {videos_count} videos")
    
    print("\n🎉 Comprehensive test data added successfully!")
    print("\n📋 Summary:")
    print(f"   • Categories: {len(categories)}")
    print(f"   • Topics: {len(topics)}")
    print(f"   • Modules: {NotesModule.objects.count()}")
    print(f"   • Videos: {NotesVideo.objects.count()}")

if __name__ == '__main__':
    try:
        add_comprehensive_test_data()
    except Exception as e:
        print(f"❌ Error adding test data: {e}")
        sys.exit(1)
