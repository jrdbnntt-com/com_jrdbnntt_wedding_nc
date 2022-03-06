from django.core.management.base import BaseCommand, CommandError
from website.tests.models.mock import create_mock_reservation, MOCK_NAME_PREFIX
from website.models.reservation import Reservation


class Command(BaseCommand):
    help = "Usage: 'mock_reservation create <count>' or 'mock.reservation delete'"

    def add_arguments(self, parser):
        parser.add_argument('action', nargs=1, type=str)
        parser.add_argument('count', nargs='?', type=int, default=100)

    def handle(self, *args, **options):
        action = options['action'][0]
        if action == 'create':
            self.action_create(options['count'])
        elif action == 'delete':
            self.action_delete()
        else:
            raise CommandError("Invalid action '%s'" % action)

    def action_create(self, count: int):
        if count <= 0:
            raise CommandError("count must be greater than 1")
        self.stdout.write("Creating %d mock reservations..." % count)
        for _ in range(count):
            create_mock_reservation()
        self.stdout.write('Successfully created %d mock reservations' % count)

    def action_delete(self):
        self.stdout.write("Deleting all mock Reservation objects...")
        deleted, _ = Reservation.objects.filter(name__startswith=MOCK_NAME_PREFIX).delete()
        self.stdout.write("Successfully deleted all mock Reservation objects (%d total objects deleted)" % deleted)
