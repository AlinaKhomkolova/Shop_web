from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу модераторов и назначает ей права'

    def handle(self, *args, **kwargs):
        group_name = 'Moderators'
        group, created = Group.objects.get_or_create(name=group_name)

        content_type = ContentType.objects.get_for_model(Product)

        permissions = [
            "can_change_product_status",
            "can_change_product_description",
            "can_change_product_category",
        ]
        for perm in permissions:
            permission = Permission.objects.get(codename=perm, content_type=content_type)
            group.permissions.add(permission)

        group.save()
        # Выводит сообщение для удобства
        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" создана и ей назначены права.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" уже существует. Права обновлены.'))
