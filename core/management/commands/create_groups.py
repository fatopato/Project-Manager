from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

user_groups = ['PM', 'DEVELOPER', 'ANALYST']


class Command(BaseCommand):
    help = 'Create the User Groups'

    def handle(self, *args, **options):

        for group_name in user_groups:
            # Check if the group already exists
            if not Group.objects.filter(name=group_name).exists():
                # Create the group if it doesn't exist
                Group.objects.create(name=group_name)
                self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created successfully'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" already exists'))
