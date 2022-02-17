from django.shortcuts import render, redirect
from ...forms.user.sign_in import UsernamePasswordForm
from django.contrib.auth import authenticate, login
from ...session import SESSION_KEY_POST_SIGN_IN_REDIRECT
from ..decorators.auth import require_unauthenticated
from ...auth import recaptcha
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

@require_unauthenticated
def index(request):
    redirect_on_success = 'redirect' in request.GET and \
                          request.GET['redirect'] == "true" and \
                          SESSION_KEY_POST_SIGN_IN_REDIRECT in request.session
    return render(request, "user/sign_in/index.html", {
        'page_title': 'Sign in',
        'redirect': redirect_on_success
    })


@require_unauthenticated
def reservation(request):
    return render(request, "user/sign_in/reservation/index.html", {
        'page_title': 'Sign in - Reservation'
    })


@require_unauthenticated
def user(request):
    recaptcha_action = recaptcha.RECAPTCHA_ACTION_SIGN_IN_USER
    redirect_on_success = 'redirect' in request.GET and \
                          request.GET['redirect'] == "true" and \
                          SESSION_KEY_POST_SIGN_IN_REDIRECT in request.session
    if not redirect_on_success and SESSION_KEY_POST_SIGN_IN_REDIRECT in request.session:
        del request.session[SESSION_KEY_POST_SIGN_IN_REDIRECT]
        request.session.modified = True
    if request.method == 'POST':
        form = UsernamePasswordForm(request.POST)
        validation_error = None
        if form.is_valid():
            try:
                recaptcha.validate_recaptcha_token(request, form.cleaned_data['recaptcha_token'], recaptcha_action)
                target_user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if target_user is not None:
                    login(request, target_user)
                    return redirect(determine_sign_in_success_view(request))
                else:
                    raise ValidationError("Invalid username or password")
            except ValidationError as e:
                validation_error = e

        form.clear_sensitive_form_data()
        if validation_error is not None:
            form.add_error(None, validation_error.message)
    else:
        form = UsernamePasswordForm()

    return render(request, "user/sign_in/user/index.html", {
        'page_title': 'Sign in - User',
        'form': form,
        'redirect': redirect_on_success,
        'recaptcha_action': recaptcha_action
    })


def determine_sign_in_success_view(request):
    target_view = 'user/profile'
    if SESSION_KEY_POST_SIGN_IN_REDIRECT in request.session:
        target_view = request.session[SESSION_KEY_POST_SIGN_IN_REDIRECT]
        del request.session[SESSION_KEY_POST_SIGN_IN_REDIRECT]
        request.session.modified = True
    return target_view

