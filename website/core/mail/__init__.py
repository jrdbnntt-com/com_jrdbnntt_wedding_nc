from urllib.parse import urljoin

from django.conf import settings

import website.core.mail.sendgrid
from website.core.date import format_month_day_long


def _build_site_link(path: str) -> str:
    return urljoin(settings.EMAIL_LINK_BASE_URL, path)


def send_registration_activated_confirmation(to_email: str, to_name: str, reservation_code: str):
    sendgrid.send_dynamic_template_email('nc_registration_activated_confirmation', to_email, {
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
                            guest_rsvp_statuses: list[str]):
    sendgrid.send_dynamic_template_email('nc_rsvp_answer_updated', to_email, {
        'link_home': settings.EMAIL_LINK_BASE_URL,
        'to_name': to_name,
        'link_rsvp': _build_site_link('/reservation/rsvp'),
        'rsvp_complete': rsvp_complete,
        'attending_wedding': attending_wedding,
        'guest_rsvp_statuses': guest_rsvp_statuses,
        'date_rsvp_deadline': format_month_day_long(settings.DATE_RSVP_DEADLINE)
    })


def send_rsvp_june_reminder_email(to_email: str, to_name: str, guest_rsvp_statuses: list[str]):
    sendgrid.send_dynamic_template_email('nc_rsvp_june_reminder', to_email, {
        'link_home': settings.EMAIL_LINK_BASE_URL,
        'to_name': to_name,
        'link_faqs': _build_site_link('/info/faqs'),
        'guest_rsvp_statuses': guest_rsvp_statuses,
    })
