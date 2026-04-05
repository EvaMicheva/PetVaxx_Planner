from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_vet', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Veterinary Info', {'fields': ('is_vet',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Veterinary Info', {'fields': ('is_vet',)}),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone')
