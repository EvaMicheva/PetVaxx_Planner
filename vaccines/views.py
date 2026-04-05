from django.shortcuts import render
from django.views.generic import DetailView
from .models import Vaccine

from django.db.models import Q
from .forms import VaccineSearchForm

def vaccine_list(request):
    form = VaccineSearchForm(request.GET or None)
    vaccines = Vaccine.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('search_query')
        category = form.cleaned_data.get('category')
        
        if query:
            vaccines = vaccines.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        if category:
            vaccines = vaccines.filter(category=category)

    return render(request, "vaccines/vaccine_list.html", {
        "vaccines": vaccines,
        "form": form
    })

class VaccineDetailView(DetailView):
    model = Vaccine
    template_name = "vaccines/vaccine_detail.html"
    context_object_name = "vaccine"

from rest_framework import generics, permissions
from .serializers import VaccineSerializer

class VaccineListAPI(generics.ListAPIView):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
