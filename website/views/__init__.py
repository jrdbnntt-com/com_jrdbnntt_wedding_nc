from django.shortcuts import render
from . import user


def home(request):
    return render(request, "home/index.html", {
        'page_title': 'Home'
    })


def event(request):
    return render(request, "event/index.html", {
        'page_title': 'Event'
    })


