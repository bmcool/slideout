from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    def handle(self, *args, **options):
        game_maker_group, created = Group.objects.get_or_create(name='GameMaker')
        if created:
            add_level = Permission.objects.get(codename='add_level')
            change_level = Permission.objects.get(codename='change_level')
            delete_level = Permission.objects.get(codename='delete_level')
            
            game_maker_group.permissions.add(add_level)
            game_maker_group.permissions.add(change_level)
            game_maker_group.permissions.add(delete_level)
