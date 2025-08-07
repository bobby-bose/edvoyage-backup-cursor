from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from cavity.models import User, Post, Comment, PostLike, CommentLike, PostShare
from datetime import datetime, timedelta
import uuid


class Command(BaseCommand):
    help = 'Add dummy data for Cavity app'

    def handle(self, *args, **options):
        self.stdout.write('Creating dummy data for Cavity app...')

        # Create users
        users_data = [
            {
                'username': 'dr_aisha',
                'email': 'aisha@example.com',
                'first_name': 'Aisha',
                'last_name': 'Rehman',
                'year_tag': '3rd year MBBS',
                'bio': 'Medical student passionate about cardiology',
                'is_verified': True,
            },
            {
                'username': 'med_student_john',
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'year_tag': '2nd year MBBS',
                'bio': 'Learning anatomy and physiology',
                'is_verified': False,
            },
            {
                'username': 'neet_aspirant',
                'email': 'neet@example.com',
                'first_name': 'Sarah',
                'last_name': 'Kumar',
                'year_tag': 'NEET 2025',
                'bio': 'Preparing for NEET 2025',
                'is_verified': False,
            },
            {
                'username': 'intern_doctor',
                'email': 'intern@example.com',
                'first_name': 'Dr. Rahul',
                'last_name': 'Sharma',
                'year_tag': 'Internship',
                'bio': 'Currently doing internship in surgery',
                'is_verified': True,
            },
            {
                'username': 'overseas_student',
                'email': 'overseas@example.com',
                'first_name': 'Maria',
                'last_name': 'Garcia',
                'year_tag': 'Overseas Edu',
                'bio': 'Studying medicine abroad',
                'is_verified': True,
            },
        ]

        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'year_tag': user_data['year_tag'],
                    'bio': user_data['bio'],
                    'is_verified': user_data['is_verified'],
                    'password': make_password('password123'),
                }
            )
            users.append(user)
            if created:
                self.stdout.write(f'Created user: {user.username}')

        # Create posts
        posts_data = [
            {
                'user': users[0],  # dr_aisha
                'content': 'Just finished my cardiology rotation! The ECG interpretation was challenging but fascinating. Learning to read different arrhythmias and understanding the cardiac cycle has been an amazing experience. The practical sessions with real patients really helped solidify the concepts.',
                'is_anonymous': False,
            },
            {
                'user': users[1],  # med_student_john
                'content': 'Anatomy lab today was intense! Dissecting the brachial plexus was both challenging and rewarding. The relationship between nerves, arteries, and veins is so intricate. Anyone have tips for memorizing the nerve pathways?',
                'is_anonymous': False,
            },
            {
                'user': users[2],  # neet_aspirant
                'content': 'NEET preparation going well! Physics is my weak point but I\'m improving. Chemistry and Biology are manageable. Any study group recommendations for Physics?',
                'is_anonymous': False,
            },
            {
                'user': users[3],  # intern_doctor
                'content': 'First day of surgery rotation! Assisted in an appendectomy today. The precision required in surgery is incredible. The team was amazing and taught me so much about sterile technique.',
                'is_anonymous': False,
            },
            {
                'user': users[4],  # overseas_student
                'content': 'Studying medicine in the UK has been an incredible experience. The approach to medical education here is quite different from back home. The emphasis on clinical reasoning and patient communication is excellent.',
                'is_anonymous': False,
            },
            {
                'user': users[0],  # dr_aisha
                'content': 'Had an interesting case today - a patient with atypical chest pain. The differential diagnosis included everything from GERD to acute coronary syndrome. Great learning experience in clinical reasoning!',
                'is_anonymous': False,
            },
        ]

        posts = []
        for i, post_data in enumerate(posts_data):
            # Create posts with different timestamps
            created_at = datetime.now() - timedelta(days=i, hours=i*2)
            post = Post.objects.create(
                user=post_data['user'],
                content=post_data['content'],
                is_anonymous=post_data['is_anonymous'],
                created_at=created_at,
            )
            posts.append(post)
            self.stdout.write(f'Created post: {post.content[:50]}...')

        # Create comments
        comments_data = [
            {
                'post': posts[0],
                'user': users[1],
                'content': 'Great experience! Which ECG findings did you find most interesting?',
            },
            {
                'post': posts[0],
                'user': users[3],
                'content': 'Cardiology is fascinating! Wait until you see your first STEMI case.',
            },
            {
                'post': posts[1],
                'user': users[0],
                'content': 'Try using mnemonics for nerve pathways. They really help!',
            },
            {
                'post': posts[2],
                'user': users[1],
                'content': 'Physics is tough but practice makes perfect. Try solving previous year questions.',
            },
            {
                'post': posts[3],
                'user': users[0],
                'content': 'Surgery is so exciting! The teamwork is incredible.',
            },
        ]

        for comment_data in comments_data:
            comment = Comment.objects.create(
                post=comment_data['post'],
                user=comment_data['user'],
                content=comment_data['content'],
            )
            self.stdout.write(f'Created comment: {comment.content[:30]}...')

        # Create likes
        like_combinations = [
            (users[1], posts[0]),  # john likes aisha's post
            (users[2], posts[0]),  # neet aspirant likes aisha's post
            (users[3], posts[0]),  # intern likes aisha's post
            (users[0], posts[1]),  # aisha likes john's post
            (users[2], posts[1]),  # neet aspirant likes john's post
            (users[0], posts[2]),  # aisha likes neet aspirant's post
            (users[1], posts[2]),  # john likes neet aspirant's post
            (users[0], posts[3]),  # aisha likes intern's post
            (users[1], posts[3]),  # john likes intern's post
        ]

        for user, post in like_combinations:
            PostLike.objects.get_or_create(
                user=user,
                post=post,
                defaults={'is_active': True}
            )
            self.stdout.write(f'{user.username} liked {post.user.username}\'s post')

        # Create shares
        share_combinations = [
            (users[1], posts[0], 'WhatsApp'),
            (users[2], posts[0], 'LinkedIn'),
            (users[0], posts[1], 'Facebook'),
        ]

        for user, post, platform in share_combinations:
            PostShare.objects.create(
                user=user,
                post=post,
                platform=platform,
            )
            self.stdout.write(f'{user.username} shared {post.user.username}\'s post on {platform}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created dummy data for Cavity app!')
        )
        self.stdout.write(f'Created {len(users)} users')
        self.stdout.write(f'Created {len(posts)} posts')
        self.stdout.write(f'Created {len(comments_data)} comments')
        self.stdout.write(f'Created {len(like_combinations)} likes')
        self.stdout.write(f'Created {len(share_combinations)} shares') 