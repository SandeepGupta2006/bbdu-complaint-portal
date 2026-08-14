from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):

    list_display = (
        "complaint_id",
        "student",
        "category",
        "priority",
        "status",
        "created_at",
    )

    list_filter = (
        "category",
        "priority",
        "status",
        "created_at",
    )

    search_fields = (
        "complaint_id",
        "subject",
        "description",
        "student__username",
        "student__email",
    )

    readonly_fields = (
        "complaint_id",
        "created_at",
        "updated_at",
    )
