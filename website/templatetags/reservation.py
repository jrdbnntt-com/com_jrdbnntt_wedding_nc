from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from website.models.guest import Guest
from website.models.reservation import Reservation

register = template.Library()


@register.simple_tag
def guest_full_name(guest: Guest) -> str:
    return guest.full_name()


@register.simple_tag
def guest_rsvp_summary(guest: Guest) -> str:
    summary = guest.rsvp_answer_display()
    if guest.rsvp_comment is not None:
        summary += '; ' + guest.rsvp_comment
    return summary


@register.simple_tag
def guest_rsvp_status_sentence(reservation: Reservation, guest: Guest) -> str:
    result = escape(guest.first_name)
    if guest.rsvp_answer is None:
        result += " has <b>not yet RSVP'd</b> to the wedding ceremony"
    else:
        result += " is <b>" + guest.rsvp_answer_display().lower() + "</b> to the wedding ceremony"
    if reservation.invited_to_rehearsal:
        if guest.rehearsal_rsvp_answer is None:
            result += " and has <b>not yet RSVP'd</b> to the rehearsal dinner"
        else:
            result += " and is <b>" + guest.rehearsal_rsvp_answer_display().lower() + "</b> to the rehearsal dinner"
    result += '.'
    return mark_safe(result)
