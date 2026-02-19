from datetime import date, timedelta
from calendar import monthrange

def add_months(birthday, months):
    year = birthday.year + (birthday.month - 1 + months) // 12
    month = (birthday.month - 1 + months) % 12 + 1
    day = min(birthday.day, monthrange(year, month)[1])
    return date(year, month, day)


def generate_doses_for_plan(plan):
    from vaccines.models import RecommendationRule, Species
    from .models import Dose

    pet = plan.pet

    species = Species.objects.filter(code=pet.species).first()
    if not species:
        return []

    rules = RecommendationRule.objects.filter(species=species)

    is_outdoor = pet.lifestyle in ("outdoor", "mixed")

    doses = []

    for rule in rules:

        if rule.requires_outdoor and not is_outdoor:
            continue

        if rule.requires_travel and not pet.travels_abroad:
            continue

        due_date = None

        if rule.due_age_weeks:
            due_date = pet.birth_date + timedelta(weeks=rule.due_age_weeks)

        elif rule.due_age_months:
            due_date = add_months(pet.birth_date, rule.due_age_months)

        if not due_date or due_date < plan.plan_start_date:
            continue

        dose = Dose.objects.create(
            plan=plan,
            vaccine=rule.vaccine,
            dose_number=rule.dose_number,
            due_date=due_date,
            is_booster=bool(rule.dose_number >= 2),
            notes=rule.notes,
        )

        doses.append(dose)

    return doses

