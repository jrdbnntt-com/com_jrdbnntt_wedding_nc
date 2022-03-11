from django.db.models.signals import post_save
from django.dispatch import receiver

from website.core.tasks import schedule_send_rsvp_updated_email
from website.models.reservation import Reservation


def init():
    """ Does nothing, just here to keep import """
    pass


@receiver(post_save, sender=Reservation)
def reservation_post_save(sender, instance: Reservation, created, raw, using, update_fields, **kwargs):
    """ Send rsvp updated email if rsvp updated """
    if not created and update_fields is not None and "rsvp_updated" in update_fields:
        schedule_send_rsvp_updated_email(instance.id)
