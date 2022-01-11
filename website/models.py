from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import datetime
import secrets as secrets
import string as string


class Reservation(models.Model):
    """ A guest reservation for one or more Guests. Used for accounts. """

    ACCESS_CODE_LENGTH = 6
    ACCESS_CODE_CHARS = string.ascii_uppercase + "23456789"

    @staticmethod
    def generate_access_code():
        return ''.join(secrets.choice(Reservation.ACCESS_CODE_CHARS) for _ in range(Reservation.ACCESS_CODE_LENGTH))

    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    access_code = models.CharField(max_length=ACCESS_CODE_LENGTH, default=generate_access_code)
    email = models.EmailField()  # Used as User.username and User.email upon User creation
    max_guests = models.IntegerField(default=2)
    rsvp_updated_at = models.DateTimeField()
    mailing_address_line_1 = models.CharField(max_length=200, blank=True)
    mailing_address_line_2 = models.CharField(max_length=200, blank=True)
    mailing_address_city = models.CharField(max_length=200, blank=True)
    mailing_address_state = models.CharField(max_length=2, blank=True)
    mailing_address_zip = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(default=datetime.now, editable=False)
    updated_at = models.DateTimeField(default=datetime.now, editable=False)


@receiver(pre_save, sender=Reservation)
def reservation_pre_save(sender, reservation: Reservation):
    """ Updates the updated_at timestamp prior to each save """
    reservation.updated_at = datetime.now()


class FoodOption(models.Model):
    """ Food options for catering """
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    picture_url = models.URLField(max_length=200)
    presentation_order = models.IntegerField(default=0)


class Guest(models.Model):
    """ A single guest for the event """
    MAX_HIDDEN_PER_RESERVATION = 10
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    rsvp_answer = models.BooleanField(default=None)
    rsvp_comment = models.CharField(max_length=1000, blank=True)
    assigned_table = models.IntegerField(max_length=100, blank=True)
    assigned_table_seat = models.IntegerField(max_length=100, blank=True)
    food_selection = models.ForeignKey(FoodOption, on_delete=models.SET_NULL)
    food_comment = models.CharField(max_length=1000, blank=True)
    hidden = models.BooleanField(default=False)  # "deleted" by reservation user
    created_at = models.DateTimeField(default=datetime.now, editable=False)
    updated_at = models.DateTimeField(default=datetime.now, editable=False)


@receiver(pre_save, sender=Guest)
def guest_pre_save(sender, guest: Reservation):
    """ Updates the updated_at timestamp prior to each save """
    guest.updated_at = datetime.now()


@receiver(post_save, sender=Guest)
def guest_post_save(sender, guest: Guest, created, raw, using, update_fields):
    """ If hiding, delete other hidden Guest objects for the same reservation to ensure that there are at max 10 """
    if update_fields is not None:
        update_fields = frozenset(update_fields)
        if "hidden" in update_fields and guest.hidden:
            reservation = Guest.objects.only("reservation").get(pk=guest.id).reservation
            hidden_guests = Guest.objects.filter(reservation=reservation, hidden=True).order_by("-updated_at")
            if len(hidden_guests) > Guest.MAX_HIDDEN_PER_RESERVATION:
                hidden_guests[Guest.MAX_HIDDEN_PER_RESERVATION:].delete()
