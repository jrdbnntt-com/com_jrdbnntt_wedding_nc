import random

from django.test import TestCase
from ...models.reservation import Reservation
from ...models.guest import Guest
import string
import secrets
import names
import logging

logger = logging.getLogger(__name__)

MOCK_NAME_PREFIX = "Test "


class MockTest(TestCase):
    def test_install_100_mock_reservations(self):
        total_reservations = Reservation.objects.count()
        total_guests = Guest.objects.count()

        for i in range(100):
            create_mock_reservation()

        total_reservations = Reservation.objects.count() - total_reservations
        total_guests = Guest.objects.count() - total_guests

        logger.info("Created a total of %d Reservations with %d Guests" % (total_reservations, total_guests))
        self.assertEqual(total_reservations, 100)

    def test_delete_all_reservations(self):
        for i in range(10):
            create_mock_reservation()
        deleted, _ = Reservation.objects.all().delete()
        logger.info('Deleted %d objects' % deleted)
        self.assertEqual(Reservation.objects.count(), 0)
        self.assertEqual(Guest.objects.count(), 0)


def random_str(length: int, charset=string.ascii_letters) -> str:
    return ''.join(secrets.choice(charset) for _ in range(length))


def create_mock_reservation():
    res = Reservation.objects.create(
        name=MOCK_NAME_PREFIX + names.get_last_name(),
    )
    guest_count = random.choices([1, 2, 3], [.20, .75, .05])[0]
    for _ in range(guest_count):
        Guest.objects.create(
            reservation=res,
            first_name=names.get_first_name(),
            last_name=names.get_last_name(),
            rsvp_answer=random.choices([True, False], [.90, .10])[0],
            food_comment=random.choices(["", "vegan", "vegetarian"], [.90, .5, .5])[0]
        )
    logger.info("Created mock reservation with %d guests named '%s'" % (guest_count, res.name))
