import sys

from django.apps import AppConfig


def run_for_migration():
    return 'migrate' in sys.argv or 'makemigrations' in sys.argv


class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self):
        from website.core.auth.user.groups import create_missing_functional_groups
        from website.core.signals import init as init_signals
        from website.core.tasks import start_processing_tasks_in_background
        init_signals()
        if not run_for_migration():
            create_missing_functional_groups()
            start_processing_tasks_in_background()
