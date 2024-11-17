from django.core.management.base import BaseCommand
from faker import Faker
from apps.shorter.models import Link  
from apps.users.models import CustomUser  
import random

class Command(BaseCommand):
    help = "Populate the database with fake data"
    # python manage.py populate_fake_data --users 20 --links 100


    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help="Number of fake users to create")
        parser.add_argument('--links', type=int, default=50, help="Number of fake links to create")

    def handle(self, *args, **options):
        fake = Faker()
        users = []
        
        for _ in range(options['users']):
            user = CustomUser.objects.create_user(
                email=fake.email(),
                password="password123",  
                is_active=True
            )
            users.append(user)
        self.stdout.write(f"Created {len(users)} fake users.")

        for _ in range(options['links']):
            Link.objects.create(
                user=random.choice(users),
                original_url=fake.url(),
                short_code=fake.unique.lexify(text='??????'),  
            )
        self.stdout.write(f"Created {options['links']} fake links.")
