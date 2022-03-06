from django.core.mail import EmailMessage
from django.conf import settings
from urllib.parse import urljoin
from website.models.email_template import EmailTemplate


def build_site_link(path: str) -> str:
    return urljoin(settings.EMAIL_LINK_BASE_URL, path)


def send_registration_activated_confirmation(to_email: str, to_name: str, reservation_code: str):
    template = EmailTemplate.objects.filter(name__exact='registration_activated_confirmation').get()
    msg = EmailMessage(
        from_email=template.from_email,
        to=[to_email]
    )
    msg.template_id = template.sendgrid_template_id
    msg.dynamic_template_data = {
        'link_rsvp': build_site_link('rsvp'),
        'to_email': to_email,
        'to_name': to_name,
        'reservation_code': reservation_code
    }
    msg.send(fail_silently=False)

