import secrets
import string

from django.contrib.auth.models import User, Group
from django.db import models
from django.utils import timezone

from website.core.auth.user import groups


def generate_access_code():
    return ''.join(secrets.choice(Reservation.ACCESS_CODE_CHARS) for _ in range(Reservation.ACCESS_CODE_LENGTH))


class Reservation(models.Model):
    """ A guest reservation for one or more Guests. Used for accounts. """
    ACCESS_CODE_LENGTH = 6
    ACCESS_CODE_CHARS = string.ascii_uppercase + "23456789"
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    access_code = models.CharField(max_length=ACCESS_CODE_LENGTH, default=generate_access_code, unique=True)
    activated = models.BooleanField(default=False)  # Set to True once the reservation has been accessed once
    activated_at = models.DateTimeField(null=True, blank=True)
    max_guests = models.IntegerField(default=2)
    rsvp_updated_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        if self.user is not None:
            return "Reservation(id={},name='{}',user.username='{}')".format(self.id, self.name, self.user.username)
        else:
            return "Reservation(id={},name='{}',inactive)".format(self.id, self.name)


def activate_reservation(reservation_id: int, email: str):
    res = Reservation.objects.filter(id=reservation_id).only("id", "access_code", "name").get()
    usr = User.objects.create_user(email, email, res.access_code)
    res.user = usr
    res.activated = True
    res.activated_at = timezone.now()
    res.save()

    wedding_guests_group = Group.objects.filter(name=groups.WEDDING_GUESTS).get()
    wedding_guests_group.user_set.add(usr)
    wedding_guests_group.save()

    return res, usr
