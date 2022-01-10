from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('event/', views.event, name='event'),
    path('user/', include([
        path('sign_in/', views.user_sign_in, name='user/sign_in'),
        path('register/', views.user_register, name='user/register'),
        path('profile/', views.user_profile, name='user/profile'),
    ]))
]
