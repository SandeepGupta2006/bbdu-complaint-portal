from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def student_required(view_func):

    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):

        if not hasattr(request.user, "studentprofile"):
            return redirect("dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper


def staff_required(view_func):

    @wraps(view_func)
    @login_required(login_url="/accounts/staff-login/")
    def wrapper(request, *args, **kwargs):

        if not request.user.is_staff:
            return redirect("dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper
