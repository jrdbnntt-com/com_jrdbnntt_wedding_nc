from django.http.request import HttpRequest
from django.shortcuts import render


def venue(request: HttpRequest):
    return render(request, "info/venue/index.html", {
        'page_title': 'Venue',
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
        'page_title': 'Travel',
        'bonus_text_chars': "BONUS LEO & ADA".strip('')
    })


def wedding_party(request: HttpRequest):
    return render(request, "info/wedding_party/index.html", {
        'page_title': 'Wedding Party'
    })


def faqs(request: HttpRequest):
    return render(request, "info/faqs/index.html", {
        'page_title': 'FAQs'
    })
