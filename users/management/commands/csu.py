from django.core.management import BaseCommand
from more_itertools.more import first

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='adminka@gmail.com',
            first_name='Admin',
            last_name='Kot',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('120703')
        user.save()
