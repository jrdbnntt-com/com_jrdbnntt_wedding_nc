from django.conf import settings
from django.urls import reverse


def add_global_vars(request):
    return {
        'base_site_domain': 'https://hannahjaredwedding.com',
        'page_title_prefix': 'Hannah & Jared',
        'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY
    }


def set_navigation_options(request):
    nav_options = [
        NavOption('home', 'Home'),
        NavOption('event', 'Event'),
        NavOption('user/sign_in', 'Sign in', require_auth=False),
        NavOption('user/profile', 'Profile', require_auth=True),
        NavOption('user/sign_out', 'Sign Out', require_auth=True)
    ]
    for option in nav_options:
        if option.view == request.resolver_match.view_name:
            option.active = True
        if request.user.is_authenticated:
            if not option.require_auth and option.require_auth is not None:
                option.show = False
        else:
            if option.require_auth:
                option.show = False

    return {
        'nav_options': [x for x in nav_options if x.show]
    }


class NavOption:
    def __init__(self, view, title, require_auth=None):
        self.view = view
        self.title = title
        self.require_auth = require_auth
        self.active = False
        self.show = True
        self.href = reverse(self.view)
