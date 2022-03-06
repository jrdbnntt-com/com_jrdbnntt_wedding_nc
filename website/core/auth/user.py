from urllib.parse import urlencode

from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from website.core.session import SESSION_KEY_POST_SIGN_IN_REDIRECT


def redirect_for_signin_with_return(request, post_sign_in_redirect_view, *url_path_args, **url_params):
    # Save return url to session for secure retrieval later
    post_sign_in_redirect_url = reverse(post_sign_in_redirect_view, args=url_path_args)
    url_params = urlencode(url_params)
    if len(url_params) > 0:
        post_sign_in_redirect_url += "?" + url_params
    if post_sign_in_redirect_view is not None:
        request.session[SESSION_KEY_POST_SIGN_IN_REDIRECT] = post_sign_in_redirect_url
        request.session.modified = True

    # Redirect to the sign in index page with ?redirect=true
    return HttpResponseRedirect(reverse("user/sign_in") + "?redirect=true")
