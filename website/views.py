from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, "home/index.html", {
        'page_title': 'Home'
    })


def event(request):
    return render(request, "event/index.html", {
        'page_title': 'Event'
    })


def user_profile(request):
    return render(request, "user/profile/index.html", {
        'page_title': 'User Profile'
    })


def user_register(request):
    return render(request, "user/register/index.html", {
        'page_title': 'Register'
    })


def user_sign_in(request):
    return render(request, "user/sign_in/index.html", {
        'page_title': 'Sign in'
    })

