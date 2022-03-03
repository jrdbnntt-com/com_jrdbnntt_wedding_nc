from django import template

from ..models.guest import Guest

register = template.Library()


@register.simple_tag
def guest_full_name(guest: Guest):
    return guest.full_name()


@register.simple_tag
def guest_rsvp_summary(guest: Guest):
    summary = guest.rsvp_answer_display()
    if guest.rsvp_comment is not None:
        summary += '; ' + guest.rsvp_comment
    return summary
