import logging

from django.contrib.auth.models import Group

logger = logging.getLogger(__name__)

WEDDING_PARTY = "Wedding Party"

functional_groups = [
    WEDDING_PARTY
]

for group in functional_groups:
    if not Group.objects.filter(name__exact=group).exists():
        Group.objects.create(name=group)
        logger.warning("Created missing functional user group '%s'", group)
