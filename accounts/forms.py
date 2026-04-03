from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    phone = forms.CharField(max_length=20, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            from .models import Profile
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': self.cleaned_data.get('first_name'),
                    'last_name': self.cleaned_data.get('last_name'),
                    'phone': self.cleaned_data.get('phone'),
                }
            )
        return user
