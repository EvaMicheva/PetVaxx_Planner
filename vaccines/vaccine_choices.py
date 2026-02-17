from django.db import models


class VaccineCategory(models.TextChoices):
    CORE = "core", "Core"
    OPTIONAL = "optional", "Optional (risk-based)"

    def __str__(self):
        return self.label

