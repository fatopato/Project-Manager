from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # Import the management comman  d to make sure it gets registered

        # Use a post_migrate signal to run the command after database is set up
        post_migrate.connect(self.run_management_command, sender=self)

    def run_management_command(self, **kwargs):
        # Run the management command when the app is ready
        from django.core.management import call_command
        call_command('create_groups')
