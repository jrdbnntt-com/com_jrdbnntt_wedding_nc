from functools import wraps
from ....auth import redirect_for_signin_with_return
from django.urls import resolve
from django.shortcuts import redirect


def require_auth_or_redirect_with_return(decorated_view_func=None, keep_get_args_on_redirect=False):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                # Authenticated, just pass on
                return view_func(request, *args, **kwargs)
            # Not authenticated, redirect to sign in and redirect back to the same view after sign in success
            view_name = resolve(request.path_info).view_name
            if keep_get_args_on_redirect:
                return redirect_for_signin_with_return(request, view_name, *args, **request.GET)
            return redirect_for_signin_with_return(request, view_name, *args)
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
