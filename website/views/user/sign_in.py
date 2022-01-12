from django.shortcuts import render
from django.http import HttpResponseRedirect
from ...forms.user.sign_in import UsernamePasswordForm

sign_in_success_view = 'user/profile'


def index(request):
    return render(request, "user/sign_in/index.html", {
        'page_title': 'Sign in'
    })


def reservation(request):
    return render(request, "user/sign_in/reservation/index.html", {
        'page_title': 'Sign in - Reservation'
    })


def user(request):
    if request.method == 'POST':
        form = UsernamePasswordForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(sign_in_success_view)
    else:
        form = UsernamePasswordForm()

    return render(request, "user/sign_in/user/index.html", {
        'page_title': 'Sign in - User',
        'form': form
    })
