from functools import wraps
from django.http import HttpResponse


def user_is_authenticated(user):
    return user.is_authenticated


def authentication_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not user_is_authenticated(request.user):
            return HttpResponse(status=401)
        return view_func(request, *args, **kwargs)
    return wrapper
