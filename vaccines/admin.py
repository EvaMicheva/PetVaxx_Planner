from django.contrib import admin

from vaccines.models import Vaccine, Species, RecommendationRule


@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["category"]
    search_fields = ["name", "category"]



@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ["code", "name"]
    list_filter = ["code"]
    search_fields = ["code", "name"]

@admin.register(RecommendationRule)
class RecommendationRuleAdmin(admin.ModelAdmin):
    list_display = ["species", "vaccine", "dose_number"]
    list_filter = ["species", "vaccine"]
    search_fields = ["species__name", "vaccine__name"]