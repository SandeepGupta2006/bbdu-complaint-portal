from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html"
        ),
        name="login"
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(
            next_page="/accounts/login/"
        ),
        name="logout"
    ),

    path(
        "admin-logout/",
        LogoutView.as_view(
            next_page="/accounts/staff-login/"
        ),
        name="admin_logout"
    ),

    path(
        "register/",
        views.register_student,
        name="register_student"
    ),

    path(
        "staff-login/",
        views.staff_login,
        name="staff_login"
    ),

    path(
        "forgot-password/",
        views.forgot_password,
        name="forgot_password"
    ),

    path(
        "verify-otp/",
        views.verify_otp,
        name="verify_otp"
    ),

    path(
        "reset-password/",
        views.reset_password,
        name="reset_password"
    ),
]
