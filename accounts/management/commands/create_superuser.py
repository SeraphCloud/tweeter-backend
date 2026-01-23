from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = 'Cria um superusuário automaticamente'

    def handle(self, *args, **options):
        username = getattr(settings, 'SUPERUSER_USERNAME', 'admin')
        email = getattr(settings, 'SUPERUSER_EMAIL', 'admin@example.com')
        password = getattr(settings, 'SUPERUSER_PASSWORD', 'admin123')
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superusuário "{username}" criado com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Superusuário "{username}" já existe.')
            )