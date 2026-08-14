from django.core.exceptions import ValidationError


def validate_bbdu_email(email):

    email = email.strip().lower()

    if not email.endswith("@bbdu.ac.in"):
        raise ValidationError(
            "Please use your official BBDU email address."
        )

    return email
