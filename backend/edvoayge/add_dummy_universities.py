import os
import django
import random
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edvoayge.settings')
django.setup()

from universities.models import University

TYPES = ['public', 'private', 'international', 'research', 'liberal_arts', 'technical', 'medical', 'business']
COUNTRIES = ['USA', 'UK', 'Canada', 'Australia', 'India', 'Germany', 'France', 'Japan', 'China', 'Brazil']
CITIES = ['New York', 'London', 'Toronto', 'Sydney', 'Mumbai', 'Berlin', 'Paris', 'Tokyo', 'Beijing', 'Sao Paulo']
LOGO_URL = 'https://images.shiksha.com/mediadata/images/articles/1744019588phpVCRWzS.jpeg'

for i in range(10):
    name = f"Dummy University {i+1}"
    short_name = f"DU{i+1}"
    slug = slugify(name)
    description = f"This is a dummy description for {name}."
    university_type = random.choice(TYPES)
    founded_year = random.randint(1850, 2020)
    country = COUNTRIES[i % len(COUNTRIES)]
    city = CITIES[i % len(CITIES)]
    website = f"https://www.dummyuniversity{i+1}.edu"
    email = f"info{(i+1)}@dummyuniversity.edu"
    phone = f"+1-555-000{i+1}"

    uni, created = University.objects.get_or_create(
        name=name,
        defaults={
            'short_name': short_name,
            'slug': slug,
            'description': description,
            'university_type': university_type,
            'founded_year': founded_year,
            'country': country,
            'city': city,
            'website': website,
            'email': email,
            'phone': phone,
            'is_active': True,
            'is_featured': False,
            'is_verified': False,
            'logo': LOGO_URL,
        }
    )
    if created:
        print(f"Created: {name}")
    else:
        print(f"Already exists: {name}") 