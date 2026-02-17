from django.shortcuts import render
from django.views.generic import DetailView
from .models import Vaccine

def vaccine_list(request):
    vaccines = Vaccine.objects.all()
    return render(request, "vaccines/vaccine_list.html", {"vaccines": vaccines})

class VaccineDetailView(DetailView):
    model = Vaccine
    template_name = "vaccines/vaccine_detail.html"
    context_object_name = "vaccine"
