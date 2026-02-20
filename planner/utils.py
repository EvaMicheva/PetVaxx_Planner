from datetime import date, timedelta
from calendar import monthrange

from vaccines.models import RecommendationRule, Species
from .models import Dose


def add_months(birthday: date, months: int) -> date:
    year = birthday.year + (birthday.month - 1 + months) // 12
    month = (birthday.month - 1 + months) % 12 + 1
    day = min(birthday.day, monthrange(year, month)[1])
    return date(year, month, day)


class DoseGenerator:
    """
    TODO: Implement logic for:
    -handle expired vaccines like Lepto or FelV.
    -handle vaccine history.

    """


    def __init__(self, plan):
        self.plan = plan
        self.pet = plan.pet
        self.species = self.get_species()
        self.is_outdoor = self.pet.lifestyle in ("outdoor", "mixed")

    def generate(self):
        if not self.species:
            return []

        rules = self.get_applicable_rules()
        doses_to_create = []

        for rule in rules:
            if not self.is_rule_applicable(rule):
                continue

            due_date = self.calculate_due_date(rule)

            if not self.is_valid_due_date(due_date):
                continue

            doses_to_create.append(self.build_dose(rule, due_date))

        return Dose.objects.bulk_create(doses_to_create)

    def get_species(self):
        return Species.objects.filter(code=self.pet.species).first()

    def get_applicable_rules(self):
        return RecommendationRule.objects.filter(species=self.species)

    def is_rule_applicable(self, rule):
        if rule.requires_outdoor and not self.is_outdoor:
            return False
        if rule.requires_travel and not self.pet.travels_abroad:
            return False
        return True

    def calculate_due_date(self, rule):
        due_date = self.calculate_initial_due_date(rule)

        if rule.repeat_every_months:
            due_date = due_date or self.pet.birth_date
            while due_date < self.plan.plan_start_date:
                due_date = add_months(due_date, rule.repeat_every_months)

        return due_date

    def calculate_initial_due_date(self, rule):
        if rule.due_age_weeks:
            return self.pet.birth_date + timedelta(weeks=rule.due_age_weeks)
        if rule.due_age_months:
            return add_months(self.pet.birth_date, rule.due_age_months)
        return None

    def is_valid_due_date(self, due_date):
        return bool(due_date and due_date >= self.plan.plan_start_date)

    def build_dose(self, rule, due_date):
        return Dose(
            plan=self.plan,
            vaccine=rule.vaccine,
            dose_number=rule.dose_number,
            due_date=due_date,
            is_booster=bool(rule.repeat_every_months or rule.dose_number >= 2),
            notes=rule.notes,
        )


