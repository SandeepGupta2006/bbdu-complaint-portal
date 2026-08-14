from django import forms
from .models import Complaint


class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint

        fields = [
            "category",
            "subject",
            "description",
            "priority",
        ]

        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter complaint subject"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Describe your complaint in detail"
                }
            ),

            "priority": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
        }
