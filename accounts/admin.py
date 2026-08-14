from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "roll_number",
        "department",
        "course",
        "year",
    )

    search_fields = (
        "roll_number",
        "user__username",
        "user__email",
    )

    list_filter = (
        "department",
        "course",
        "year",
    )
