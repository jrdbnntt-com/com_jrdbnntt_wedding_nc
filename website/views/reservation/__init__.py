from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http.request import HttpRequest
from django.shortcuts import render, redirect

from website.views.decorators.reservation import require_activated_reservation, require_unactivated_reservation
from ...auth import recaptcha
from ...forms.reservation import ActivateForm
from ...models import reservation
from ...models.guest import Guest


@require_activated_reservation
def index(request: HttpRequest, reservation_id: int):
    # TODO make a page that summarizes the reservation
    guests = Guest.objects.filter(reservation__id=reservation_id, hidden=False).all()
    return render(request, "reservation/index.html", {
        'page_title': 'Reservation',
        'guests': guests
    })


@require_unactivated_reservation
def activate(request: HttpRequest, reservation_id: int):
    recaptcha_action = recaptcha.RECAPTCHA_ACTION_RESERVATION_ACTIVATE
    if request.method == "POST":
        form = ActivateForm(request.POST)
        if form.is_valid():
            try:
                recaptcha.validate_recaptcha_token(request, form.cleaned_data['recaptcha_token'], recaptcha_action)
            except ValidationError as e:
                form.add_error(None, e.message)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Ensure email not tied to an existing user
            if User.objects.filter(email=email).count() != 0 or User.objects.filter(username=email).count() != 0:
                form.add_error('email', 'Email already in use, please use another one')
            else:
                new_user = reservation.activate_reservation(reservation_id, email)
                login(request, new_user)
                return redirect('reservation')
        form.clear_sensitive_form_data()
    else:
        form = ActivateForm()

    return render(request, "reservation/activate/index.html", {
        'page_title': 'Activate Reservation',
        'form': form,
        'recaptcha_action': recaptcha_action
    })
