#!/usr/bin/env python
"""
Script to add Previous Year Papers dummy data to the database.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edvoayge.settings')
django.setup()

from notes.models import NotesCategory, NotesTopic, NotesModule, NotesPreviousPapers
from django.db import transaction

def create_previous_papers_dummy_data():
    """Create dummy Previous Year Papers data."""
    
    print("Creating Previous Year Papers dummy data...")
    
    try:
        with transaction.atomic():
            # Get or create Previous Year Papers category
            previous_papers_category, created = NotesCategory.objects.get_or_create(
                name='previous_papers',
                defaults={
                    'display_name': 'Previous Year Papers',
                    'description': 'Previous year examination papers for medical students',
                    'topics_count': 8,
                    'modules_count': 200,
                    'videos_count': 0,
                    'is_active': True,
                    'is_featured': True,
                }
            )
            
            if created:
                print(f"Created Previous Year Papers category: {previous_papers_category}")
            else:
                print(f"Previous Year Papers category already exists: {previous_papers_category}")
            
            # Previous Year Papers topics data
            papers_topics_data = [
                {
                    'title': 'USMLE Step 1 Papers',
                    'description': 'Previous year USMLE Step 1 examination papers',
                    'modules_count': 25,
                    'is_featured': True,
                    'order': 1
                },
                {
                    'title': 'USMLE Step 2 CK Papers',
                    'description': 'Previous year USMLE Step 2 CK examination papers',
                    'modules_count': 20,
                    'is_featured': False,
                    'order': 2
                },
                {
                    'title': 'PLAB 1 Papers',
                    'description': 'Previous year PLAB 1 examination papers',
                    'modules_count': 18,
                    'is_featured': False,
                    'order': 3
                },
                {
                    'title': 'PLAB 2 Papers',
                    'description': 'Previous year PLAB 2 examination papers',
                    'modules_count': 15,
                    'is_featured': False,
                    'order': 4
                },
                {
                    'title': 'AMC Papers',
                    'description': 'Previous year Australian Medical Council papers',
                    'modules_count': 22,
                    'is_featured': False,
                    'order': 5
                },
                {
                    'title': 'MCCQE Papers',
                    'description': 'Previous year Medical Council of Canada papers',
                    'modules_count': 16,
                    'is_featured': False,
                    'order': 6
                },
                {
                    'title': 'FMGE Papers',
                    'description': 'Previous year Foreign Medical Graduate Examination papers',
                    'modules_count': 30,
                    'is_featured': False,
                    'order': 7
                },
                {
                    'title': 'NEET PG Papers',
                    'description': 'Previous year NEET PG examination papers',
                    'modules_count': 28,
                    'is_featured': False,
                    'order': 8
                },
            ]
            
            # Create Previous Year Papers topics
            created_topics = []
            for topic_data in papers_topics_data:
                topic, created = NotesTopic.objects.get_or_create(
                    category=previous_papers_category,
                    title=topic_data['title'],
                    defaults={
                        'description': topic_data['description'],
                        'modules_count': topic_data['modules_count'],
                        'is_featured': topic_data['is_featured'],
                        'order': topic_data['order'],
                        'is_active': True,
                    }
                )
                
                if created:
                    print(f"Created Previous Year Papers topic: {topic.title}")
                    created_topics.append(topic)
                else:
                    print(f"Previous Year Papers topic already exists: {topic.title}")
                    created_topics.append(topic)
            
            # Create some sample Previous Year Papers modules for the first topic
            if created_topics:
                first_topic = created_topics[0]  # USMLE Step 1 Papers
                
                # Sample Previous Year Papers for USMLE Step 1
                usmle_papers = [
                    {
                        'title': 'USMLE Step 1 Paper 2023',
                        'paper_title': 'USMLE Step 1 Examination 2023',
                        'year': 2023,
                        'exam_type': 'USMLE Step 1',
                        'total_questions': 280,
                        'duration_minutes': 480,
                        'difficulty_level': 'medium',
                    },
                    {
                        'title': 'USMLE Step 1 Paper 2022',
                        'paper_title': 'USMLE Step 1 Examination 2022',
                        'year': 2022,
                        'exam_type': 'USMLE Step 1',
                        'total_questions': 280,
                        'duration_minutes': 480,
                        'difficulty_level': 'medium',
                    },
                    {
                        'title': 'USMLE Step 1 Paper 2021',
                        'paper_title': 'USMLE Step 1 Examination 2021',
                        'year': 2021,
                        'exam_type': 'USMLE Step 1',
                        'total_questions': 280,
                        'duration_minutes': 480,
                        'difficulty_level': 'hard',
                    },
                ]
                
                for i, paper_data in enumerate(usmle_papers):
                    # Create module
                    module, created = NotesModule.objects.get_or_create(
                        topic=first_topic,
                        title=paper_data['title'],
                        defaults={
                            'module_type': 'previous_papers',
                            'description': f'USMLE Step 1 paper from {paper_data["year"]}',
                            'duration_minutes': paper_data['duration_minutes'],
                            'views_count': 0,
                            'likes_count': 0,
                            'is_active': True,
                            'is_premium': False,
                            'order': i + 1,
                        }
                    )
                    
                    if created:
                        print(f"Created Previous Year Papers module: {module.title}")
                        
                        # Create Previous Year Papers content
                        paper, created = NotesPreviousPapers.objects.get_or_create(
                            module=module,
                            defaults={
                                'paper_title': paper_data['paper_title'],
                                'year': paper_data['year'],
                                'exam_type': paper_data['exam_type'],
                                'paper_url': f'https://example.com/papers/usmle-step1-{paper_data["year"]}.pdf',
                                'solution_url': f'https://example.com/solutions/usmle-step1-{paper_data["year"]}.pdf',
                                'total_questions': paper_data['total_questions'],
                                'duration_minutes': paper_data['duration_minutes'],
                                'difficulty_level': paper_data['difficulty_level'],
                                'views_count': 0,
                                'downloads_count': 0,
                            }
                        )
                        
                        if created:
                            print(f"Created Previous Year Papers content for: {module.title}")
            
            print("\nPrevious Year Papers dummy data created successfully!")
            print(f"Created {len(created_topics)} Previous Year Papers topics")
            
    except Exception as e:
        print(f"Error creating Previous Year Papers dummy data: {e}")
        raise

if __name__ == '__main__':
    create_previous_papers_dummy_data() 