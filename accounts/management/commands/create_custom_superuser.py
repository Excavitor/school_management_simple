import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser non-interactively using environment variables.'

    def handle(self, *args, **options):
        email = os.environ.get('SUPERUSER_EMAIL')
        password = os.environ.get('SUPERUSER_PASSWORD')

        if not all([email, password]):
            self.stdout.write(self.style.ERROR(
                'Missing environment variables: SUPERUSER_EMAIL, SUPERUSER_PASSWORD'
            ))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'User with email "{email}" already exists.'))
        else:
            User.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser with email "{email}" created successfully.'))