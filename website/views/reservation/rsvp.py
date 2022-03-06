from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect, render

from website.views.decorators.reservation import require_activated_reservation
from website.models.guest import Guest


@require_activated_reservation
def index(request: HttpRequest, reservation_id: int):
    # TODO make a page for editing RSVP
    return render(request, "reservation/rsvp/index.html", {
        'page_title': 'Manage RSVP',
    })


@require_activated_reservation
def quick_answer(request: HttpRequest, reservation_id: int, answer: str):
    if answer == 'yes':
        rsvp_answer = True
    elif answer == 'no':
        rsvp_answer = False
    else:
        return HttpResponseBadRequest()
    for guest in Guest.objects.filter(reservation_id=reservation_id).all():
        guest.rsvp_answer = rsvp_answer
        guest.save()
    return redirect('reservation')

