from django import forms
from django.utils import timezone

from .models import Pet


class PetForm(forms.ModelForm):

    age_in_weeks = forms.IntegerField(
        required=False,
        disabled=True,
        label="Age (weeks)",
        help_text="Calculated from birth date; read-only."
    )

    class Meta:
        model = Pet
        fields = '__all__'

        labels = {
            "name": "Pet Name",
            "species": "Species",
            "birth_date": "Birth Date",
            "lifestyle": "Lifestyle",
            "travels_abroad": "Travels Abroad?",
            "notes": " Important Notes",
        }
        help_texts = {
            "name": "Enter your pet's name.",
            "species": "Choose from the list or enter a custom species name.",
            "birth_date": "Use the calendar to select the correct date.",
            "lifestyle": "Used to determine optional vaccine recommendations.",
            "travels_abroad": "Enable if your pet travels internationally.",
            "notes": "Add any relevant medical history or allergies.",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Buddy"}),
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3, "placeholder": "Any special considerations?"}),
        }
        error_messages = {
            "name": {
                "required": "Please provide your pet's name.",
                "max_length": "Name is too long. Please keep it under 80 characters.",
            },
            "birth_date": {
                "invalid": "Please enter a valid date.",
                "required": "Birth date is required to calculate vaccine timing.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        birth = None

        if self.instance and self.instance.pk:
            birth = self.instance.birth_date

        if birth:
            self.fields["age_in_weeks"].initial = max(
                0,
                (timezone.localdate() - birth).days // 7
            )

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")

        if birth_date is not None and birth_date > timezone.localdate():
            raise forms.ValidationError(
                "Birth date cannot be in the future."
            )
        if birth_date:
            self.cleaned_data["age_in_weeks"] = max(
                0,
                (timezone.localdate() - birth_date).days // 7
            )

        return birth_date