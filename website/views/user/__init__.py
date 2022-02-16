from django.shortcuts import render, redirect
from django.contrib.auth import logout
from . import sign_in
from ..decorators.auth import require_auth_or_redirect_with_return, require_unauthenticated


@require_auth_or_redirect_with_return
def profile(request):
    return render(request, "user/profile/index.html", {
        'page_title': 'User Profile'
    })


@require_unauthenticated
def register(request):
    return render(request, "user/register/index.html", {
        'page_title': 'Register'
    })


def sign_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("home")
