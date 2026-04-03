from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from .forms import ContactForm

class ContactView(FormView):
    template_name = 'common/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('common:contact_success')

    def form_valid(self, form):
        # In a real app, you might send an email here.
        # For now, just proceed to success page.
        return super().form_valid(form)

class ContactSuccessView(TemplateView):
    template_name = 'common/contact_success.html'

class AboutView(TemplateView):
    template_name = 'common/about.html'
