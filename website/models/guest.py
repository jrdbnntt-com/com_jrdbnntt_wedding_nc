from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib import admin
from datetime import datetime
from .reservation import Reservation
from .food_option import FoodOption


class Guest(models.Model):
    """ A single guest for the event """
    MAX_HIDDEN_PER_RESERVATION = 10
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    rsvp_answer = models.BooleanField(default=None)
    rsvp_comment = models.CharField(max_length=1000, blank=True)
    assigned_table = models.IntegerField(null=True, blank=True)
    assigned_table_seat = models.IntegerField(null=True, blank=True)
    food_selection = models.ForeignKey(FoodOption, on_delete=models.SET_NULL, null=True, blank=True)
    food_comment = models.CharField(max_length=1000, blank=True)
    hidden = models.BooleanField(default=False)  # "deleted" by reservation user
    created_at = models.DateTimeField(default=datetime.now, editable=False)
    updated_at = models.DateTimeField(default=datetime.now, editable=False)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name, self.rsvp_answer)


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    pass


@receiver(pre_save, sender=Guest)
def pre_save(sender, instance: Guest, **kwargs):
    """ Updates the updated_at timestamp prior to each save """
    instance.updated_at = datetime.now()


@receiver(post_save, sender=Guest)
def post_save(sender, instance: Guest, created, raw, using, update_fields, **kwargs):
    """ If hiding, delete other hidden Guest objects for the same reservation to ensure that there are at max 10 """
    if update_fields is not None:
        update_fields = frozenset(update_fields)
        if "hidden" in update_fields and instance.hidden:
            reservation = Guest.objects.only("reservation").get(pk=instance.id).reservation
            hidden_guests = Guest.objects.filter(reservation=reservation, hidden=True).order_by("-updated_at")
            if len(hidden_guests) > Guest.MAX_HIDDEN_PER_RESERVATION:
                hidden_guests[Guest.MAX_HIDDEN_PER_RESERVATION:].delete()
