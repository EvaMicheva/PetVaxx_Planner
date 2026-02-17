from django.db import models


class PlanStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    FINAL = "final", "Final"
