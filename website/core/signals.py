import logging

from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone

from website.core.tasks import schedule_send_rsvp_updated_email
from website.models.guest import Guest
from website.models.reservation import Reservation

logger = logging.getLogger(__name__)


def init():
    """ Does nothing, just here to keep import """
    pass


@receiver(pre_save, sender=Guest, dispatch_uid="guest_pre_save")
def guest_pre_save(sender, instance: Guest, **kwargs):
    """ Updates the updated_at timestamp prior to each save """
    instance.updated_at = timezone.now()


@receiver(post_save, sender=Guest, dispatch_uid="guest_post_save")
def guest_post_save(sender, instance: Guest, created, raw, using, update_fields, **kwargs):
    if created or update_fields is not None and (
            "rsvp_answer" in update_fields or "rehearsal_rsvp_answer" in update_fields):
        reservation = Guest.objects.only("reservation").get(pk=instance.id).reservation
        reservation.rsvp_updated_at = timezone.now()
        reservation.save(update_fields=['rsvp_updated_at'])


@receiver(pre_delete, sender=Guest, dispatch_uid="guest_pre_delete")
def guest_pre_delete(sender, instance: Guest, **kwargs):
    reservation = Guest.objects.only("reservation").get(pk=instance.id).reservation
    reservation.rsvp_updated_at = timezone.now()
    reservation.save(update_fields=['rsvp_updated_at'])


@receiver(pre_save, sender=Reservation, dispatch_uid="reservation_pre_save")
def reservation_pre_save(sender, instance: Reservation, update_fields, **kwargs):
    """ Updates the updated_at timestamp prior to each save """
    instance.updated_at = timezone.now()


@receiver(post_save, sender=Reservation, dispatch_uid="reservation_post_save")
def reservation_post_save(sender, instance: Reservation, created, raw, using, update_fields, **kwargs):
    if created or update_fields is not None and "rsvp_updated_at" in update_fields:
        schedule_send_rsvp_updated_email(instance.id)
