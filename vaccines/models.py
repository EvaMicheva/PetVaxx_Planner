from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .vaccine_choices import VaccineCategory


class Species(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return self.name


class Vaccine(models.Model):
    name = models.CharField(max_length=120, unique=True)
    category = models.CharField(
        max_length=10,
        choices=VaccineCategory,
        default=VaccineCategory.CORE,
    )

    applicable_species = models.ManyToManyField(Species, related_name="vaccines")

    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.get_category_display()})"


class RecommendationRule(models.Model):
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name="rules")
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name="rules")

    dose_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    due_age_weeks = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(400)],
        null=True, blank=True
    )
    due_age_months = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(240)],
        null=True, blank=True
    )

    repeat_every_months = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        null=True, blank=True
    )

    requires_outdoor = models.BooleanField(default=False)
    requires_travel = models.BooleanField(default=False)

    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["vaccine", "species", "dose_number"],
                name="uniq_rule_vaccine_species_dose"
            )
        ]

    def clean(self):
        if self.due_age_weeks is not None and self.due_age_months is not None:
            raise ValidationError("Use either due_age_weeks OR due_age_months, not both.")

    def __str__(self) -> str:
        return f"{self.vaccine.name} - {self.species.name} dose {self.dose_number}"

