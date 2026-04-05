from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_vet = models.BooleanField(
        default=False, 
        verbose_name="Is Veterinarian",
        help_text="Designates whether this user has veterinary administrative privileges."
    )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
