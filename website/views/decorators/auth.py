from functools import wraps

from django.contrib.auth.models import Group
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


def require_user_groups(decorated_view_func=None, groups=None, always_allow_admin=True,
                        not_in_group_view="user/profile", sign_in_view="user/sign_in",
                        keep_get_url_params_on_redirect=False):
    if groups is None or len(groups) == 0:
        raise ValueError('at least one group required')
    for group in groups:
        if not Group.objects.filter(name__exact=group).exists():
            raise ValueError('user group "%s" does not exist' % group)

    def decorator(view_func):
        @require_auth_or_redirect_with_return(sign_in_view=sign_in_view,
                                              keep_get_url_params_on_redirect=keep_get_url_params_on_redirect)
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists() or (always_allow_admin and request.user.is_staff):
                return view_func(request, *args, **kwargs)
            return redirect(not_in_group_view)

        return _wrapped_view

    if decorated_view_func:
        return decorator(decorated_view_func)
    return decorator
