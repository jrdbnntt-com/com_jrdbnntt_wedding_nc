from urllib.parse import urljoin

from django.conf import settings

import website.core.mail.sendgrid


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
