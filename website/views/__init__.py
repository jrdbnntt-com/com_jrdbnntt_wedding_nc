from django.http.request import HttpRequest
from django.shortcuts import render, redirect

from website.core.auth.user import redirect_for_signin_with_return
from website.views.decorators.auth import require_auth_or_redirect_with_return, require_unauthenticated


def home(request: HttpRequest):
    return render(request, "home/index.html", {
        'page_title': 'Home'
    })


def event(request: HttpRequest):
    return render(request, "info/event/index.html", {
        'page_title': 'Event'
    })


def rsvp(request: HttpRequest):
    return redirect("reservation/rsvp")


@require_unauthenticated
def admin_login_redirect(request, *args, **kwargs):
    return redirect_for_signin_with_return(request, post_sign_in_redirect_view="admin:index",
                                           sign_in_view="user/sign_in/user")
