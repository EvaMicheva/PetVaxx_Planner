from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .planner_choices import PlanStatus


class Plan(models.Model):
    pet = models.ForeignKey("pets.Pet", on_delete=models.CASCADE, related_name="plans")
    plan_start_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=PlanStatus,
        default=PlanStatus.DRAFT,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.pet_id and self.plan_start_date < self.pet.birth_date:
            raise ValidationError({"plan_start_date": "Plan start date cannot be before the pet's birth date."})

    def __str__(self) -> str:
        return f"Plan for {self.pet.name} ({self.plan_start_date})"


class Dose(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="doses")
    vaccine = models.ForeignKey("vaccines.Vaccine", on_delete=models.CASCADE, related_name="doses")

    dose_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    due_date = models.DateField()

    is_booster = models.BooleanField(default=False)
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["due_date", "vaccine__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["plan", "vaccine", "dose_number"],
                name="uniq_dose_plan_vaccine_number"
            )
        ]

    def __str__(self) -> str:
        return f"{self.vaccine.name} dose {self.dose_number} on {self.due_date}"
