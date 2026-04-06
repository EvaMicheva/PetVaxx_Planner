from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from .models import Pet
from .forms import PetForm

@login_required
def pet_list(request):
    if request.user.is_vet or request.user.groups.filter(name='Vet Administrators').exists() or request.user.is_superuser:
        pets = Pet.objects.all()
    else:
        pets = Pet.objects.filter(user=request.user)
    return render(request, "pets/pet_list.html", {"pets": pets})

class PetDetailView(LoginRequiredMixin, DetailView):
    model = Pet
    template_name = "pets/pet_detail.html"
    context_object_name = "pet"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        import django.shortcuts
        obj = django.shortcuts.get_object_or_404(Pet, pk=self.kwargs.get(self.pk_url_kwarg, 'pk'))

        if not (self.request.user.is_vet or self.request.user.groups.filter(name='Vet Administrators').exists() or self.request.user.is_superuser):
            if obj.user != self.request.user:
                from django.core.exceptions import PermissionDenied
                raise PermissionDenied
        return obj

    def get_queryset(self):
        if self.request.user.is_vet or self.request.user.groups.filter(name='Vet Administrators').exists() or self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)

class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetForm
    template_name = "pets/pet_form.html"
    success_url = reverse_lazy("pets:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not form.instance.user:
            form.instance.user = self.request.user
        messages.success(self.request, f"Pet '{form.instance.name}' added successfully!")
        return super().form_valid(form)

class PetUpdateView(LoginRequiredMixin, UpdateView):
    model = Pet
    form_class = PetForm
    template_name = "pets/pet_form.html"
    success_url = reverse_lazy("pets:list")

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        
        import django.shortcuts
        obj = django.shortcuts.get_object_or_404(Pet, pk=self.kwargs.get(self.pk_url_kwarg, 'pk'))

        if not (self.request.user.is_vet or self.request.user.groups.filter(name='Vet Administrators').exists() or self.request.user.is_superuser):
            if obj.user != self.request.user:
                from django.core.exceptions import PermissionDenied
                raise PermissionDenied
        return obj

    def get_queryset(self):
        if self.request.user.is_vet or self.request.user.groups.filter(name='Vet Administrators').exists() or self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, f"Pet '{form.instance.name}' updated successfully!")
        return super().form_valid(form)

class PetDeleteView(LoginRequiredMixin, DeleteView):
    model = Pet
    template_name = "pets/pet_confirm_delete.html"
    success_url = reverse_lazy("pets:list")

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        
        import django.shortcuts
        obj = django.shortcuts.get_object_or_404(Pet, pk=self.kwargs.get(self.pk_url_kwarg, 'pk'))

        if not (self.request.user.is_vet or self.request.user.groups.filter(name='Vet Administrators').exists() or self.request.user.is_superuser):
            if obj.user != self.request.user:
                from django.core.exceptions import PermissionDenied
                raise PermissionDenied
        return obj

    def get_queryset(self):
        if self.request.user.is_vet or self.request.user.groups.filter(name='Vet Administrators').exists() or self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        pet = self.get_object()
        messages.warning(request, f"Pet '{pet.name}' deleted.")
        return super().delete(request, *args, **kwargs)
