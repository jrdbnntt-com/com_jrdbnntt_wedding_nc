from django.urls import path, include

from . import views
from .views import reservation
from .views import user
from .views.user import sign_in

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
    path('reservation', include([
        path('', reservation.index),
        path('activate/', reservation.activate)
    ]))
]
