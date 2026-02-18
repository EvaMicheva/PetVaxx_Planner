def add_months(sourcedate, months):

    import datetime
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1


    day = min(sourcedate.day, [31,
        29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1])
    return datetime.date(year, month, day)

def generate_doses_for_plan(plan):

    from datetime import timedelta
    from vaccines.models import RecommendationRule, Species
    from .models import Dose
    pet = plan.pet
    # Get the species object
    try:
        species_obj = Species.objects.get(code=pet.species)
    except Species.DoesNotExist:
        return []

    # Filter rules for the species
    rules = RecommendationRule.objects.filter(species=species_obj)

    # Filter rules by pet's lifestyle/travels
    # If a rule requires_outdoor=True, the pet must be 'outdoor' or 'mixed'
    # If a rule requires_travel=True, pet must have travels_abroad=True
    # Lifestyle choices (from pets_choices.py): INDOOR, OUTDOOR, MIXED
    is_outdoor_pet = pet.lifestyle in ['outdoor', 'mixed']
    
    generated_doses = []
    
    for rule in rules:
        # Check if rule matches pet's lifestyle/travels
        if rule.requires_outdoor and not is_outdoor_pet:
            continue
        if rule.requires_travel and not pet.travels_abroad:
            continue
            
        # Calculate due date based on birth_date
        due_date = None
        if rule.due_age_weeks is not None:
            due_date = pet.birth_date + timedelta(weeks=rule.due_age_weeks)
        elif rule.due_age_months is not None:
            due_date = add_months(pet.birth_date, rule.due_age_months)
            
        if due_date:
            # Only generate if due_date is >= plan_start_date (so we don't schedule past things in new plans)
            # Actually, sometimes we want full history, but for a NEW plan, 
            # let's assume we want doses from the plan_start_date onwards.
            # But wait, birth_date is the anchor.
            
            # Let's just create it if it's within a reasonable window from plan_start_date or in the future
            # If user starts plan today, they probably want current/future doses.
            # For simplicity, let's create ALL doses that are >= plan_start_date.
            
            if due_date >= plan.plan_start_date:
                dose = Dose.objects.create(
                    plan=plan,
                    vaccine=rule.vaccine,
                    dose_number=rule.dose_number,
                    due_date=due_date,
                    is_booster=(rule.repeat_every_months is not None or rule.dose_number > 3), # Heuristic
                    notes=rule.notes
                )
                generated_doses.append(dose)
                
    return generated_doses
