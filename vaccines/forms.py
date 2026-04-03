from django import forms
from .vaccine_choices import VaccineCategory

class VaccineSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        label="Search Vaccines",
        widget=forms.TextInput(attrs={'placeholder': 'Search by name or description...', 'class': 'form-control rounded-pill px-4'})
    )
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + list(VaccineCategory.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select rounded-pill px-4'})
    )
