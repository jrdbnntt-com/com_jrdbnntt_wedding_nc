from django.contrib.auth import logout
from django.shortcuts import render, redirect

from ..decorators.auth import require_auth_or_redirect_with_return


@require_auth_or_redirect_with_return
def profile(request):
    return render(request, "user/profile/index.html", {
        'page_title': 'User Profile'
    })


def sign_out(request):
    request.session.clear()
    if request.user.is_authenticated:
        logout(request)
    return redirect("home")
