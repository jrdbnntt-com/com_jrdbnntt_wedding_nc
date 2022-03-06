from django.contrib import admin
from website.models.reservation import Reservation
from website.models.guest import Guest


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("access_code", "name", "user", "activated", "guests_all", "guests_rsvp")

    @admin.display(description="Guests (all)")
    def guests_all(self, obj):
        return ', '.join(map(lambda x: x.__str__(), self.get_simple_guests(obj)))

    @admin.display(description="Guests (RSVP=true)")
    def guests_rsvp(self, obj):
        return ', '.join(map(lambda x: x.__str__(), self.get_simple_guests(obj).filter(rsvp_answer=True)))

    @staticmethod
    def get_simple_guests(obj):
        return Guest.objects.filter(reservation=obj).only("first_name", "last_name")
