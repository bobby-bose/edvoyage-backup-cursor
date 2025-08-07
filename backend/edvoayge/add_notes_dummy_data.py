import os
import django
import random
from django.utils import timezone
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edvoayge.settings')
django.setup()

from notes.models import (
    NotesCategory, NotesTopic, NotesModule, NotesVideo, 
    NotesMCQ, NotesMCQOption, NotesClinicalCase, 
    NotesQBank, NotesFlashCard, NotesStatistics
)

# Categories data
CATEGORIES_DATA = [
    {
        'name': 'video',
        'display_name': 'Video',
        'description': 'Educational videos covering various medical topics',
        'topics_count': 23,
        'modules_count': 0,
        'videos_count': 200,
    },
    {
        'name': 'mcq',
        'display_name': 'MCQ',
        'description': 'Multiple choice questions for exam preparation',
        'topics_count': 23,
        'modules_count': 230,
        'videos_count': 0,
    },
    {
        'name': 'clinical_case',
        'display_name': 'Clinical Case',
        'description': 'Real clinical cases for practical learning',
        'topics_count': 23,
        'modules_count': 230,
        'videos_count': 0,
    },
    {
        'name': 'q_bank',
        'display_name': 'Q-Bank',
        'description': 'Question bank for comprehensive practice',
        'topics_count': 23,
        'modules_count': 230,
        'videos_count': 0,
    },
    {
        'name': 'flash_card',
        'display_name': 'Flash Card',
        'description': 'Flash cards for quick revision',
        'topics_count': 23,
        'modules_count': 230,
        'videos_count': 0,
    },
]

# Topics data for each category
TOPICS_DATA = {
    'video': [
        'Anatomy Basics', 'Physiology Fundamentals', 'Pathology Overview', 
        'Pharmacology Essentials', 'Clinical Skills', 'Medical Procedures',
        'Emergency Medicine', 'Cardiology', 'Neurology', 'Pediatrics',
        'Obstetrics & Gynecology', 'Psychiatry', 'Surgery Basics',
        'Radiology', 'Laboratory Medicine', 'Preventive Medicine',
        'Medical Ethics', 'Research Methods', 'Evidence-Based Medicine',
        'Medical Technology', 'Healthcare Systems', 'Global Health',
        'Medical History'
    ],
    'mcq': [
        'Anatomy MCQs', 'Physiology MCQs', 'Pathology MCQs',
        'Pharmacology MCQs', 'Clinical Skills MCQs', 'Medical Procedures MCQs',
        'Emergency Medicine MCQs', 'Cardiology MCQs', 'Neurology MCQs',
        'Pediatrics MCQs', 'Obstetrics & Gynecology MCQs', 'Psychiatry MCQs',
        'Surgery MCQs', 'Radiology MCQs', 'Laboratory Medicine MCQs',
        'Preventive Medicine MCQs', 'Medical Ethics MCQs', 'Research MCQs',
        'Evidence-Based Medicine MCQs', 'Medical Technology MCQs',
        'Healthcare Systems MCQs', 'Global Health MCQs', 'Medical History MCQs'
    ],
    'clinical_case': [
        'Cardiovascular Cases', 'Respiratory Cases', 'Gastrointestinal Cases',
        'Neurological Cases', 'Endocrine Cases', 'Renal Cases',
        'Hematological Cases', 'Infectious Disease Cases', 'Oncological Cases',
        'Pediatric Cases', 'Obstetric Cases', 'Psychiatric Cases',
        'Surgical Cases', 'Emergency Cases', 'Trauma Cases',
        'Critical Care Cases', 'Geriatric Cases', 'Rheumatological Cases',
        'Dermatological Cases', 'Ophthalmological Cases', 'ENT Cases',
        'Orthopedic Cases', 'Urological Cases'
    ],
    'q_bank': [
        'USMLE Step 1 Q-Bank', 'USMLE Step 2 Q-Bank', 'USMLE Step 3 Q-Bank',
        'PLAB Q-Bank', 'FMGE Q-Bank', 'NEET PG Q-Bank',
        'AIIMS Q-Bank', 'JIPMER Q-Bank', 'State PG Q-Bank',
        'International Q-Bank', 'Specialty Q-Bank', 'Subspecialty Q-Bank',
        'Clinical Q-Bank', 'Basic Science Q-Bank', 'Clinical Skills Q-Bank',
        'Communication Skills Q-Bank', 'Professionalism Q-Bank',
        'Medical Knowledge Q-Bank', 'Patient Care Q-Bank',
        'Practice-Based Learning Q-Bank', 'Systems-Based Practice Q-Bank',
        'Interpersonal Skills Q-Bank', 'Medical Ethics Q-Bank'
    ],
    'flash_card': [
        'Anatomy Flash Cards', 'Physiology Flash Cards', 'Pathology Flash Cards',
        'Pharmacology Flash Cards', 'Clinical Skills Flash Cards',
        'Medical Procedures Flash Cards', 'Emergency Medicine Flash Cards',
        'Cardiology Flash Cards', 'Neurology Flash Cards', 'Pediatrics Flash Cards',
        'Obstetrics & Gynecology Flash Cards', 'Psychiatry Flash Cards',
        'Surgery Flash Cards', 'Radiology Flash Cards', 'Laboratory Medicine Flash Cards',
        'Preventive Medicine Flash Cards', 'Medical Ethics Flash Cards',
        'Research Flash Cards', 'Evidence-Based Medicine Flash Cards',
        'Medical Technology Flash Cards', 'Healthcare Systems Flash Cards',
        'Global Health Flash Cards', 'Medical History Flash Cards'
    ],
}

# Sample MCQ questions
MCQ_QUESTIONS = [
    {
        'question': 'Which of the following is the primary function of the heart?',
        'options': [
            'Pump blood throughout the body',
            'Filter blood',
            'Produce hormones',
            'Store blood'
        ],
        'correct': 0,
        'explanation': 'The heart\'s primary function is to pump blood throughout the body, delivering oxygen and nutrients to tissues.'
    },
    {
        'question': 'What is the normal range for blood pressure in adults?',
        'options': [
            '90/60 mmHg',
            '120/80 mmHg',
            '140/90 mmHg',
            '160/100 mmHg'
        ],
        'correct': 1,
        'explanation': 'Normal blood pressure is typically around 120/80 mmHg, though it can vary slightly.'
    },
    {
        'question': 'Which organ is responsible for filtering blood and removing waste?',
        'options': [
            'Heart',
            'Liver',
            'Kidneys',
            'Lungs'
        ],
        'correct': 2,
        'explanation': 'The kidneys are responsible for filtering blood and removing waste products from the body.'
    },
]

# Sample clinical cases
CLINICAL_CASES = [
    {
        'title': 'Chest Pain Case',
        'patient_history': '45-year-old male presents with chest pain for 2 hours. Pain is crushing, radiates to left arm.',
        'clinical_findings': 'BP: 160/95, HR: 110, RR: 20, Temp: 37.2°C. ECG shows ST elevation in leads II, III, aVF.',
        'diagnosis': 'Acute Inferior Myocardial Infarction',
        'treatment': 'Immediate aspirin, nitroglycerin, and transfer to cardiac catheterization lab.'
    },
    {
        'title': 'Shortness of Breath Case',
        'patient_history': '65-year-old female with history of COPD presents with worsening shortness of breath for 3 days.',
        'clinical_findings': 'BP: 140/85, HR: 95, RR: 25, Temp: 37.8°C. Decreased breath sounds bilaterally.',
        'diagnosis': 'COPD Exacerbation',
        'treatment': 'Bronchodilators, corticosteroids, and oxygen therapy.'
    },
]

# Sample flash cards
FLASH_CARDS = [
    {
        'front': 'What is the largest organ in the human body?',
        'back': 'The skin is the largest organ in the human body.',
        'category': 'Anatomy'
    },
    {
        'front': 'What is the normal heart rate for adults?',
        'back': '60-100 beats per minute at rest.',
        'category': 'Physiology'
    },
    {
        'front': 'What is the primary function of red blood cells?',
        'back': 'To transport oxygen from the lungs to tissues throughout the body.',
        'category': 'Physiology'
    },
]

def create_categories():
    """Create notes categories."""
    print("Creating notes categories...")
    
    for category_data in CATEGORIES_DATA:
        category, created = NotesCategory.objects.get_or_create(
            name=category_data['name'],
            defaults={
                'display_name': category_data['display_name'],
                'description': category_data['description'],
                'topics_count': category_data['topics_count'],
                'modules_count': category_data['modules_count'],
                'videos_count': category_data['videos_count'],
                'is_active': True,
                'is_featured': True,
            }
        )
        
        if created:
            print(f"Created category: {category.display_name}")
        else:
            print(f"Category already exists: {category.display_name}")
        
        # Create topics for this category
        create_topics_for_category(category)

def create_topics_for_category(category):
    """Create topics for a specific category."""
    topics_list = TOPICS_DATA.get(category.name, [])
    
    for i, topic_title in enumerate(topics_list):
        topic, created = NotesTopic.objects.get_or_create(
            category=category,
            title=topic_title,
            defaults={
                'description': f'Comprehensive {topic_title.lower()} content for medical students.',
                'modules_count': random.randint(5, 15),
                'videos_count': random.randint(3, 10) if category.name == 'video' else 0,
                'is_active': True,
                'is_featured': random.choice([True, False]),
                'order': i + 1,
            }
        )
        
        if created:
            print(f"  Created topic: {topic.title}")
            # Create some modules for this topic
            create_modules_for_topic(topic)
        else:
            print(f"  Topic already exists: {topic.title}")

def create_modules_for_topic(topic):
    """Create modules for a specific topic."""
    module_types = ['video', 'mcq', 'clinical_case', 'q_bank', 'flash_card']
    
    # Create 2-5 modules per topic
    num_modules = random.randint(2, 5)
    
    for i in range(num_modules):
        module_type = topic.category.name
        module_title = f"{topic.title} Module {i + 1}"
        
        module, created = NotesModule.objects.get_or_create(
            topic=topic,
            title=module_title,
            defaults={
                'module_type': module_type,
                'description': f'Comprehensive {module_type} content for {topic.title}.',
                'content_url': f'https://example.com/{module_type}/{topic.id}/{i + 1}',
                'duration_minutes': random.randint(15, 60),
                'views_count': random.randint(10, 500),
                'likes_count': random.randint(0, 50),
                'is_active': True,
                'is_premium': random.choice([True, False]),
                'order': i + 1,
            }
        )
        
        if created:
            print(f"    Created module: {module.title}")
            # Create specific content based on module type
            create_specific_content(module)
        else:
            print(f"    Module already exists: {module.title}")

def create_specific_content(module):
    """Create specific content based on module type."""
    if module.module_type == 'video':
        create_video_content(module)
    elif module.module_type == 'mcq':
        create_mcq_content(module)
    elif module.module_type == 'clinical_case':
        create_clinical_case_content(module)
    elif module.module_type == 'q_bank':
        create_q_bank_content(module)
    elif module.module_type == 'flash_card':
        create_flash_card_content(module)

def create_video_content(module):
    """Create video content for a module."""
    video, created = NotesVideo.objects.get_or_create(
        module=module,
        defaults={
            'video_url': f'https://example.com/videos/{module.id}.mp4',
            'thumbnail_url': f'https://example.com/thumbnails/{module.id}.jpg',
            'duration_seconds': random.randint(300, 3600),  # 5-60 minutes
            'quality': random.choice(['360p', '480p', '720p', '1080p']),
            'views_count': random.randint(10, 500),
            'likes_count': random.randint(0, 50),
        }
    )
    
    if created:
        print(f"      Created video content for: {module.title}")

def create_mcq_content(module):
    """Create MCQ content for a module."""
    # Select a random MCQ question
    mcq_data = random.choice(MCQ_QUESTIONS)
    
    mcq, created = NotesMCQ.objects.get_or_create(
        module=module,
        defaults={
            'question_text': mcq_data['question'],
            'explanation': mcq_data['explanation'],
            'attempts_count': random.randint(5, 100),
            'correct_answers_count': random.randint(2, 80),
        }
    )
    
    if created:
        print(f"      Created MCQ content for: {module.title}")
        # Create options for this MCQ
        create_mcq_options(mcq, mcq_data)

def create_mcq_options(mcq, mcq_data):
    """Create options for an MCQ."""
    for i, option_text in enumerate(mcq_data['options']):
        option, created = NotesMCQOption.objects.get_or_create(
            mcq=mcq,
            option_text=option_text,
            defaults={
                'is_correct': (i == mcq_data['correct']),
                'order': i + 1,
            }
        )
        
        if created:
            print(f"        Created MCQ option: {option_text}")

def create_clinical_case_content(module):
    """Create clinical case content for a module."""
    case_data = random.choice(CLINICAL_CASES)
    
    case, created = NotesClinicalCase.objects.get_or_create(
        module=module,
        defaults={
            'case_title': case_data['title'],
            'patient_history': case_data['patient_history'],
            'clinical_findings': case_data['clinical_findings'],
            'diagnosis': case_data['diagnosis'],
            'treatment': case_data['treatment'],
            'views_count': random.randint(5, 100),
        }
    )
    
    if created:
        print(f"      Created clinical case for: {module.title}")

def create_q_bank_content(module):
    """Create Q-Bank content for a module."""
    q_bank, created = NotesQBank.objects.get_or_create(
        module=module,
        defaults={
            'question_text': f'Q-Bank question for {module.title}',
            'explanation': f'Detailed explanation for the question in {module.title}',
            'difficulty_level': random.choice(['easy', 'medium', 'hard']),
            'attempts_count': random.randint(10, 200),
            'correct_answers_count': random.randint(5, 150),
        }
    )
    
    if created:
        print(f"      Created Q-Bank content for: {module.title}")

def create_flash_card_content(module):
    """Create flash card content for a module."""
    card_data = random.choice(FLASH_CARDS)
    
    flash_card, created = NotesFlashCard.objects.get_or_create(
        module=module,
        defaults={
            'front_text': card_data['front'],
            'back_text': card_data['back'],
            'category': card_data['category'],
            'views_count': random.randint(5, 50),
            'mastery_level': random.randint(0, 100),
        }
    )
    
    if created:
        print(f"      Created flash card for: {module.title}")

def create_statistics():
    """Create sample statistics."""
    print("Creating statistics...")
    
    # Create statistics for the last 30 days
    for i in range(30):
        stat_date = date.today() - timedelta(days=i)
        
        stats, created = NotesStatistics.objects.get_or_create(
            date=stat_date,
            defaults={
                'total_views': random.randint(100, 1000),
                'total_modules_accessed': random.randint(50, 200),
                'total_unique_users': random.randint(20, 100),
                'video_views': random.randint(30, 300),
                'mcq_attempts': random.randint(40, 400),
                'clinical_case_views': random.randint(20, 150),
                'q_bank_attempts': random.randint(25, 200),
                'flash_card_views': random.randint(15, 100),
            }
        )
        
        if created:
            print(f"Created statistics for: {stat_date}")
        else:
            print(f"Statistics already exist for: {stat_date}")

def main():
    """Main function to create comprehensive notes dummy data."""
    print("Creating comprehensive notes dummy data...")
    
    # Create categories and topics
    create_categories()
    
    # Create statistics
    create_statistics()
    
    print("\nComprehensive notes dummy data creation completed!")
    print("Created categories, topics, modules, and statistics.")

if __name__ == '__main__':
    main() 