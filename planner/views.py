from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from pets.models import Pet
from vaccines.models import Vaccine
from .models import Plan
from .utils import generate_doses_for_plan

def home(request):
    return render(request, "home.html", {
        "pets_count": Pet.objects.count(),
        "vaccines_count": Vaccine.objects.count(),
        "plans_count": Plan.objects.count(),
    })

class PlanListView(ListView):
    model = Plan
    template_name = "planner/plan_list.html"
    context_object_name = "plans"
    ordering = ["-created_at"]

class PlanDetailView(DetailView):
    model = Plan
    template_name = "planner/plan_detail.html"
    context_object_name = "plan"

class PlanCreateView(CreateView):
    model = Plan
    fields = ["pet", "plan_start_date", "status"]
    template_name = "planner/plan_form.html"
    success_url = reverse_lazy("planner:list")

    def form_valid(self, form):
        messages.success(self.request, "Vaccination plan created!")
        return super().form_valid(form)

class PlanUpdateView(UpdateView):
    model = Plan
    fields = ["pet", "plan_start_date", "status"]
    template_name = "planner/plan_form.html"
    success_url = reverse_lazy("planner:list")

    def form_valid(self, form):
        messages.success(self.request, "Vaccination plan updated!")
        return super().form_valid(form)

class PlanDeleteView(DeleteView):
    model = Plan
    template_name = "planner/plan_confirm_delete.html"
    success_url = reverse_lazy("planner:list")

    def delete(self, request, *args, **kwargs):
        messages.warning(request, "Vaccination plan removed.")
        return super().delete(request, *args, **kwargs)

def quick_plan_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        species = request.POST.get("species")
        birth_date = request.POST.get("birth_date")
        lifestyle = request.POST.get("lifestyle", "mixed")
        travels_abroad = request.POST.get("travels_abroad") == "on"

        try:
            from datetime import datetime
            birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            birth_date_obj = timezone.localdate()

        pet = Pet.objects.create(
            name=name,
            species=species,
            birth_date=birth_date_obj,
            lifestyle=lifestyle,
            travels_abroad=travels_abroad
        )

        plan = Plan.objects.create(
            pet=pet,
            plan_start_date=timezone.localdate(),
            status="draft"
        )
        
        # Generate Doses
        generate_doses_for_plan(plan)
        
        messages.success(request, f"Plan generated for {pet.name} with all recommended doses!")
        return redirect(reverse("planner:detail", kwargs={"pk": plan.pk}))
        
    return render(request, "planner/quick_plan_form.html", {
        "species_choices": Pet._meta.get_field("species").choices,
        "lifestyle_choices": Pet._meta.get_field("lifestyle").choices,
    })