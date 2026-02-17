from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from pets.models import Pet
from vaccines.models import Vaccine, Species
from planner.models import Plan, Dose
from planner.planner_choices import PlanStatus


class PlanModelTest(TestCase):
    def setUp(self):
        self.pet = Pet.objects.create(
            name="Max",
            species="dog",
            birth_date=date(2020, 1, 1)
        )

    def test_plan_creation(self):
        plan = Plan.objects.create(
            pet=self.pet,
            plan_start_date=date(2025, 1, 1),
            status=PlanStatus.DRAFT
        )
        self.assertEqual(str(plan), "Plan for Max (2025-01-01)")

    def test_plan_start_date_before_birth_date(self):
        plan = Plan(
            pet=self.pet,
            plan_start_date=date(2019, 12, 31),
            status=PlanStatus.DRAFT
        )
        with self.assertRaises(ValidationError):
            plan.full_clean()


class DoseModelTest(TestCase):
    def setUp(self):
        self.species = Species.objects.create(code="dog", name="Dog")
        self.pet = Pet.objects.create(
            name="Buddy",
            species="dog",
            birth_date=date(2025, 1, 1)
        )
        self.vaccine = Vaccine.objects.create(name="Core Vax")
        self.vaccine.applicable_species.add(self.species)
        self.plan = Plan.objects.create(
            pet=self.pet,
            plan_start_date=date(2025, 2, 1),
            status=PlanStatus.DRAFT
        )

    def test_dose_creation(self):
        dose = Dose.objects.create(
            plan=self.plan,
            vaccine=self.vaccine,
            dose_number=1,
            due_date=date(2025, 2, 10)
        )
        self.assertEqual(str(dose), "Core Vax dose 1 on 2025-02-10")

    def test_unique_dose_constraint(self):
        Dose.objects.create(
            plan=self.plan,
            vaccine=self.vaccine,
            dose_number=1,
            due_date=date(2025, 2, 10)
        )
        with self.assertRaises(Exception):  # IntegrityError
            Dose.objects.create(
                plan=self.plan,
                vaccine=self.vaccine,
                dose_number=1,
                due_date=date(2025, 3, 10)
            )

    def test_dose_ordering(self):
        v2 = Vaccine.objects.create(name="Antigen B")
        v2.applicable_species.add(self.species)
        
        d1 = Dose.objects.create(plan=self.plan, vaccine=self.vaccine, dose_number=2, due_date=date(2025, 3, 1))
        d2 = Dose.objects.create(plan=self.plan, vaccine=v2, dose_number=1, due_date=date(2025, 2, 15))
        
        doses = Dose.objects.all()
        self.assertEqual(doses[0], d2)
        self.assertEqual(doses[1], d1)
