from django.db import models

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .pets_choices import PetSpecies, Lifestyle


class Pet(models.Model):
    name = models.CharField(max_length=80)
    species = models.CharField(max_length=10, choices=PetSpecies)
    birth_date = models.DateField()

    lifestyle = models.CharField(
        max_length=10,
        choices=Lifestyle,
        default=Lifestyle.MIXED,
    )
    travels_abroad = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def clean(self):
        if self.birth_date and self.birth_date > timezone.localdate():
            raise ValidationError({"birth_date": "Birth date cannot be in the future, please use a valid date."})

    def age_in_days(self) -> int:
        if not self.birth_date:
            return 0
        return max(0, (timezone.localdate() - self.birth_date).days)

    def age_in_weeks(self) -> int:
        return self.age_in_days() // 7

    def __str__(self) -> str:
        return f"{self.name} - {self.species}"
