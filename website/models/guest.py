from django.contrib import admin
from django.db import models
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
    food_vegan_option = models.BooleanField(default=False, blank=True, null=True)
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
        'reservation__id',
        'reservation__access_code',
        'reservation__name',
        'first_name',
        'last_name',
        'updated_at',
        'rsvp_answer_display',
        'food_vegan_option',
    )
    list_filter = (
        'rsvp_answer',
        'food_vegan_option',
    )

    @staticmethod
    def reservation__id(obj: Guest):
        return obj.reservation.id

    @staticmethod
    def reservation__access_code(obj: Guest):
        return obj.reservation.access_code

    @staticmethod
    def reservation__name(obj: Guest):
        return obj.reservation.name
