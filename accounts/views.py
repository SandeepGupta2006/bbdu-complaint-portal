from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import StudentProfile, PasswordResetOTP
from .validators import validate_bbdu_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.conf import settings
import secrets
from datetime import timedelta
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password


def register_student(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")

        try:
            email = validate_bbdu_email(email)

        except ValidationError as e:
            return render(
                request,
                "accounts/register.html",
                {
                    "error": e.message
                }
            )

        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        roll_number = request.POST.get("roll_number")
        department = request.POST.get("department")
        course = request.POST.get("course")
        year = request.POST.get("year")

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "accounts/register.html",
                {
                    "error": "Username already exists."
                }
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "accounts/register.html",
                {
                    "error": "Email already exists."
                }
            )

        if StudentProfile.objects.filter(
            roll_number=roll_number
        ).exists():
            return render(
                request,
                "accounts/register.html",
                {
                    "error": "Roll number already exists."
                }
            )

        try:
            validate_password(
                password,
                user=User(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
            )

        except ValidationError as e:

            return render(
                request,
                "accounts/register.html",
                {
                    "error": e.messages[0]
                }
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        StudentProfile.objects.create(
            user=user,
            roll_number=roll_number,
            department=department,
            course=course,
            year=year
        )

        login(request, user)

        return redirect("dashboard")

    return render(
        request,
        "accounts/register.html"
    )


def staff_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if user.is_staff:

                login(request, user)

                return redirect("admin_dashboard")

            return render(
                request,
                "accounts/staff_login.html",
                {
                    "error": "You do not have staff access."
                }
            )

        return render(
            request,
            "accounts/staff_login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(
        request,
        "accounts/staff_login.html"
    )


def forgot_password(request):

    if request.method == "POST":

        last_otp_sent = request.session.get("otp_sent_at")

        if last_otp_sent:

            elapsed = (timezone.now().timestamp() - last_otp_sent)

            if elapsed < 60:

                remaining = int(60 - elapsed)

                return render(
                    request,
                    "accounts/forgot_password.html",
                    {
                        "error": (
                            f"Please wait {remaining} seconds "
                            "before requesting another OTP."
                        )
                    }
                )

        email = request.POST.get(
            "email",
            ""
        ).strip().lower()

        # Validate BBDU email
        try:
            email = validate_bbdu_email(email)

        except ValidationError as e:

            return render(
                request,
                "accounts/forgot_password.html",
                {
                    "error": e.message
                }
            )

        user = User.objects.filter(
            email__iexact=email
        ).first()

        if user is not None:

            recent_otp = PasswordResetOTP.objects.filter(
                user=user,
                verified=False
            ).order_by(
                "-created_at"
            ).first()

            if recent_otp:

                elapsed = (timezone.now() -
                           recent_otp.created_at).total_seconds()

                if elapsed < 60:

                    remaining = int(
                        60 - elapsed
                    )

                    return render(
                        request,
                        "accounts/forgot_password.html",
                        {
                            "error": (
                                f"Please wait {remaining} seconds "
                                "before requesting another OTP."
                            )
                        }
                    )

            # Invalidate previous OTPs

            PasswordResetOTP.objects.filter(
                user=user,
                verified=False
            ).delete()

            # Generate secure 6-digit OTP

            otp = str(
                secrets.randbelow(900000) + 100000
            )

            # Store hashed OTP

            PasswordResetOTP.objects.create(
                user=user,
                otp_hash=make_password(otp)
            )

            # Send OTP email

            send_mail(
                subject="BBDU Password Reset OTP",

                message=(
                    f"Your BBDU password reset OTP is: {otp}\n\n"
                    "This OTP is valid for 5 minutes.\n"
                    "If you did not request a password reset, "
                    "please ignore this email."
                ),

                from_email=settings.DEFAULT_FROM_EMAIL,

                recipient_list=[user.email],

                fail_silently=False
            )

        request.session["password_reset_email"] = email

        request.session["otp_sent_at"] = (
            timezone.now().timestamp()
        )

        return redirect(
            "verify_otp"
        )

    return render(
        request,
        "accounts/forgot_password.html"
    )


def verify_otp(request):

    if request.method == "POST":

        email = request.session.get(
            "password_reset_email",
            ""
        ).strip().lower()

        otp = request.POST.get(
            "otp",
            ""
        ).strip()

        try:
            email = validate_bbdu_email(email)

        except ValidationError as e:

            return render(
                request,
                "accounts/verify_otp.html",
                {
                    "error": e.message
                }
            )

        user = User.objects.filter(
            email__iexact=email
        ).first()

        if user is None:

            return render(
                request,
                "accounts/verify_otp.html",
                {
                    "error": "Invalid OTP."
                }
            )

        reset_otp = PasswordResetOTP.objects.filter(
            user=user,
            verified=False
        ).order_by(
            "-created_at"
        ).first()

        if reset_otp is None:

            return render(
                request,
                "accounts/verify_otp.html",
                {
                    "error": "OTP is invalid or has expired."
                }
            )

        # Check expiry

        expiry_time = (
            reset_otp.created_at
            + timedelta(minutes=5)
        )

        if timezone.now() > expiry_time:

            reset_otp.delete()

            return render(
                request,
                "accounts/verify_otp.html",
                {
                    "error": "OTP has expired. Please request a new one."
                }
            )

        # Check attempt limit

        if reset_otp.attempts >= 5:

            reset_otp.delete()

            return render(
                request,
                "accounts/verify_otp.html",
                {
                    "error": (
                        "Too many incorrect attempts. "
                        "Please request a new OTP."
                    )
                }
            )

        # Validate OTP format

        if len(otp) != 6 or not otp.isdigit():

            reset_otp.attempts += 1
            reset_otp.save(
                update_fields=["attempts"]
            )

            return render(
                request,
                "accounts/verify_otp.html",
                {
                    "error": "Please enter a valid 6-digit OTP."
                }
            )

        # Check hashed OTP

        if not check_password(
            otp,
            reset_otp.otp_hash
        ):

            reset_otp.attempts += 1
            reset_otp.save(
                update_fields=["attempts"]
            )

            return render(
                request,
                "accounts/verify_otp.html",
                {
                    "error": "Incorrect OTP."
                }
            )

        # OTP verified

        reset_otp.verified = True
        reset_otp.save(
            update_fields=["verified"]
        )

        request.session["password_reset_user"] = user.id

        request.session.pop(
            "password_reset_email",
            None
        )

        request.session.pop(
            "otp_sent_at",
            None
        )

        return redirect(
            "reset_password"
        )

    return render(
        request,
        "accounts/verify_otp.html"
    )


def reset_password(request):

    user_id = request.session.get(
        "password_reset_user"
    )

    if not user_id:
        return redirect("login")

    user = User.objects.filter(
        id=user_id
    ).first()

    if user is None:
        request.session.pop(
            "password_reset_user",
            None
        )

        request.session.pop(
            "password_reset_email",
            None
        )

        return redirect("login")

    if request.method == "POST":

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        if password != confirm_password:

            return render(
                request,
                "accounts/reset_password.html",
                {
                    "error": "Passwords do not match."
                }
            )

        try:
            validate_password(
                password,
                user=user
            )

        except ValidationError as e:

            return render(
                request,
                "accounts/reset_password.html",
                {
                    "error": e.messages[0]
                }
            )

        user.set_password(password)
        user.save()

        # Clear password-reset session data

        request.session.pop(
            "password_reset_user",
            None
        )

        request.session.pop(
            "password_reset_email",
            None
        )

        request.session.pop(
            "otp_sent_at",
            None
        )

        return redirect("login")

    return render(
        request,
        "accounts/reset_password.html"
    )
