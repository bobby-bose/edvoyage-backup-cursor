import os
import django
import random
from django.utils.text import slugify
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edvoayge.settings')
django.setup()

from universities.models import University, UniversityProgram, UniversityFaculty, UniversityResearch, UniversityPartnership, UniversityRanking, Campus
from django.utils import timezone

# Comprehensive dummy data
UNIVERSITY_DATA = [
    {
        'name': 'Stanford International University',
        'short_name': 'SIU',
        'description': 'Stanford International University is a prestigious research institution known for its innovative approach to education and cutting-edge research facilities. Founded in 1891, SIU has consistently ranked among the top universities globally.',
        'mission_statement': 'To advance knowledge and educate students in science, technology, and other areas of scholarship that will best serve the nation and the world in the 21st century.',
        'vision_statement': 'To be a leading research university that addresses the world\'s most pressing challenges through innovative education and groundbreaking research.',
        'university_type': 'research',
        'founded_year': 1891,
        'accreditation': 'Accredited by the Higher Learning Commission and various specialized accrediting agencies.',
        'website': 'https://www.stanford-international.edu',
        'email': 'info@stanford-international.edu',
        'phone': '+1-650-723-2300',
        'country': 'USA',
        'state': 'California',
        'city': 'Stanford',
        'address': '450 Serra Mall, Stanford, CA 94305',
        'postal_code': '94305',
        'total_students': 17000,
        'international_students': 5100,
        'faculty_count': 2200,
        'logo': 'https://images.shiksha.com/mediadata/images/articles/1744019588phpVCRWzS.jpeg',
        'gallery': [
            'https://www.topuniversities.com/sites/default/files/harvard_1.jpg',
            'https://images.unsplash.com/photo-1562774053-701939374585?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1541339907198-0875adf6a1b5?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80'
        ]
    },
    {
        'name': 'Oxford Global Institute',
        'short_name': 'OGI',
        'description': 'Oxford Global Institute is a world-renowned institution of higher learning, combining centuries of academic tradition with modern innovation. Our diverse community of scholars and students from over 150 countries creates a vibrant intellectual environment.',
        'mission_statement': 'To provide world-class education and research opportunities that inspire students to become global leaders and innovators.',
        'vision_statement': 'To be the most respected and influential university in the world, known for excellence in teaching, research, and global impact.',
        'university_type': 'international',
        'founded_year': 1096,
        'accreditation': 'Accredited by the Quality Assurance Agency for Higher Education and various international accrediting bodies.',
        'website': 'https://www.oxford-global.edu',
        'email': 'admissions@oxford-global.edu',
        'phone': '+44-1865-270000',
        'country': 'UK',
        'state': 'England',
        'city': 'Oxford',
        'address': 'University Offices, Wellington Square, Oxford OX1 2JD',
        'postal_code': 'OX1 2JD',
        'total_students': 24000,
        'international_students': 7200,
        'faculty_count': 3500,
        'logo': 'https://images.shiksha.com/mediadata/images/articles/1744019588phpVCRWzS.jpeg',
        'gallery': [
            'https://www.topuniversities.com/sites/default/files/harvard_1.jpg',
            'https://images.unsplash.com/photo-1562774053-701939374585?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1541339907198-0875adf6a1b5?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80'
        ]
    },
    {
        'name': 'Tokyo Advanced University of Technology',
        'short_name': 'TAUT',
        'description': 'Tokyo Advanced University of Technology is a leading institution specializing in engineering, technology, and innovation. With state-of-the-art facilities and industry partnerships, we prepare students for the future of technology.',
        'mission_statement': 'To foster innovation and technological advancement through excellence in education, research, and industry collaboration.',
        'vision_statement': 'To be the premier technological university in Asia, driving innovation and sustainable development.',
        'university_type': 'technical',
        'founded_year': 1877,
        'accreditation': 'Accredited by the Japan University Accreditation Association and international engineering accreditation bodies.',
        'website': 'https://www.tokyo-advanced-tech.edu',
        'email': 'info@tokyo-advanced-tech.edu',
        'phone': '+81-3-5734-2000',
        'country': 'Japan',
        'state': 'Tokyo',
        'city': 'Tokyo',
        'address': '2-12-1 Ookayama, Meguro-ku, Tokyo 152-8550',
        'postal_code': '152-8550',
        'total_students': 10500,
        'international_students': 2100,
        'faculty_count': 1200,
        'logo': 'https://images.shiksha.com/mediadata/images/articles/1744019588phpVCRWzS.jpeg',
        'gallery': [
            'https://www.topuniversities.com/sites/default/files/harvard_1.jpg',
            'https://images.unsplash.com/photo-1562774053-701939374585?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1541339907198-0875adf6a1b5?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80'
        ]
    }
]

PROGRAM_DATA = [
    # Stanford International University Programs
    {
        'name': 'Bachelor of Science in Computer Science',
        'program_level': 'undergraduate',
        'program_type': 'full_time',
        'description': 'A comprehensive program covering algorithms, data structures, software engineering, and artificial intelligence.',
        'objectives': 'To prepare students for careers in software development, data science, and technology leadership.',
        'outcomes': 'Graduates will be proficient in programming, problem-solving, and system design.',
        'duration_years': 4,
        'total_credits': 120,
        'semesters': 2,
        'entry_requirements': 'High school diploma with strong mathematics background, SAT/ACT scores.',
        'language_requirements': 'TOEFL 100 or IELTS 7.0 for international students.'
    },
    {
        'name': 'Master of Business Administration',
        'program_level': 'graduate',
        'program_type': 'full_time',
        'description': 'Advanced business program focusing on leadership, strategy, and global management.',
        'objectives': 'To develop business leaders with strategic thinking and global perspective.',
        'outcomes': 'Graduates will be prepared for executive leadership roles in global organizations.',
        'duration_years': 2,
        'total_credits': 60,
        'semesters': 2,
        'entry_requirements': 'Bachelor\'s degree, GMAT/GRE scores, work experience preferred.',
        'language_requirements': 'TOEFL 100 or IELTS 7.0 for international students.'
    },
    {
        'name': 'PhD in Engineering',
        'program_level': 'phd',
        'program_type': 'full_time',
        'description': 'Research-focused doctoral program in various engineering disciplines.',
        'objectives': 'To advance knowledge in engineering through original research.',
        'outcomes': 'Graduates will be prepared for academic and research careers.',
        'duration_years': 5,
        'total_credits': 90,
        'semesters': 2,
        'entry_requirements': 'Master\'s degree in engineering, research proposal.',
        'language_requirements': 'TOEFL 100 or IELTS 7.0 for international students.'
    },
    # Oxford Global Institute Programs
    {
        'name': 'Bachelor of Arts in International Relations',
        'program_level': 'undergraduate',
        'program_type': 'full_time',
        'description': 'Comprehensive study of global politics, economics, and international cooperation.',
        'objectives': 'To prepare students for careers in diplomacy, international organizations, and global policy.',
        'outcomes': 'Graduates will understand global systems and international cooperation.',
        'duration_years': 3,
        'total_credits': 90,
        'semesters': 3,
        'entry_requirements': 'A-levels or equivalent, strong academic record.',
        'language_requirements': 'IELTS 7.0 or equivalent for international students.'
    },
    {
        'name': 'Master of Science in Economics',
        'program_level': 'graduate',
        'program_type': 'full_time',
        'description': 'Advanced study of economic theory, econometrics, and policy analysis.',
        'objectives': 'To develop analytical skills for economic research and policy-making.',
        'outcomes': 'Graduates will be prepared for careers in research, consulting, and policy.',
        'duration_years': 1,
        'total_credits': 45,
        'semesters': 3,
        'entry_requirements': 'Bachelor\'s degree in economics or related field.',
        'language_requirements': 'IELTS 7.0 or equivalent for international students.'
    },
    # Tokyo Advanced University Programs
    {
        'name': 'Bachelor of Engineering in Mechanical Engineering',
        'program_level': 'undergraduate',
        'program_type': 'full_time',
        'description': 'Comprehensive engineering program covering mechanics, materials, and manufacturing.',
        'objectives': 'To prepare students for careers in mechanical engineering and manufacturing.',
        'outcomes': 'Graduates will be proficient in mechanical design and analysis.',
        'duration_years': 4,
        'total_credits': 130,
        'semesters': 2,
        'entry_requirements': 'High school diploma with strong mathematics and physics.',
        'language_requirements': 'JLPT N2 or equivalent for international students.'
    },
    {
        'name': 'Master of Engineering in Robotics',
        'program_level': 'graduate',
        'program_type': 'full_time',
        'description': 'Advanced program in robotics, automation, and artificial intelligence.',
        'objectives': 'To develop expertise in robotics and automation systems.',
        'outcomes': 'Graduates will be prepared for careers in robotics and automation.',
        'duration_years': 2,
        'total_credits': 60,
        'semesters': 2,
        'entry_requirements': 'Bachelor\'s degree in engineering or related field.',
        'language_requirements': 'JLPT N2 or equivalent for international students.'
    }
]

FACULTY_DATA = [
    {
        'name': 'School of Engineering',
        'short_name': 'SOE',
        'description': 'Leading engineering education with cutting-edge research and industry partnerships.',
        'mission': 'To advance engineering knowledge and prepare future engineering leaders.',
        'email': 'engineering@stanford-international.edu',
        'phone': '+1-650-723-2301',
        'website': 'https://engineering.stanford-international.edu',
        'student_count': 4500,
        'faculty_count': 350
    },
    {
        'name': 'School of Business',
        'short_name': 'SOB',
        'description': 'World-class business education with global perspective and industry connections.',
        'mission': 'To develop business leaders who drive innovation and sustainable growth.',
        'email': 'business@stanford-international.edu',
        'phone': '+1-650-723-2302',
        'website': 'https://business.stanford-international.edu',
        'student_count': 2800,
        'faculty_count': 220
    },
    {
        'name': 'Faculty of Social Sciences',
        'short_name': 'FSS',
        'description': 'Comprehensive study of human society, behavior, and social systems.',
        'mission': 'To advance understanding of social systems and human behavior.',
        'email': 'socialsciences@oxford-global.edu',
        'phone': '+44-1865-270001',
        'website': 'https://socialsciences.oxford-global.edu',
        'student_count': 3200,
        'faculty_count': 280
    },
    {
        'name': 'Faculty of Technology',
        'short_name': 'FOT',
        'description': 'Advanced technology education with focus on innovation and practical applications.',
        'mission': 'To advance technological innovation and prepare future technology leaders.',
        'email': 'technology@tokyo-advanced-tech.edu',
        'phone': '+81-3-5734-2001',
        'website': 'https://technology.tokyo-advanced-tech.edu',
        'student_count': 3800,
        'faculty_count': 320
    }
]

RESEARCH_DATA = [
    {
        'title': 'Artificial Intelligence in Healthcare',
        'research_area': 'technology',
        'description': 'Developing AI systems for early disease detection and personalized medicine.',
        'objectives': 'To improve healthcare outcomes through AI-powered diagnostic tools.',
        'methodology': 'Machine learning algorithms applied to medical imaging and patient data.',
        'funding_amount': 2500000.00,
        'funding_source': 'National Institutes of Health',
        'start_date': date(2023, 1, 15),
        'end_date': date(2026, 1, 15),
        'status': 'ongoing'
    },
    {
        'title': 'Sustainable Energy Solutions',
        'research_area': 'engineering',
        'description': 'Developing renewable energy technologies for urban environments.',
        'objectives': 'To create sustainable energy solutions for smart cities.',
        'methodology': 'Experimental research with computational modeling and field testing.',
        'funding_amount': 1800000.00,
        'funding_source': 'Department of Energy',
        'start_date': date(2022, 6, 1),
        'end_date': date(2025, 6, 1),
        'status': 'ongoing'
    },
    {
        'title': 'Global Economic Policy Analysis',
        'research_area': 'social_sciences',
        'description': 'Analyzing the impact of international trade policies on economic development.',
        'objectives': 'To inform policy decisions for sustainable economic growth.',
        'methodology': 'Economic modeling and statistical analysis of global trade data.',
        'funding_amount': 1200000.00,
        'funding_source': 'World Bank',
        'start_date': date(2023, 3, 1),
        'end_date': date(2025, 3, 1),
        'status': 'ongoing'
    },
    {
        'title': 'Advanced Robotics Systems',
        'research_area': 'technology',
        'description': 'Developing next-generation robotics for industrial automation.',
        'objectives': 'To create intelligent robotic systems for manufacturing.',
        'methodology': 'Robotics engineering with AI integration and sensor technology.',
        'funding_amount': 3200000.00,
        'funding_source': 'Ministry of Economy, Trade and Industry',
        'start_date': date(2022, 9, 1),
        'end_date': date(2026, 9, 1),
        'status': 'ongoing'
    }
]

PARTNERSHIP_DATA = [
    {
        'partner_name': 'MIT Technology Institute',
        'partnership_type': 'research',
        'description': 'Collaborative research in artificial intelligence and machine learning.',
        'objectives': 'To advance AI research through joint projects and student exchanges.',
        'partner_contact': 'Dr. Sarah Johnson',
        'partner_email': 'sarah.johnson@mit.edu',
        'partner_website': 'https://www.mit.edu',
        'start_date': date(2022, 1, 1),
        'end_date': date(2027, 1, 1),
        'status': 'active'
    },
    {
        'partner_name': 'Cambridge University',
        'partnership_type': 'academic',
        'description': 'Joint degree programs and faculty exchange initiatives.',
        'objectives': 'To provide students with international academic opportunities.',
        'partner_contact': 'Prof. Michael Brown',
        'partner_email': 'michael.brown@cam.ac.uk',
        'partner_website': 'https://www.cam.ac.uk',
        'start_date': date(2021, 9, 1),
        'end_date': date(2026, 9, 1),
        'status': 'active'
    },
    {
        'partner_name': 'Sony Corporation',
        'partnership_type': 'research',
        'description': 'Collaborative research in robotics and automation technology.',
        'objectives': 'To develop advanced robotics solutions for industry.',
        'partner_contact': 'Dr. Hiroshi Tanaka',
        'partner_email': 'hiroshi.tanaka@sony.com',
        'partner_website': 'https://www.sony.com',
        'start_date': date(2023, 4, 1),
        'end_date': date(2028, 4, 1),
        'status': 'active'
    }
]

RANKING_DATA = [
    {
        'ranking_type': 'world',
        'ranking_source': 'QS World University Rankings',
        'rank': 3,
        'total_institutions': 1000,
        'score': 98.5,
        'year': 2024,
        'methodology': 'Based on academic reputation, employer reputation, faculty/student ratio, citations per faculty, international faculty ratio, and international student ratio.'
    },
    {
        'ranking_type': 'world',
        'ranking_source': 'Times Higher Education',
        'rank': 5,
        'total_institutions': 1500,
        'score': 95.2,
        'year': 2024,
        'methodology': 'Based on teaching, research, citations, industry income, and international outlook.'
    },
    {
        'ranking_type': 'world',
        'ranking_source': 'QS World University Rankings',
        'rank': 2,
        'total_institutions': 1000,
        'score': 99.1,
        'year': 2024,
        'methodology': 'Based on academic reputation, employer reputation, faculty/student ratio, citations per faculty, international faculty ratio, and international student ratio.'
    },
    {
        'ranking_type': 'world',
        'ranking_source': 'Times Higher Education',
        'rank': 1,
        'total_institutions': 1500,
        'score': 99.8,
        'year': 2024,
        'methodology': 'Based on teaching, research, citations, industry income, and international outlook.'
    },
    {
        'ranking_type': 'world',
        'ranking_source': 'QS World University Rankings',
        'rank': 15,
        'total_institutions': 1000,
        'score': 92.3,
        'year': 2024,
        'methodology': 'Based on academic reputation, employer reputation, faculty/student ratio, citations per faculty, international faculty ratio, and international student ratio.'
    },
    {
        'ranking_type': 'world',
        'ranking_source': 'Times Higher Education',
        'rank': 12,
        'total_institutions': 1500,
        'score': 91.7,
        'year': 2024,
        'methodology': 'Based on teaching, research, citations, industry income, and international outlook.'
    }
]

def create_universities():
    """Create universities with comprehensive data."""
    universities = []
    
    for i, uni_data in enumerate(UNIVERSITY_DATA):
        slug = slugify(uni_data['name'])
        
        uni, created = University.objects.get_or_create(
            name=uni_data['name'],
            defaults={
                'short_name': uni_data['short_name'],
                'slug': slug,
                'description': uni_data['description'],
                'mission_statement': uni_data['mission_statement'],
                'vision_statement': uni_data['vision_statement'],
                'university_type': uni_data['university_type'],
                'founded_year': uni_data['founded_year'],
                'accreditation': uni_data['accreditation'],
                'website': uni_data['website'],
                'email': uni_data['email'],
                'phone': uni_data['phone'],
                'country': uni_data['country'],
                'state': uni_data['state'],
                'city': uni_data['city'],
                'address': uni_data['address'],
                'postal_code': uni_data['postal_code'],
                'total_students': uni_data['total_students'],
                'international_students': uni_data['international_students'],
                'faculty_count': uni_data['faculty_count'],
                'logo': uni_data['logo'],
                'gallery': uni_data['gallery'],
                'is_active': True,
                'is_featured': True,
                'is_verified': True,
            }
        )
        
        if created:
            print(f"Created: {uni.name}")
        else:
            print(f"Already exists: {uni.name}")
        
        universities.append(uni)
    
    return universities

def create_programs(universities):
    """Create programs for universities."""
    program_index = 0
    
    for i, university in enumerate(universities):
        # Create 2-3 programs per university
        programs_per_uni = 2 if i == 2 else 3  # Last university gets 2 programs
        
        for j in range(programs_per_uni):
            if program_index < len(PROGRAM_DATA):
                program_data = PROGRAM_DATA[program_index]
                
                program, created = UniversityProgram.objects.get_or_create(
                    university=university,
                    name=program_data['name'],
                    defaults={
                        'program_level': program_data['program_level'],
                        'program_type': program_data['program_type'],
                        'description': program_data['description'],
                        'objectives': program_data['objectives'],
                        'outcomes': program_data['outcomes'],
                        'duration_years': program_data['duration_years'],
                        'total_credits': program_data['total_credits'],
                        'semesters': program_data['semesters'],
                        'entry_requirements': program_data['entry_requirements'],
                        'language_requirements': program_data['language_requirements'],
                        'is_active': True,
                        'is_featured': True,
                    }
                )
                
                if created:
                    print(f"Created program: {program.name} for {university.name}")
                else:
                    print(f"Program already exists: {program.name}")
                
                program_index += 1

def create_faculties(universities):
    """Create faculties for universities."""
    faculty_index = 0
    
    for i, university in enumerate(universities):
        # Create 1-2 faculties per university
        faculties_per_uni = 1 if i == 2 else 2  # Last university gets 1 faculty
        
        for j in range(faculties_per_uni):
            if faculty_index < len(FACULTY_DATA):
                faculty_data = FACULTY_DATA[faculty_index]
                
                faculty, created = UniversityFaculty.objects.get_or_create(
                    university=university,
                    name=faculty_data['name'],
                    defaults={
                        'short_name': faculty_data['short_name'],
                        'description': faculty_data['description'],
                        'mission': faculty_data['mission'],
                        'email': faculty_data['email'],
                        'phone': faculty_data['phone'],
                        'website': faculty_data['website'],
                        'student_count': faculty_data['student_count'],
                        'faculty_count': faculty_data['faculty_count'],
                        'is_active': True,
                    }
                )
                
                if created:
                    print(f"Created faculty: {faculty.name} for {university.name}")
                else:
                    print(f"Faculty already exists: {faculty.name}")
                
                faculty_index += 1

def create_research(universities):
    """Create research projects for universities."""
    research_index = 0
    
    for i, university in enumerate(universities):
        # Create 1-2 research projects per university
        research_per_uni = 1 if i == 1 else 2  # Middle university gets 1 research
        
        for j in range(research_per_uni):
            if research_index < len(RESEARCH_DATA):
                research_data = RESEARCH_DATA[research_index]
                
                research, created = UniversityResearch.objects.get_or_create(
                    university=university,
                    title=research_data['title'],
                    defaults={
                        'research_area': research_data['research_area'],
                        'description': research_data['description'],
                        'objectives': research_data['objectives'],
                        'methodology': research_data['methodology'],
                        'funding_amount': research_data['funding_amount'],
                        'funding_source': research_data['funding_source'],
                        'start_date': research_data['start_date'],
                        'end_date': research_data['end_date'],
                        'status': research_data['status'],
                    }
                )
                
                if created:
                    print(f"Created research: {research.title} for {university.name}")
                else:
                    print(f"Research already exists: {research.title}")
                
                research_index += 1

def create_partnerships(universities):
    """Create partnerships for universities."""
    partnership_index = 0
    
    for i, university in enumerate(universities):
        # Create 1 partnership per university
        if partnership_index < len(PARTNERSHIP_DATA):
            partnership_data = PARTNERSHIP_DATA[partnership_index]
            
            partnership, created = UniversityPartnership.objects.get_or_create(
                university=university,
                partner_name=partnership_data['partner_name'],
                defaults={
                    'partnership_type': partnership_data['partnership_type'],
                    'description': partnership_data['description'],
                    'objectives': partnership_data['objectives'],
                    'partner_contact': partnership_data['partner_contact'],
                    'partner_email': partnership_data['partner_email'],
                    'partner_website': partnership_data['partner_website'],
                    'start_date': partnership_data['start_date'],
                    'end_date': partnership_data['end_date'],
                    'status': partnership_data['status'],
                }
            )
            
            if created:
                print(f"Created partnership: {partnership.partner_name} for {university.name}")
            else:
                print(f"Partnership already exists: {partnership.partner_name}")
            
            partnership_index += 1

def create_rankings(universities):
    """Create rankings for universities."""
    ranking_index = 0
    
    for i, university in enumerate(universities):
        # Create 2 rankings per university
        for j in range(2):
            if ranking_index < len(RANKING_DATA):
                ranking_data = RANKING_DATA[ranking_index]
                
                ranking, created = UniversityRanking.objects.get_or_create(
                    university=university,
                    ranking_type=ranking_data['ranking_type'],
                    ranking_source=ranking_data['ranking_source'],
                    year=ranking_data['year'],
                    defaults={
                        'rank': ranking_data['rank'],
                        'total_institutions': ranking_data['total_institutions'],
                        'score': ranking_data['score'],
                        'methodology': ranking_data['methodology'],
                    }
                )
                
                if created:
                    print(f"Created ranking: {ranking.ranking_type} for {university.name}")
                else:
                    print(f"Ranking already exists: {ranking.ranking_type}")
                
                ranking_index += 1

def main():
    """Main function to create comprehensive dummy data."""
    print("Creating comprehensive dummy data...")
    
    # Create universities
    universities = create_universities()
    
    # Create related data
    create_programs(universities)
    create_faculties(universities)
    create_research(universities)
    create_partnerships(universities)
    create_rankings(universities)
    
    print("\nComprehensive dummy data creation completed!")
    print(f"Created {len(universities)} universities with complete data.")

if __name__ == '__main__':
    main() 