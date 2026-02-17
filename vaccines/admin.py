from django.contrib import admin

from vaccines.models import Vaccine


@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    pass
