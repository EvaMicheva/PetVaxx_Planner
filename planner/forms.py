from django import forms
from django.utils import timezone
from datetime import timedelta

from .models import Plan
from pets.models import Pet
from pets.pets_choices import Lifestyle, PetSpecies


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ["pet", "plan_start_date", "status"]
        labels = {
            "pet": "Pet",
            "plan_start_date": "Plan Start Date",
            "status": "Status",
        }
        help_texts = {
            "pet": "The pet this vaccination plan belongs to.",
            "plan_start_date": "The first day the plan should be active.",
            "status": "You can keep the plan as a draft until you finalize it.",
        }
        widgets = {
            "plan_start_date": forms.DateInput(attrs={"type": "date", "placeholder": "YYYY-MM-DD"}),
        }
        error_messages = {
            "plan_start_date": {
                "required": "Please provide a start date for the plan.",
                "invalid": "Enter a valid date in YYYY-MM-DD format.",
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["pet"].disabled = True

    def clean_plan_start_date(self):
        date = self.cleaned_data.get("plan_start_date")
        if date is not None and date > timezone.localdate() + timedelta(days=365*5):
            raise forms.ValidationError("Start date seems too far in the future. Please pick a nearer date.")
        return date


class QuickPlanForm(forms.Form):
    name = forms.CharField(
        max_length=80,
        label="Pet Name",
        widget=forms.TextInput(attrs={"placeholder": "e.g. Buddy"}),
        error_messages={
            "required": "Please enter the pet's name.",
            "max_length": "Name cannot exceed 80 characters.",
        },
        help_text="Name will be used when saving the pet and plan.",
    )
    species = forms.ChoiceField(
        choices=Pet._meta.get_field("species").choices,
        label="Species",
        error_messages={"required": "Please select a species."},
    )
    birth_date = forms.DateField(
        label="Birth Date",
        widget=forms.DateInput(attrs={"type": "date"}),
        error_messages={
            "required": "Birth date is required.",
            "invalid": "Please enter a valid date.",
        },
        help_text="Used to determine correct vaccine timing.",
    )
    lifestyle = forms.ChoiceField(
        choices=Pet._meta.get_field("lifestyle").choices,
        initial=Lifestyle.MIXED,
        label="Lifestyle",
        help_text="Helps choose optional vaccine rules.",
    )
    travels_abroad = forms.BooleanField(
        required=False,
        initial=False,
        label="Travels Abroad?",
        help_text="Enable if the pet travels internationally.",
    )

    def clean_birth_date(self):
        b = self.cleaned_data["birth_date"]
        if b > timezone.localdate():
            raise forms.ValidationError("Birth date cannot be in the future.")
        return b
