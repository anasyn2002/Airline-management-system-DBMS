# airline_app/management/commands/create_test_user.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a test user for development'

    def handle(self, *args, **kwargs):
        username = 'staff'
        email = 'staff@airline.com'
        password = 'staffpassword'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists'))
        else:
            User.objects.create_user(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created user "{username}" with password "{password}"'))