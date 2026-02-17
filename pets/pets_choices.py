from django.db import models


class PetSpecies(models.TextChoices):
    DOG = "dog", "Dog"
    CAT = "cat", "Cat"


class Lifestyle(models.TextChoices):
    INDOOR = "indoor", "Indoor"
    OUTDOOR = "outdoor", "Outdoor"
    MIXED = "mixed", "Mixed"


