import logging

from django.contrib.auth.models import Group

logger = logging.getLogger(__name__)

WEDDING_PARTY = "Wedding Party"
REHEARSAL_GUESTS = "Rehearsal Guests"
WEDDING_GUESTS = "Wedding Guests"

functional_groups = [
    WEDDING_PARTY,
    REHEARSAL_GUESTS,
    WEDDING_GUESTS
]


def create_missing_functional_groups():
    for group in functional_groups:
        if not Group.objects.filter(name__exact=group).exists():
            Group.objects.create(name=group)
            logger.warning("Created missing functional user group '%s'", group)
