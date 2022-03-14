from django.contrib import admin
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from website.models.reservation import Reservation


def init():
    """ Does nothing, just here to keep import """
    pass


class Guest(models.Model):
    """ A single guest for the event """
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    rsvp_answer = models.BooleanField(default=None, blank=True, null=True)
    rehearsal_rsvp_answer = models.BooleanField(default=None, blank=True, null=True)
    rsvp_comment = models.CharField(max_length=1000, blank=True)
    assigned_table = models.IntegerField(null=True, blank=True)
    assigned_table_seat = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self) -> str:
        return self.full_name()

    def full_name(self) -> str:
        return "{} {}".format(self.first_name, self.last_name)

    def full_name_rsvp(self) -> str:
        return "{} ({})".format(self.full_name(), self.rsvp_answer_display())

    def rsvp_answer_display(self) -> str:
        return self._answer_display(self.rsvp_answer)

    def rehearsal_rsvp_answer_display(self) -> str:
        if self.reservation.invited_to_rehearsal:
            return self._answer_display(self.rehearsal_rsvp_answer)
        return '(not invited)'

    @staticmethod
    def _answer_display(answer: bool) -> str:
        if answer is None:
            return "TBD"
        if answer:
            return "Going"
        return "Not Going"


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    ordering = ('last_name', 'first_name')
    list_display = (
        'reservation__access_code',
        'reservation__name',
        'first_name',
        'last_name',
        'updated_at',
        'rsvp_answer_display',
        'rehearsal_rsvp_answer_display',
        'rsvp_comment',
        'assigned_table',
        'assigned_table_seat',
    )
    list_filter = (
        'rsvp_answer',
        'rehearsal_rsvp_answer'
    )

    @staticmethod
    def reservation__access_code(obj: Guest):
        return obj.reservation.access_code

    @staticmethod
    def reservation__name(obj: Guest):
        return obj.reservation.name


@receiver(pre_save, sender=Guest)
def pre_save(sender, instance: Guest, **kwargs):
    """ Updates the updated_at timestamp prior to each save """
    instance.updated_at = timezone.now()


@receiver(post_save, sender=Guest)
def post_save(sender, instance: Guest, created, raw, using, update_fields, **kwargs):
    if update_fields is not None:
        update_fields = frozenset(update_fields)
        rsvp_updated = False
        reservation = None
        if "rsvp_answer" in update_fields or "rehearsal_rsvp_answer" in update_fields:
            rsvp_updated = True
        if rsvp_updated:
            if reservation is None:
                reservation = Guest.objects.only("reservation").get(pk=instance.id).reservation
            reservation.rsvp_updated_at = timezone.now()
            reservation.save()
