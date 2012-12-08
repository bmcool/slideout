from django.core.management.base import BaseCommand
from django.core.management import call_command

from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('syncdb', interactive=False)
        call_command('migrate')
        
        game_maker_group, created = Group.objects.get_or_create(name='GameMaker')
        if created:
            add_level = Permission.objects.get(codename='add_slideoutlevel')
            change_level = Permission.objects.get(codename='change_slideoutlevel')
            delete_level = Permission.objects.get(codename='delete_slideoutlevel')
            
            game_maker_group.permissions.add(add_level)
            game_maker_group.permissions.add(change_level)
            game_maker_group.permissions.add(delete_level)
