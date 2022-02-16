from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('event/', views.event, name='event'),
    path('user/', include([
        path('sign_in/', include([
            path('', views.user.sign_in.index, name='user/sign_in'),
            path('reservation/', views.user.sign_in.reservation, name='user/sign_in/reservation'),
            path('user/', views.user.sign_in.user, name='user/sign_in/user'),
        ])),
        path('sign_out', views.user.sign_out, name="user/sign_out"),
        path('register/', views.user.register, name='user/register'),
        path('profile/', views.user.profile, name='user/profile'),
    ]))
]
