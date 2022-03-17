import csv

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from website.models.reservation import Reservation
from website.models.guest import Guest
from distutils.util import strtobool
from django.core import serializers

required_csv_columns = [
    'name',
]
optional_csv_columns = [
    'initial_guests',
    'access_code',
    'max_guests',
    'mailing_address_line_1',
    'mailing_address_line_2',
    'mailing_address_city',
    'mailing_address_state',
    'mailing_address_zip',
    'invited_to_rehearsal'
]


class Command(BaseCommand):
    help = "Usage: 'import_reservations <path_to_reservations.csv>''"

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', nargs=1, type=str)

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path'][0]
        curr_row = 0
        new_reservations = 0
        updated_reservations = 0
        with open(csv_file_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for col in reader.fieldnames:
                if col not in required_csv_columns and col not in optional_csv_columns:
                    raise ValueError("Invalid column '%s'" % col)
            for row in reader:
                curr_row += 1
                for key in row.keys():
                    row[key] = str(row[key]).strip()
                    if not row[key]:
                        del row[key]
                if len(row.keys()) == 0:
                    continue
                for required_col in required_csv_columns:
                    if required_col not in row:
                        raise ValueError("Missing column '%s' in row %d: %s" % (required_col, curr_row, row))
                    try:
                        new, updated = self.save_reservation(row)
                    except Exception as e:
                        raise Exception("Failed to save reservation in row %d: %s" % (curr_row, row)) from e
                    if new:
                        new_reservations += 1
                    if updated:
                        updated_reservations += 1
        self.stdout.write('Successfully created %d and updated %d reservations' % (
            new_reservations,
            updated_reservations
        ))

    @staticmethod
    def save_reservation(row: dict) -> tuple[bool, bool]:
        name = row["name"]
        try:
            res = Reservation.objects.filter(name__exact=name).get()
            new = False
        except ObjectDoesNotExist:
            res = Reservation.objects.create(name=name)
            new = True

        max_guests = None
        if 'initial_guests' in row and new:
            guest_count = 0
            for guest_full_name in str(row['initial_guests']).split(','):
                if len(guest_full_name.strip()) == 0:
                    continue
                name_parts = guest_full_name.split(' ')
                if len(name_parts) < 2:
                    raise ValueError(
                        "initial_guests must by a list of guest first and last names, but got guest '%s'" % guest_full_name)
                Guest.objects.create(
                    reservation=res,
                    first_name=" ".join(name_parts[0:-1]),
                    last_name=name_parts[-1]
                )
                guest_count += 1
            max_guests = max(guest_count, 2)
        updated = False
        if 'access_code' in row:
            access_code = str(row['access_code'])
            if res.access_code != access_code:
                res.access_code = access_code
                updated = True
        if 'max_guests' in row or max_guests is not None:
            if 'max_guests' in row:
                max_guests = int(row['max_guests'])
            if res.max_guests != max_guests:
                res.max_guests = max_guests
                updated = True
        if 'mailing_address_line_1' in row:
            mailing_address_line_1 = str(row['mailing_address_line_1'])
            if res.mailing_address_line_1 != mailing_address_line_1:
                res.mailing_address_line_1 = mailing_address_line_1
                updated = True
        if 'mailing_address_line_2' in row:
            mailing_address_line_2 = str(row['mailing_address_line_2'])
            if res.mailing_address_line_2 != mailing_address_line_2:
                res.mailing_address_line_2 = mailing_address_line_2
                updated = True
        if 'mailing_address_city' in row:
            mailing_address_city = str(row['mailing_address_city'])
            if res.mailing_address_city != mailing_address_city:
                res.mailing_address_city = mailing_address_city
                updated = True
        if 'mailing_address_state' in row:
            mailing_address_state = str(row['mailing_address_state'])
            if res.mailing_address_state != mailing_address_state:
                res.mailing_address_state = mailing_address_state
                updated = True
        if 'mailing_address_zip' in row:
            mailing_address_zip = str(row['mailing_address_zip'])
            if res.mailing_address_zip != mailing_address_zip:
                res.mailing_address_zip = mailing_address_zip
                updated = True
        if 'invited_to_rehearsal' in row:
            invited_to_rehearsal = strtobool(row['invited_to_rehearsal'])
            if res.invited_to_rehearsal != invited_to_rehearsal:
                res.invited_to_rehearsal = invited_to_rehearsal
                updated = True
        if updated:
            try:
                res.save()
            except Exception as e:
                raise Exception("Failed to save reservation %s made from row %s" % (serializers.serialize('json', [res]), row)) from e
        return new, (not new and updated)
