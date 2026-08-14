from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def student_required(view_func):

    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):

        if not hasattr(request.user, "studentprofile"):
            return redirect("admin_dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper
