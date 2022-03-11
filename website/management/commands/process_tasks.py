from django.core.management.base import BaseCommand

from website.core.tasks import process_all_processable_tasks


class Command(BaseCommand):
    help = "Usage: 'process_tasks'"

    def handle(self, *args, **options):
        process_all_processable_tasks()
