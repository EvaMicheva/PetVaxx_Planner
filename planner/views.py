from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from pets.models import Pet
from vaccines.models import Vaccine
from .models import Plan
from .forms import PlanForm, QuickPlanForm
from .utils import DoseGenerator

def home(request):
    if request.user.is_authenticated:
        pets_count = Pet.objects.filter(user=request.user).count()
        plans_count = Plan.objects.filter(pet__user=request.user).count()
    else:
        pets_count = 0
        plans_count = 0
        
    return render(request, "home.html", {
        "pets_count": pets_count,
        "vaccines_count": Vaccine.objects.count(),
        "plans_count": plans_count,
    })

class PlanListView(LoginRequiredMixin, ListView):
    model = Plan
    template_name = "planner/plan_list.html"
    context_object_name = "plans"

    def get_queryset(self):
        qs = super().get_queryset().filter(pet__user=self.request.user).select_related("pet")

        status = self.request.GET.get("status")
        if status in {"draft", "final"}:
            qs = qs.filter(status=status)

        order_map = {
            "start_asc": ("plan_start_date", "pet__name"),
            "start_desc": ("-plan_start_date", "pet__name"),
            "created_asc": ("created_at",),
            "created_desc": ("-created_at",),
        }
        order = self.request.GET.get("order", "created_desc")
        return qs.order_by(*order_map.get(order, ("-created_at",)))

    def get_context_data(self, **kwargs):
        return super().get_context_data(**{
            "current_status": self.request.GET.get("status", ""),
            "current_order": self.request.GET.get("order", "created_desc"),
            "total_count": Plan.objects.filter(pet__user=self.request.user).count(),
            **kwargs
        })

class PlanDetailView(LoginRequiredMixin, DetailView):
    model = Plan
    template_name = "planner/plan_detail.html"
    context_object_name = "plan"

    def get_queryset(self):
        return super().get_queryset().filter(pet__user=self.request.user)

class PlanCreateView(LoginRequiredMixin, CreateView):
    model = Plan
    form_class = PlanForm
    template_name = "planner/plan_form.html"
    success_url = reverse_lazy("planner:list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['pet'].queryset = Pet.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        plan = form.save()
        if not plan.doses.exists():
            DoseGenerator(plan).generate()
        messages.success(self.request, "Vaccination plan created!")
        return super().form_valid(form)

class PlanUpdateView(LoginRequiredMixin, UpdateView):
    model = Plan
    form_class = PlanForm
    template_name = "planner/plan_form.html"
    success_url = reverse_lazy("planner:list")

    def get_queryset(self):
        return super().get_queryset().filter(pet__user=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['pet'].queryset = Pet.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        messages.success(self.request, "Vaccination plan updated!")
        return super().form_valid(form)

class PlanDeleteView(LoginRequiredMixin, DeleteView):
    model = Plan
    template_name = "planner/plan_confirm_delete.html"
    success_url = reverse_lazy("planner:list")

    def get_queryset(self):
        return super().get_queryset().filter(pet__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.warning(request, "Vaccination plan removed.")
        return super().delete(request, *args, **kwargs)

@login_required
def quick_plan_create(request):
    if request.method == "POST":
        form = QuickPlanForm(request.POST)
        form.fields['pet'].queryset = Pet.objects.filter(user=request.user)
        if form.is_valid():
            cd = form.cleaned_data

            if cd.get("pet"):
                pet = cd["pet"]
            else:
                pet = Pet.objects.create(
                    user=request.user,
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

            DoseGenerator(plan).generate()
            messages.success(request, f"Plan generated for {pet.name} with all recommended doses!")
            return redirect(reverse("planner:detail", kwargs={"pk": plan.pk}))
    else:
        form = QuickPlanForm()
        form.fields['pet'].queryset = Pet.objects.filter(user=request.user)

    return render(request, "planner/quick_plan_form.html", {
        "form": form,
    })