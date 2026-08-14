from django.db import models
from accounts.models import StudentProfile
from django.utils import timezone


class Complaint(models.Model):

    CATEGORY_CHOICES = [
        ("Academic", "Academic"),
        ("Hostel", "Hostel"),
        ("Library", "Library"),
        ("Transport", "Transport"),
        ("Faculty", "Faculty"),
        ("Other", "Other"),
    ]

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Urgent", "Urgent"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Under Review", "Under Review"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
        ("Closed", "Closed"),
    ]

    complaint_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="complaints"
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    subject = models.CharField(
        max_length=200
    )

    description = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Medium"
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.complaint_id:
            year = timezone.now().year

            last_complaint = (
                Complaint.objects
                .filter(complaint_id__startswith=f"BBDU-{year}-")
                .order_by("-id")
                .first()
            )

            if last_complaint:
                last_number = int(
                    last_complaint.complaint_id.split("-")[-1]
                )
                next_number = last_number + 1
            else:
                next_number = 1

            self.complaint_id = (
                f"BBDU-{year}-{next_number:06d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.complaint_id
