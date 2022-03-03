from django.shortcuts import render, redirect

from .decorators.auth import require_auth_or_redirect_with_return


def home(request):
    return render(request, "home/index.html", {
        'page_title': 'Home'
    })


def event(request):
    return render(request, "event/index.html", {
        'page_title': 'Event'
    })


def rsvp():
    return redirect("user/sign_in/reservation")
