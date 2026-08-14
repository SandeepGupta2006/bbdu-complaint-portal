from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.models import StudentProfile
from .forms import ComplaintForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Complaint
from accounts.decorators import student_required
from django.shortcuts import get_object_or_404


def home(request):
    return render(
        request,
        "complaints/home.html"
    )


@student_required
def register_complaint(request):

    if request.method == "POST":

        form = ComplaintForm(request.POST)

        if form.is_valid():

            complaint = form.save(commit=False)

            student_profile = StudentProfile.objects.get(
                user=request.user
            )

            complaint.student = student_profile

            complaint.save()

            return redirect(
                "complaint_success",
                complaint_id=complaint.complaint_id
            )

    else:
        form = ComplaintForm()

    return render(
        request,
        "complaints/register_complaint.html",
        {"form": form}
    )


@student_required
def complaint_success(request, complaint_id):

    return render(
        request,
        "complaints/success.html",
        {
            "complaint_id": complaint_id
        }
    )


@student_required
def dashboard(request):

    student_profile = StudentProfile.objects.get(
        user=request.user
    )

    complaints = Complaint.objects.filter(
        student=student_profile
    ).order_by("-created_at")

    pending_count = complaints.filter(
        status="Pending"
    ).count()

    resolved_count = complaints.filter(
        status="Resolved"
    ).count()

    return render(
        request,
        "complaints/dashboard.html",
        {
            "complaints": complaints,
            "pending_count": pending_count,
            "resolved_count": resolved_count,
        }
    )


@staff_member_required
def admin_dashboard(request):

    total_complaints = Complaint.objects.count()

    pending_complaints = Complaint.objects.filter(
        status="Pending"
    ).count()

    under_review_complaints = Complaint.objects.filter(
        status="Under Review"
    ).count()

    in_progress_complaints = Complaint.objects.filter(
        status="In Progress"
    ).count()

    resolved_complaints = Complaint.objects.filter(
        status="Resolved"
    ).count()

    recent_complaints = Complaint.objects.select_related(
        "student",
        "student__user"
    ).order_by("-created_at")[:10]

    context = {
        "total_complaints": total_complaints,
        "pending_complaints": pending_complaints,
        "under_review_complaints": under_review_complaints,
        "in_progress_complaints": in_progress_complaints,
        "resolved_complaints": resolved_complaints,
        "recent_complaints": recent_complaints,
    }

    return render(
        request,
        "complaints/admin_dashboard.html",
        context
    )


@staff_member_required
def admin_update_complaint(request, complaint_id):

    complaint = get_object_or_404(
        Complaint,
        complaint_id=complaint_id
    )

    if request.method == "POST":

        new_status = request.POST.get("status")

        if new_status in [
            "Pending",
            "Under Review",
            "In Progress",
            "Resolved"
        ]:
            complaint.status = new_status
            complaint.save()

        return redirect("admin_dashboard")

    return render(
        request,
        "complaints/admin_update_complaint.html",
        {
            "complaint": complaint
        }
    )


@staff_member_required
def admin_complaints(request):

    complaints = Complaint.objects.select_related(
        "student",
        "student__user"
    ).order_by("-created_at")

    return render(
        request,
        "complaints/admin_complaints.html",
        {
            "complaints": complaints,
        }
    )
