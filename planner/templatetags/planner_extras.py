from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def status_badge(status: str) -> str:
    if not status:
        return "badge bg-secondary"
    status = str(status).lower()
    if status == "final":
        return "badge bg-info text-white shadow-sm"
    if status == "draft":
        return "badge bg-warning text-dark shadow-sm"
    return "badge bg-secondary"


@register.filter
def species_icon(species: str) -> str:
    if not species:
        return "fas fa-paw"
    s = str(species).lower()
    if "dog" in s:
        return "fas fa-dog"
    if "cat" in s:
        return "fas fa-cat"
    return "fas fa-paw"


@register.filter
def species_color_class(species: str) -> str:
    if not species:
        return "primary"
    s = str(species).lower()
    if "dog" in s:
        return "primary" # Blue/Indigo for dogs
    if "cat" in s:
        return "info"    # Purple for cats
    return "success"     # Teal for others


@register.filter
def format_date_long(value):
    if not value:
        return ""
    try:
        return value.strftime("%b %d, %Y")
    except Exception:
        return str(value)


@register.filter
def age_years(birth_date) -> int:
    if not birth_date:
        return 0
    today = timezone.localdate()
    years = today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )
    return max(0, years)
