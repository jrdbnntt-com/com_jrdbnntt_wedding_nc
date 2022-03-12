from django.conf import settings
from django.urls import reverse

from website.core.date import format_month_day_year_long


def add_global_vars(request):
    return {
        'base_site_domain': 'https://hannahjaredwedding.com',
        'page_title_prefix': 'Hannah & Jared',
        'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
        'event_location': settings.EVENT_PUBLIC_LOCATION,
        'event_date': format_month_day_year_long(settings.EVENT_DATE),
        'js_window_params': [
            ('EVENT_DATE_ISO', '"%s"' % settings.EVENT_DATE.isoformat())
        ]
    }


def set_navigation_options(request):
    nav_options = [
        NavOption('home', 'Home'),
        NavOption('info/story', 'Our Story'),
        NavOption('info/travel_and_stay', 'Travel & Stay'),
        # NavOption('info/photos', 'Photos'),
        # NavOption('info/wedding_party', 'Wedding Party'),
        NavOption('info/venue', 'Venue'),
        NavOption('reservation/rsvp', 'RSVP'),
        NavOption('user/sign_in', 'Sign in', require_auth=False),
        # NavOption('user/profile', 'Profile', require_auth=True),
    ]
    if settings.ADMIN_SITE_ENABLED:
        nav_options.append(NavOption('admin:index', 'Admin', require_admin=True))
    nav_options.append(NavOption('user/sign_out', 'Sign Out', require_auth=True))
    for option in nav_options:
        if option.view == request.resolver_match.view_name:
            option.active = True
        if request.user.is_authenticated:
            if not option.require_auth and option.require_auth is not None:
                option.show = False
            if option.require_admin and not request.user.is_superuser:
                option.show = False
        else:
            if option.require_auth:
                option.show = False

    return {
        'nav_options': [x for x in nav_options if x.show]
    }


class NavOption:
    def __init__(self, view, title, require_auth=None, require_admin=False):
        self.view = view
        self.title = title
        self.require_auth = require_auth
        self.active = False
        self.show = True
        self.href = reverse(self.view)
        self.require_admin = require_admin
        if self.require_admin:
            self.require_auth = True
