from urllib.parse import urljoin

from django.conf import settings

import website.core.mail.sendgrid
from website.core.date import format_month_day_long


def _build_site_link(path: str) -> str:
    return urljoin(settings.EMAIL_LINK_BASE_URL, path)


def send_registration_activated_confirmation(to_email: str, to_name: str, reservation_code: str):
    sendgrid.send_dynamic_template_email('hj_registration_activated_confirmation', to_email, {
        'link_home': settings.EMAIL_LINK_BASE_URL,
        'link_rsvp': _build_site_link('rsvp'),
        'link_rsvp_yes': _build_site_link('reservation/rsvp/quick_answer/yes'),
        'link_rsvp_no': _build_site_link('reservation/rsvp/quick_answer/no'),
        'link_faqs': _build_site_link('info/faqs'),
        'to_email': to_email,
        'to_name': to_name,
        'reservation_code': reservation_code
    })


def send_rsvp_updated_email(to_email: str, to_name: str, rsvp_complete: bool, attending_wedding: bool,
                            attending_rehearsal: bool, invited_to_rehearsal: bool, guest_rsvp_statuses: list[str]):
    sendgrid.send_dynamic_template_email('hj_rsvp_answer_updated', to_email, {
        'link_home': settings.EMAIL_LINK_BASE_URL,
        'to_name': to_name,
        'link_rsvp': _build_site_link('/reservation/rsvp'),
        'rsvp_complete': rsvp_complete,
        'attending_wedding': attending_wedding,
        'attending_rehearsal': attending_rehearsal,
        'guest_rsvp_statuses': guest_rsvp_statuses,
        'invited_to_rehearsal': invited_to_rehearsal,
        'date_rsvp_deadline': format_month_day_long(settings.DATE_RSVP_DEADLINE)
    })


def send_rsvp_june_reminder_email(to_email: str, to_name: str, attending_rehearsal_dinner: bool,
                                  attending_rehearsal: bool, attending_wedding: bool, guest_rsvp_statuses: list[str]):
    sendgrid.send_dynamic_template_email('hj_rsvp_june_reminder', to_email, {
        'link_home': settings.EMAIL_LINK_BASE_URL,
        'to_name': to_name,
        'link_faqs': _build_site_link('/info/faqs'),
        'guest_rsvp_statuses': guest_rsvp_statuses,
        'attending_wedding': attending_wedding,
        'attending_rehearsal': attending_rehearsal,
        'attending_rehearsal_dinner': attending_rehearsal_dinner,
    })
