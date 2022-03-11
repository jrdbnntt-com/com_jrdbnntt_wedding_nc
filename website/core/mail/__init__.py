from urllib.parse import urljoin

from django.conf import settings

import website.core.mail.sendgrid
from website.core.date import format_month_day_year_long


def _build_site_link(path: str) -> str:
    return urljoin(settings.EMAIL_LINK_BASE_URL, path)


def send_registration_activated_confirmation(to_email: str, to_name: str, reservation_code: str):
    sendgrid.send_dynamic_template_email('hj_registration_activated_confirmation', to_email, {
        'link_rsvp': _build_site_link('rsvp'),
        'link_rsvp_yes': _build_site_link('reservation/rsvp/quick_answer/yes'),
        'link_rsvp_no': _build_site_link('reservation/rsvp/quick_answer/no'),
        'to_email': to_email,
        'to_name': to_name,
        'reservation_code': reservation_code
    })


def send_rsvp_updated_email(to_email: str, to_name: str, rsvp_complete: bool, attending_wedding: bool,
                            attending_rehearsal: bool, invited_to_rehearsal: bool, guest_rsvp_statuses: list[str]):
    sendgrid.send_dynamic_template_email('hj_rsvp_answer_updated', to_email, {
        'to_name': to_name,
        'rsvp_complete': rsvp_complete,
        'attending_wedding': attending_wedding,
        'attending_rehearsal': attending_rehearsal,
        'guest_rsvp_statuses': guest_rsvp_statuses,
        'invited_to_rehearsal': invited_to_rehearsal,
        'date_rsvp_deadline': format_month_day_year_long(settings.DATE_RSVP_DEADLINE)
    })
