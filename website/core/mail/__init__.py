import json
import logging
from urllib.parse import urljoin

from django.conf import settings
from django.core.mail import EmailMessage

from website.models.mail.template import EmailTemplate

logger = logging.getLogger(__name__)


def build_site_link(path: str) -> str:
    return urljoin(settings.EMAIL_LINK_BASE_URL, path)


def get_template(name: str) -> EmailTemplate:
    template = EmailTemplate.objects.filter(name__exact=name).get()
    if template.sendgrid_subscription_group is None:
        logger.warning("Email template '%s' does not have subscription group" % template.sendgrid_subscription_group)
    return template


def send_dynamic_template_email(template_name: str, to_email: str, dynamic_template_data: dict):
    template = get_template(template_name)
    msg = EmailMessage(
        from_email=template.from_email,
        to=[to_email]
    )
    msg.template_id = template.sendgrid_template_id
    msg.dynamic_template_data = dynamic_template_data
    if template.sendgrid_subscription_group is not None:
        msg.asm = {
            'group_id': template.sendgrid_subscription_group.sendgrid_id
        }
    try:
        msg.send()
    except Exception as e:
        logger.warning("Failed to send '%s' email to '%s' with data '%s': %s" % (
            template_name,
            to_email,
            json.dumps(dynamic_template_data),
            e
        ))


def send_registration_activated_confirmation(to_email: str, to_name: str, reservation_code: str):
    send_dynamic_template_email('hj_registration_activated_confirmation', to_email, {
        'link_rsvp': build_site_link('rsvp'),
        'to_email': to_email,
        'to_name': to_name,
        'reservation_code': reservation_code
    })
