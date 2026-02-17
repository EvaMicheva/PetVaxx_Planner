from django.contrib import admin

from pets.models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ["name", "species", "birth_date"]
    list_filter = ["species"]
    search_fields = ["name", "species"]
