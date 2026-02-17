from django.contrib import admin

from planner.models import Plan, Dose


class DoseInline(admin.TabularInline):
    model = Dose
    extra = 1


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ["pet", "plan_start_date", "status", "created_at"]
    list_filter = ["status", "plan_start_date"]
    search_fields = ["pet__name"]
    inlines = [DoseInline]


@admin.register(Dose)
class DoseAdmin(admin.ModelAdmin):
    list_display = ["vaccine", "plan", "dose_number", "due_date", "is_booster"]
    list_filter = ["is_booster", "due_date", "vaccine"]
    search_fields = ["plan__pet__name", "vaccine__name"]