from functools import wraps

from django.shortcuts import redirect

from website.core.session import SESSION_KEY_RESERVATION_ID
from website.models.reservation import Reservation
from website.views.decorators.auth import require_auth_or_redirect_with_return, require_unauthenticated


def require_activated_reservation(decorated_view_func=None):
    def decorator(view_func):
        @require_auth_or_redirect_with_return(sign_in_view="user/sign_in/reservation")
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            res_id = None
            if SESSION_KEY_RESERVATION_ID in request.session:
                # Get reservation from session
                res_id = request.session[SESSION_KEY_RESERVATION_ID]
                if Reservation.objects.filter(id=res_id, user=request.user).count() != 1:
                    # Invalid id, remove from session
                    res_id = None
                    del request.session[SESSION_KEY_RESERVATION_ID]
                    request.session.modified = True
            if res_id is None and request.user.is_authenticated:
                results = Reservation.objects.filter(user=request.user).only("id").all()
                if len(results) == 1:
                    res_id = results[0].id
                    request.session[SESSION_KEY_RESERVATION_ID] = res_id
                    request.session.modified = True
            if res_id is None:
                return redirect("user/profile")
            return view_func(request, reservation_id=res_id, *args, **kwargs)

        return _wrapped_view

    if decorated_view_func:
        return decorator(decorated_view_func)
    return decorator


def require_unactivated_reservation(decorated_view_func=None, redirect_view="user/sign_in/reservation"):
    def decorator(view_func):
        @require_unauthenticated()
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if SESSION_KEY_RESERVATION_ID in request.session:
                # Get reservation from session
                res_id = request.session[SESSION_KEY_RESERVATION_ID]
                if Reservation.objects.filter(id=res_id, activated=False, user__isnull=True).count() == 1:
                    return view_func(request, reservation_id=res_id, *args, **kwargs)
                else:
                    # Invalid id, remove from session
                    del request.session[SESSION_KEY_RESERVATION_ID]
                    request.session.modified = True
            return redirect(redirect_view)

        return _wrapped_view

    if decorated_view_func:
        return decorator(decorated_view_func)
    return decorator
