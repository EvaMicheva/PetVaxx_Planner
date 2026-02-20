from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from pets.models import Pet
from vaccines.models import Vaccine
from .models import Plan
from .forms import PlanForm, QuickPlanForm
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

    def get_queryset(self):
        qs = super().get_queryset().select_related("pet")
        status = self.request.GET.get("status")
        if status in {"draft", "final"}:
            qs = qs.filter(status=status)
        order = self.request.GET.get("order")
        if order == "start_asc":
            qs = qs.order_by("plan_start_date", "pet__name")
        elif order == "start_desc":
            qs = qs.order_by("-plan_start_date", "pet__name")
        elif order == "created_asc":
            qs = qs.order_by("created_at")
        else:
            qs = qs.order_by("-created_at")
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["current_status"] = self.request.GET.get("status", "")
        ctx["current_order"] = self.request.GET.get("order", "-created")
        ctx["total_count"] = Plan.objects.count()
        return ctx

class PlanDetailView(DetailView):
    model = Plan
    template_name = "planner/plan_detail.html"
    context_object_name = "plan"

class PlanCreateView(CreateView):
    model = Plan
    form_class = PlanForm
    template_name = "planner/plan_form.html"
    success_url = reverse_lazy("planner:list")

    def form_valid(self, form):
        plan = form.save()
        if not plan.doses.exists():
            generate_doses_for_plan(plan)
        messages.success(self.request, "Vaccination plan created!")
        return redirect(self.success_url)

class PlanUpdateView(UpdateView):
    model = Plan
    form_class = PlanForm
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
        form = QuickPlanForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            pet = Pet.objects.create(
                name=cd["name"],
                species=cd["species"],
                birth_date=cd["birth_date"],
                lifestyle=cd["lifestyle"],
                travels_abroad=cd["travels_abroad"],
            )
            plan = Plan.objects.create(
                pet=pet,
                plan_start_date=timezone.localdate(),
                status="draft",
            )

            generate_doses_for_plan(plan)
            messages.success(request, f"Plan generated for {pet.name} with all recommended doses!")
            return redirect(reverse("planner:detail", kwargs={"pk": plan.pk}))
    else:
        form = QuickPlanForm()

    return render(request, "planner/quick_plan_form.html", {
        "form": form,
    })