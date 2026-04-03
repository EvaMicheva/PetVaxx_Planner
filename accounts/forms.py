from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import Group
from .models import Profile

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    phone = forms.CharField(max_length=20, required=True)
    is_vet = forms.BooleanField(
        required=False, 
        label="Register as Veterinarian",
        help_text="Check this if you are a vet administrator.",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if hasattr(self, 'save_m2m'):
                self.save_m2m()
            
            if self.cleaned_data.get('is_vet'):
                group, _ = Group.objects.get_or_create(name='Vet Administrators')
            else:
                group, _ = Group.objects.get_or_create(name='Regular Users')
            user.groups.add(group)

            Profile.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': self.cleaned_data.get('first_name'),
                    'last_name': self.cleaned_data.get('last_name'),
                    'phone': self.cleaned_data.get('phone'),
                }
            )
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
