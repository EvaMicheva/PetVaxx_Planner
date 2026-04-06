from django import forms
from .vaccine_choices import VaccineCategory

class VaccineSearchForm(forms.Form):
    PILL_CLASSES = 'rounded-pill px-4'

    search_query = forms.CharField(
        required=False,
        label="Search Vaccines",
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by name or description...',
            'class': f'form-control {PILL_CLASSES}'
        })
    )
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + VaccineCategory.choices,
        required=False,
        widget=forms.Select(attrs={'class': f'form-select {PILL_CLASSES}'})
    )
