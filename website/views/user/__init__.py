from django.shortcuts import render
from . import sign_in


def profile(request):
    return render(request, "user/profile/index.html", {
        'page_title': 'User Profile'
    })


def register(request):
    return render(request, "user/register/index.html", {
        'page_title': 'Register'
    })
