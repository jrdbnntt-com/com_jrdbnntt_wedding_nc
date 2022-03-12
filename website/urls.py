from django.conf import settings
from django.urls import path, include

from website import views
from website.models.aggregate import init as init_model_aggregates
from website.views import reservation, user, registry, info
from website.views.reservation import rsvp
from website.views.user import sign_in

urlpatterns = [
    path('', views.home, name='home'),
    path('rsvp/', views.rsvp, name='rsvp'),
    path('user/', include([
        path('sign_in/', include([
            path('', sign_in.index, name='user/sign_in'),
            path('reservation/', sign_in.reservation, name='user/sign_in/reservation'),
            path('user/', sign_in.user, name='user/sign_in/user'),
        ])),
        path('sign_out', user.sign_out, name="user/sign_out"),
        path('profile/', user.profile, name='user/profile'),
    ])),
    path('reservation/', include([
        path('', reservation.index, name='reservation'),
        path('activate/', reservation.activate, name='reservation/activate'),
        path('rsvp/', include([
            path('', rsvp.index, name="reservation/rsvp"),
            path('quick_answer/<str:answer>/', rsvp.quick_answer, name="reservation/rsvp/quick_answer")
        ]))
    ])),
    path('registry/', include([
        path('', registry.index, name="registry")
    ])),
    path('info/', include([
        path('venue/', info.venue, name='info/venue'),
        # path('photos/', info.photos, name='info/photos'),
        path('story/', info.story, name='info/story'),
        path('travel_and_stay/', info.travel_and_stay, name='info/travel_and_stay'),
        # path('wedding_party/', info.wedding_party, name='info/wedding_party')
    ]))
]

if settings.ADMIN_SITE_ENABLED:
    urlpatterns.append(path('admin/login/', views.admin_login_redirect))

init_model_aggregates()
