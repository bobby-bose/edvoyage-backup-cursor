#!/usr/bin/env python
"""
Script to add Q-Bank dummy data to the database.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edvoayge.settings')
django.setup()

from notes.models import NotesCategory, NotesTopic, NotesModule, NotesQBank, NotesQBankOption
from django.db import transaction

def create_qbank_dummy_data():
    """Create dummy Q-Bank data."""
    
    print("Creating Q-Bank dummy data...")
    
    try:
        with transaction.atomic():
            # Get or create Q-Bank category
            q_bank_category, created = NotesCategory.objects.get_or_create(
                name='q_bank',
                defaults={
                    'display_name': 'Q-Bank',
                    'description': 'Comprehensive question bank for medical students',
                    'topics_count': 8,
                    'modules_count': 150,
                    'videos_count': 0,
                    'is_active': True,
                    'is_featured': True,
                }
            )
            
            if created:
                print(f"Created Q-Bank category: {q_bank_category}")
            else:
                print(f"Q-Bank category already exists: {q_bank_category}")
            
            # Q-Bank topics data
            q_bank_topics_data = [
                {
                    'title': 'Anatomy Q-Bank',
                    'description': 'Comprehensive anatomy question bank for medical students',
                    'modules_count': 18,
                    'is_featured': True,
                    'order': 1
                },
                {
                    'title': 'Physiology Q-Bank',
                    'description': 'Physiology question bank and practice questions',
                    'modules_count': 15,
                    'is_featured': False,
                    'order': 2
                },
                {
                    'title': 'Biochemistry Q-Bank',
                    'description': 'Biochemistry question bank and molecular concepts',
                    'modules_count': 20,
                    'is_featured': False,
                    'order': 3
                },
                {
                    'title': 'Pharmacology Q-Bank',
                    'description': 'Drug mechanisms and therapeutic question bank',
                    'modules_count': 22,
                    'is_featured': False,
                    'order': 4
                },
                {
                    'title': 'Pathology Q-Bank',
                    'description': 'Disease mechanisms and diagnostic question bank',
                    'modules_count': 16,
                    'is_featured': False,
                    'order': 5
                },
                {
                    'title': 'Microbiology Q-Bank',
                    'description': 'Microbial organisms and infectious disease question bank',
                    'modules_count': 19,
                    'is_featured': False,
                    'order': 6
                },
                {
                    'title': 'Forensic Medicine Q-Bank',
                    'description': 'Forensic science and toxicological question bank',
                    'modules_count': 12,
                    'is_featured': False,
                    'order': 7
                },
                {
                    'title': 'Community Medicine Q-Bank',
                    'description': 'Public health and community healthcare question bank',
                    'modules_count': 14,
                    'is_featured': False,
                    'order': 8
                },
            ]
            
            # Create Q-Bank topics
            created_topics = []
            for topic_data in q_bank_topics_data:
                topic, created = NotesTopic.objects.get_or_create(
                    category=q_bank_category,
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
                    print(f"Created Q-Bank topic: {topic.title}")
                    created_topics.append(topic)
                else:
                    print(f"Q-Bank topic already exists: {topic.title}")
                    created_topics.append(topic)
            
            # Create some sample Q-Bank modules for the first topic
            if created_topics:
                first_topic = created_topics[0]  # Anatomy Q-Bank
                
                # Sample Q-Bank questions for Anatomy
                anatomy_questions = [
                    {
                        'title': 'Anatomy Q-Bank Module 1',
                        'question_text': 'Which of the following is NOT a function of the skeletal system?',
                        'explanation': 'The skeletal system provides support, protection, and movement, but does not directly produce hormones.',
                        'difficulty_level': 'medium',
                        'options': [
                            'Support and protection',
                            'Blood cell production',
                            'Hormone production',
                            'Mineral storage',
                        ],
                        'correct_option': 2,  # 0-indexed
                    },
                    {
                        'title': 'Anatomy Q-Bank Module 2',
                        'question_text': 'The largest bone in the human body is:',
                        'explanation': 'The femur (thigh bone) is the longest and strongest bone in the human body.',
                        'difficulty_level': 'easy',
                        'options': [
                            'Humerus',
                            'Femur',
                            'Tibia',
                            'Radius',
                        ],
                        'correct_option': 1,  # 0-indexed
                    },
                    {
                        'title': 'Anatomy Q-Bank Module 3',
                        'question_text': 'Which muscle is responsible for flexing the elbow?',
                        'explanation': 'The biceps brachii is the primary muscle responsible for flexing the elbow joint.',
                        'difficulty_level': 'medium',
                        'options': [
                            'Triceps brachii',
                            'Biceps brachii',
                            'Deltoid',
                            'Pectoralis major',
                        ],
                        'correct_option': 1,  # 0-indexed
                    },
                ]
                
                for i, q_data in enumerate(anatomy_questions):
                    # Create module
                    module, created = NotesModule.objects.get_or_create(
                        topic=first_topic,
                        title=q_data['title'],
                        defaults={
                            'module_type': 'q_bank',
                            'description': f'Anatomy Q-Bank question {i+1}',
                            'duration_minutes': 5,
                            'views_count': 0,
                            'likes_count': 0,
                            'is_active': True,
                            'is_premium': False,
                            'order': i + 1,
                        }
                    )
                    
                    if created:
                        print(f"Created Q-Bank module: {module.title}")
                        
                        # Create Q-Bank content
                        q_bank, created = NotesQBank.objects.get_or_create(
                            module=module,
                            defaults={
                                'question_text': q_data['question_text'],
                                'explanation': q_data['explanation'],
                                'difficulty_level': q_data['difficulty_level'],
                                'attempts_count': 0,
                                'correct_answers_count': 0,
                            }
                        )
                        
                        if created:
                            print(f"Created Q-Bank content for: {module.title}")
                            
                            # Create options
                            for j, option_text in enumerate(q_data['options']):
                                is_correct = (j == q_data['correct_option'])
                                option, created = NotesQBankOption.objects.get_or_create(
                                    q_bank=q_bank,
                                    option_text=option_text,
                                    defaults={
                                        'is_correct': is_correct,
                                        'order': j + 1,
                                    }
                                )
                                
                                if created:
                                    print(f"Created option {j+1}: {option_text} (Correct: {is_correct})")
            
            print("\nQ-Bank dummy data created successfully!")
            print(f"Created {len(created_topics)} Q-Bank topics")
            
    except Exception as e:
        print(f"Error creating Q-Bank dummy data: {e}")
        raise

if __name__ == '__main__':
    create_qbank_dummy_data() 