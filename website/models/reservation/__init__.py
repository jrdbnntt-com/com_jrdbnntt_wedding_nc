from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime
import secrets
import string


def generate_access_code():
    return ''.join(secrets.choice(Reservation.ACCESS_CODE_CHARS) for _ in range(Reservation.ACCESS_CODE_LENGTH))


class Reservation(models.Model):
    """ A guest reservation for one or more Guests. Used for accounts. """
    ACCESS_CODE_LENGTH = 6
    ACCESS_CODE_CHARS = string.ascii_uppercase + "23456789"
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    access_code = models.CharField(max_length=ACCESS_CODE_LENGTH, default=generate_access_code)
    activated = models.BooleanField(default=False)  # Set to True once the reservation has been accessed once
    activated_at = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(blank=True)  # Used as User.username and User.email upon activation and user creation
    max_guests = models.IntegerField(default=2)
    rsvp_updated_at = models.DateTimeField(null=True, blank=True)
    mailing_address_line_1 = models.CharField(max_length=200, blank=True)
    mailing_address_line_2 = models.CharField(max_length=200, blank=True)
    mailing_address_city = models.CharField(max_length=200, blank=True)
    mailing_address_state = models.CharField(max_length=2, blank=True)
    mailing_address_zip = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(default=datetime.now, editable=False)
    updated_at = models.DateTimeField(default=datetime.now, editable=False)

    def __str__(self):
        if self.user is not None:
            return "Reservation (id={}, user.username='{}')".format(self.id, self.user.username)
        else:
            return super.__str__(self)


@receiver(pre_save, sender=Reservation)
def pre_save(sender, instance: Reservation, **kwargs):
    """ Updates the updated_at timestamp prior to each save """
    instance.updated_at = datetime.now()
