from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def status_badge(status: str) -> str:
    """Return Bootstrap badge classes for a plan status."""
    if not status:
        return "badge bg-secondary"
    status = str(status).lower()
    if status == "final":
        return "badge bg-success shadow-sm"
    if status == "draft":
        return "badge bg-warning text-dark"
    return "badge bg-secondary"


@register.filter
def species_icon(species: str) -> str:
    """Font Awesome icon class based on species code/name."""
    if not species:
        return "fas fa-paw"
    s = str(species).lower()
    if "dog" in s:
        return "fas fa-dog"
    if "cat" in s:
        return "fas fa-cat"
    return "fas fa-paw"


@register.filter
def format_date_long(value):
    """Format a date in a friendly long form."""
    if not value:
        return ""
    try:
        return value.strftime("%b %d, %Y")
    except Exception:
        return str(value)


@register.filter
def age_years(birth_date) -> int:
    """Compute age in whole years from a birth_date."""
    if not birth_date:
        return 0
    today = timezone.localdate()
    years = today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )
    return max(0, years)
