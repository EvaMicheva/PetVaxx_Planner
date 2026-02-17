from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from .models import Pet

def pet_list(request):
    pets = Pet.objects.all()
    return render(request, "pets/pet_list.html", {"pets": pets})

class PetDetailView(DetailView):
    model = Pet
    template_name = "pets/pet_detail.html"
    context_object_name = "pet"

class PetCreateView(CreateView):
    model = Pet
    fields = ["name", "species", "birth_date", "lifestyle", "travels_abroad", "notes"]
    template_name = "pets/pet_form.html"
    success_url = reverse_lazy("pets:list")

    def form_valid(self, form):
        messages.success(self.request, f"Pet '{form.instance.name}' added successfully!")
        return super().form_valid(form)

class PetUpdateView(UpdateView):
    model = Pet
    fields = ["name", "species", "birth_date", "lifestyle", "travels_abroad", "notes"]
    template_name = "pets/pet_form.html"
    success_url = reverse_lazy("pets:list")

    def form_valid(self, form):
        messages.success(self.request, f"Pet '{form.instance.name}' updated successfully!")
        return super().form_valid(form)

class PetDeleteView(DeleteView):
    model = Pet
    template_name = "pets/pet_confirm_delete.html"
    success_url = reverse_lazy("pets:list")

    def delete(self, request, *args, **kwargs):
        pet = self.get_object()
        messages.warning(request, f"Pet '{pet.name}' deleted.")
        return super().delete(request, *args, **kwargs)
