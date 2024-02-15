import csv
import time

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from website.models.reservation import Reservation
from website.models.guest import Guest
from distutils.util import strtobool
from django.core import serializers

csv_columns = [
    'name',
    'guests',
    'access_code',
    'max_guests',
]


class Command(BaseCommand):
    help = "Usage: 'export_reservations'"

    def handle(self, *args, **options):
        csv_file_path = 'logs/reservations_export_%d.csv' % int(time.time())
        self.stdout.write('Exporting reservations to %s' % csv_file_path)
        res_count = 0
        guest_count = 0
        with open(csv_file_path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for res in Reservation.objects.all().only('id', 'name', 'access_code', 'max_guests').order_by('id'):
                all_guest_names = []
                for guest in Guest.objects.filter(reservation__id=res.id).only('first_name', 'last_name').order_by('id'):
                    all_guest_names.append(guest.full_name())
                    guest_count += 1
                writer.writerow({
                    'name': res.name,
                    'guests': ", ".join(all_guest_names),
                    'access_code': res.access_code,
                    'max_guests': res.max_guests
                })
                res_count += 1
        self.stdout.write('Successfully exported %d reservations for %d known guests' % (
            res_count,
            guest_count
        ))