from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import UserRegistrationForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import asyncio
import threading

def run_async(coro):
    loop = asyncio.new_event_loop()
    threading.Thread(target=loop.run_until_complete, args=(coro,)).start()

async def send_welcome_task(user_email):
    await asyncio.sleep(2)
    print(f"DEBUG: Asynchronous 'Welcome' email successfully sent to {user_email}")

class UserRegistrationView(CreateView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('planner:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        if user.email:
            run_async(send_welcome_task(user.email))
        return redirect(self.success_url)

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('planner:home')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('planner:home')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)
