from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    roll_number = models.CharField(
        max_length=30,
        unique=True
    )

    department = models.CharField(
        max_length=100
    )

    course = models.CharField(
        max_length=100
    )

    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.roll_number}"


class PasswordResetOTP(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    otp_hash = models.CharField(
        max_length=128
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    attempts = models.PositiveIntegerField(
        default=0
    )

    verified = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"Password reset OTP - {self.user.username}"
