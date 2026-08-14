from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "register/",
        views.register_complaint,
        name="register_complaint"
    ),

    path(
        "success/<str:complaint_id>/",
        views.complaint_success,
        name="complaint_success"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "admin-dashboard/complaint/<str:complaint_id>/",
        views.admin_update_complaint,
        name="admin_update_complaint"
    ),

    path(
        "admin/complaints/",
        views.admin_complaints,
        name="admin_complaints"
    ),
]
