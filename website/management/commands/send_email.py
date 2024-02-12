import typing

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
        elif email_name == 'covid_update':
            self.email_covid_update(reservation_ids)
        elif email_name == 'print_emails_attending_wedding':
            self.print_emails_attending_wedding(reservation_ids)
        elif email_name == 'print_emails_attending_only_wedding':
            self.print_emails_attending_only_wedding(reservation_ids)
        elif email_name == 'print_emails_attending_rehearsal':
            self.print_emails_attending_rehearsal(reservation_ids)
        elif email_name == 'print_emails_not_attending':
            self.print_not_attending_emails(reservation_ids)
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
            if reservation_has_guests_attending_wedding_event(res) and res.user is not None:
                reservations_with_attendees.append(res)
        self.stdout.write("Found %d Reservation objects with attendees" % len(reservations_with_attendees))
        return reservations_with_attendees

    def collect_reservations_with_no_attendees(self, reservation_ids: list[str] = None) -> list[Reservation]:
        self.stdout.write("Collecting Reservation objects...")
        if reservation_ids is not None and len(reservation_ids) > 0:
            reservations = Reservation.objects.filter(id__in=reservation_ids).order_by('id')
        else:
            reservations = Reservation.objects.all().order_by('id')
        reservations_with_no_attendees = []
        for res in reservations:
            if not reservation_has_guests_attending_wedding_event(res) and res.user is not None:
                reservations_with_no_attendees.append(res)
        self.stdout.write("Found %d Reservation objects with no attendees" % len(reservations_with_no_attendees))
        return reservations_with_no_attendees


    @staticmethod
    def confirm_send(email_name: str, reservation_count: int):
        answer = input("Send '%s' email to %d Reservations (y/N)?" % (email_name, reservation_count))
        if answer != "y":
            raise CommandError("Aborted")

    def email_rsvp_june_reminder(self, reservation_ids: list[str] = None):
        email_name = 'rsvp_june_reminder'
        reservations_with_attendees = self.collect_reservations_with_attendees(reservation_ids)

        def send(res: Reservation):
            guests = Guest.objects.filter(reservation__id=res.id).order_by('created_at').all()
            attending_wedding = False
            for guest in guests:
                if guest.rsvp_answer is True:
                    attending_wedding = True
            guest_rsvp_statuses = []
            for guest in guests:
                guest_rsvp_statuses.append(
                    "<b>%s</b> is <b>%s</b> to the wedding." % (
                        guest.first_name,
                        guest.rsvp_answer_display().lower()
                    )
                )
            if not attending_wedding:
                self.stdout.write(
                    "Skipping '%s' email for %s, not attending the wedding" % (email_name, res))
            elif res.user is None:
                self.stdout.write("Skipping '%s' email for %s, no user" % (email_name, res))
            else:
                mail.send_rsvp_june_reminder_email(
                    to_email=res.user.email,
                    to_name=res.name,
                    guest_rsvp_statuses=guest_rsvp_statuses
                )

        self.send_email_to_reservations(email_name, reservations_with_attendees, send)

    def send_email_to_reservations(self, email_name: str, reservations: list[Reservation], send: typing.Callable[[Reservation], None]):
        self.confirm_send(email_name, len(reservations))
        self.stdout.write("Sending %s emails..." % email_name)
        for i in range(len(reservations)):
            res = reservations[i]
            try:
                self.stdout.write("Sending '%s' email to %s..." % (email_name, res))
                send(res)
            except Exception as e:
                raise CommandError("Failed to send '%s' email to %s. Remaining ids: %s" % (
                    email_name,
                    res,
                    " ".join(self.collect_ids(reservations[i:]))
                )) from e
            self.stdout.write("Sent '%s' email to %s." % (email_name, res))
        self.stdout.write("Successfully sent '%s' to reservations with ids: %s" % (
            email_name,
            " ".join(self.collect_ids(reservations))
        ))

    def print_emails_attending_wedding(self, reservation_ids=None):
        reservations_with_attendees = self.collect_reservations_with_attendees(reservation_ids)
        for res in reservations_with_attendees:
            self.stdout.write(res.user.email)

    def print_not_attending_emails(self, reservation_ids=None):
        reservations_with_no_attendees = self.collect_reservations_with_no_attendees(reservation_ids)
        for res in reservations_with_no_attendees:
            self.stdout.write(res.user.email)

    @staticmethod
    def collect_ids(objs: list[Reservation]) -> list[str]:
        return [("%d" % obj.id) for obj in objs]
