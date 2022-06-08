from django.core.management.base import BaseCommand, CommandError

from website.core import mail
from website.models.guest import Guest
from website.models.reservation import Reservation
from website.models.reservation.admin import reservation_has_guests_attending_wedding_event


class Command(BaseCommand):
    help = "Usage: 'send_email <email_name> [...<reservation_id>]'"

    def add_arguments(self, parser):
        parser.add_argument('email_name', nargs=1, type=str)
        parser.add_argument('--ids', nargs='+', type=int, default=[])

    def handle(self, *args, **options):
        email_name = options['email_name'][0]
        reservation_ids = options['ids']
        if email_name == 'rsvp_june_reminder':
            self.email_rsvp_june_reminder(reservation_ids)
        else:
            raise CommandError("Invalid email_name '%s'" % email_name)

    def collect_reservations_with_attendees(self, reservation_ids: list[str] = None) -> list[Reservation]:
        self.stdout.write("Collecting Reservation objects...")
        if reservation_ids is not None and len(reservation_ids) > 0:
            reservations = Reservation.objects.filter(id__in=reservation_ids).order_by('id')
        else:
            reservations = Reservation.objects.all().order_by('id')
        reservations_with_attendees = []
        for res in reservations:
            if reservation_has_guests_attending_wedding_event(res):
                reservations_with_attendees.append(res)
        self.stdout.write("Found %d Reservation objects with attendees" % len(reservations_with_attendees))
        return reservations_with_attendees

    @staticmethod
    def confirm_send(email_name: str, reservation_count: int):
        answer = input("Send '%s' email to %d Reservations (y/N)?" % (email_name, reservation_count))
        if answer != "y":
            raise CommandError("Aborted")

    def email_rsvp_june_reminder(self, reservation_ids: list[str] = None):
        email_name = 'rsvp_june_reminder'
        reservations_with_attendees = self.collect_reservations_with_attendees(reservation_ids)
        self.confirm_send(email_name, len(reservations_with_attendees))
        self.stdout.write("Sending %s emails..." % email_name)
        for i in range(len(reservations_with_attendees)):
            res = reservations_with_attendees[i]
            try:
                self.stdout.write("Preparing '%s' email for %s..." % (email_name, res))
                guests = Guest.objects.filter(reservation__id=res.id).order_by('created_at').all()
                attending_rehearsal = False
                attending_rehearsal_dinner = False
                attending_wedding = False
                for guest in guests:
                    if guest.rsvp_answer is True:
                        attending_wedding = True
                    if guest.rehearsal_rsvp_answer is True:
                        attending_rehearsal_dinner = True
                    if guest.attending_ceremony_rehearsal is True:
                        attending_rehearsal = True
                guest_rsvp_statuses = []
                for guest in guests:
                    if guest.attending_ceremony_rehearsal:
                        guest_rsvp_statuses.append(
                            "<b>%s</b> is <b>going</b> to the ceremony rehearsal, is <b>%s</b> to the rehearsal dinner, and is <b>%s</b> to the wedding." % (
                                guest.first_name,
                                guest.rehearsal_rsvp_answer_display().lower(),
                                guest.rsvp_answer_display().lower()
                            )
                        )
                    elif attending_rehearsal_dinner:
                        guest_rsvp_statuses.append(
                            "<b>%s</b> is <b>%s</b> to the rehearsal dinner and is <b>%s</b> to the wedding." % (
                                guest.first_name,
                                guest.rehearsal_rsvp_answer_display().lower(),
                                guest.rsvp_answer_display().lower()
                            )
                        )
                    else:
                        guest_rsvp_statuses.append(
                            "<b>%s</b> is <b>%s</b> to the wedding." % (
                                guest.first_name,
                                guest.rsvp_answer_display().lower()
                            )
                        )

                if not attending_rehearsal and not attending_rehearsal_dinner and not attending_wedding:
                    self.stdout.write(
                        "Skipping '%s' email for %s, not attending anything" % (email_name, res))
                elif res.user is None:
                    self.stdout.write("Skipping '%s' email for %s, no user" % (email_name, res))
                else:
                    self.stdout.write("Sending '%s' email for %s..." % (email_name, res))
                    mail.send_rsvp_june_reminder_email(
                        to_email=res.user.email,
                        to_name=res.name,
                        attending_rehearsal=attending_rehearsal,
                        attending_rehearsal_dinner=attending_rehearsal_dinner,
                        attending_wedding=attending_wedding,
                        guest_rsvp_statuses=guest_rsvp_statuses
                    )
            except Exception as e:
                raise CommandError("Failed to send '%s' email to %s. Remaining ids: %s" % (
                    email_name,
                    res,
                    " ".join(self.collect_ids(reservations_with_attendees[i:]))
                )) from e
            self.stdout.write("Sent '%s' email to %s" % (email_name, res))
        self.stdout.write("Successfully sent '%s' to reservations with ids: %s" % (
            email_name,
            " ".join(self.collect_ids(reservations_with_attendees))
        ))

    def email_covid_update(self, reservation_ids: list[str] = None):
        email_name = 'covid_update'
        reservations_with_attendees = self.collect_reservations_with_attendees(reservation_ids)
        self.confirm_send(email_name, len(reservations_with_attendees))
        self.stdout.write("Sending %s emails..." % email_name)
        for i in range(len(reservations_with_attendees)):
            res = reservations_with_attendees[i]
            try:
                self.stdout.write("Sending '%s' email for reservation with id %d..." % (email_name, res.id))
                mail.send_covid_update_email(
                    to_email=res.user.email,
                    to_name=res.name
                )
            except Exception as e:
                raise CommandError("Failed to send '%s' email to reservation with id %d. Remaining ids: %s" % (
                    email_name,
                    res.id,
                    " ".join(self.collect_ids(reservations_with_attendees[i:]))
                )) from e
            self.stdout.write("Sent '%s' email for reservation with id %d." % (email_name, res.id))
        self.stdout.write("Successfully sent '%s' to reservations with ids: %s" % (
            email_name,
            " ".join(self.collect_ids(reservations_with_attendees))
        ))

    @staticmethod
    def collect_ids(objs: list[Reservation]) -> list[str]:
        return [("%d" % obj.id) for obj in objs]
