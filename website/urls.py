from django.conf import settings
from django.urls import path, include

from website import views
from website.views import reservation
from website.views import user
from website.views.user import sign_in
from website.views.reservation import rsvp

urlpatterns = [
    path('', views.home, name='home'),
    path('event/', views.event, name='event'),
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
    ]))
]

if settings.ADMIN_SITE_ENABLED:
    urlpatterns.append(path('admin/login/', views.admin_login_redirect))
