from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Follow
from posts.models import Post

User = get_user_model()

class Command(BaseCommand):
    help = "Cria usuários e posts de teste"

    def handle(self, *args, **options):
        me, _ = User.objects.get_or_create(username="tester", defaults={"password": "tester123"})
        u2, _ = User.objects.get_or_create(username="bob", defaults={"password": "bob123"})
        u3, _ = User.objects.get_or_create(username="carol", defaults={"password": "carol123"})

        Follow.objects.get_or_create(follower=me, following=u2)
        Follow.objects.get_or_create(follower=me, following=u3)

        Post.objects.get_or_create(author=u2, content="Post do Bob 1")
        Post.objects.get_or_create(author=u2, content="Post do Bob 2")
        Post.objects.get_or_create(author=u3, content="Post da Carol 1")

        self.stdout.write(self.style.SUCCESS("Usuários e posts de teste criados."))
