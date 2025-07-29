from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import User
from .forms import CustomUserRegistrationForm


class LoginView(BaseLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard:dashboard')


class RegisterView(CreateView):
    model = User
    form_class = CustomUserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Registration successful! Please log in.')
        return super().form_valid(form)
