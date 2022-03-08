from django.http.request import HttpRequest
from django.shortcuts import render


def index(request: HttpRequest):
    return render(request, "info/registry/index.html", {
        'page_title': 'Registry'
    })
