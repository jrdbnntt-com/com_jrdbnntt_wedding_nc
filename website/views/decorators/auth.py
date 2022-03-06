from functools import wraps

from django.shortcuts import redirect
from django.urls import resolve

from website.core.auth.user import redirect_for_signin_with_return


def require_auth_or_redirect_with_return(decorated_view_func=None, sign_in_view="user/sign_in",
                                         keep_get_url_params_on_redirect=False):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                # Authenticated, just pass on
                return view_func(request, *args, **kwargs)
            # Not authenticated, redirect to sign in and redirect back to the same view after sign in success
            view_name = resolve(request.path_info).view_name
            if keep_get_url_params_on_redirect:
                return redirect_for_signin_with_return(request, view_name, sign_in_view=sign_in_view,
                                                       request_kwargs=kwargs,
                                                       **request.GET)
            return redirect_for_signin_with_return(request, view_name, sign_in_view=sign_in_view, request_kwargs=kwargs,
                                                   request_args=args)

        return _wrapped_view

    if decorated_view_func:
        return decorator(decorated_view_func)
    return decorator


def require_unauthenticated(decorated_view_func=None, redirect_view='user/profile'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # Not authenticated, just pass on
                return view_func(request, *args, **kwargs)
            # Authenticated, just redirect to home page
            return redirect(redirect_view)

        return _wrapped_view

    if decorated_view_func:
        return decorator(decorated_view_func)
    return decorator
