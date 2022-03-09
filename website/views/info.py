from django.http.request import HttpRequest
from django.shortcuts import render

from website.core.auth.user import groups


def event(request: HttpRequest):
    show_rehearsal_dinner_info = False
    if request.user and request.user.is_authenticated and (
            request.user.is_staff or request.user.groups.filter(name=groups.WEDDING_PARTY)):
        show_rehearsal_dinner_info = True
    return render(request, "info/event/index.html", {
        'page_title': 'Event Details',
        'show_rehearsal_dinner_info': show_rehearsal_dinner_info
    })


def photos(request: HttpRequest):
    return render(request, "info/photos/index.html", {
        'page_title': 'Photos'
    })


def story(request: HttpRequest):
    return render(request, "info/story/index.html", {
        'page_title': 'Our Story'
    })


def travel_and_stay(request: HttpRequest):
    return render(request, "info/travel_and_stay/index.html", {
        'page_title': 'Travel'
    })


def wedding_party(request: HttpRequest):
    return render(request, "info/wedding_party/index.html", {
        'page_title': 'Wedding Party'
    })
