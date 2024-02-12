from django.contrib import admin

from website.models.guest import Guest
from website.models.reservation import Reservation


def init():
    """ Does nothing, just here to keep import """
    pass


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    ordering = ("name",)
    list_display = (
        "id",
        "access_code",
        "name",
        "user",
        "activated",
        "guests_all",
        "guests_rsvp",
    )
    list_filter = ('activated',)

    @admin.display(description="All Guests (RSVP)")
    def guests_all(self, obj: Reservation) -> str:
        return ', '.join(map(lambda x: x.full_name_rsvp(), self.get_simple_guests(obj)))

    @admin.display(description="Guests (RSVP=Going)")
    def guests_rsvp(self, obj: Reservation) -> str:
        return ', '.join(map(lambda x: x.__str__(), self.get_simple_guests(obj).filter(rsvp_answer=True)))

    @staticmethod
    def get_simple_guests(obj):
        return Guest.objects.filter(reservation=obj).only("first_name", "last_name").order_by('first_name')


def reservation_has_guests_attending_wedding_event(res: Reservation) -> bool:
    for guest in Guest.objects.filter(reservation=res):
        if guest.rsvp_answer is True:
            return True
    return False
