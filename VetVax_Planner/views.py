from django.shortcuts import render


def custom_404(request, exception=None):
    """Render the custom 404 error page."""
    return render(request, "404.html", status=404)
