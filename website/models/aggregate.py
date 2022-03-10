from website.core.mail import send_rsvp_updated_email
from website.models.reservation import Reservation
from website.core.tasks import schedule_send_rsvp_updated_email


def init():
    """ Does nothing, just here to keep import """
    pass


@receiver(post_save, sender=Reservation)
def reservation_post_save(sender, instance: Reservation, created, raw, using, update_fields, **kwargs):
    """ Send rsvp updated email if rsvp updated """
    if not created and update_fields is not None and "rsvp_updated" in update_fields:
        schedule_send_rsvp_updated_email(instance.id)
