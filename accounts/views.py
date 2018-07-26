from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.urls import reverse_lazy
from django.conf import settings
from django.views import generic

from . import forms
from . import models


class RegistrationView(generic.CreateView):
    model = models.User
    form_class = forms.UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('chat:messages')

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        response = super().form_valid(form)
        messages.success(self.request, 'Successfully Registered. Please login!')
        return response