from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import User


class LoginView(BaseLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard:dashboard')


class RegisterView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    fields = ['email', 'password', 'first_name', 'last_name', 'phone']
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, 'Registration successful! Please log in.')
        return super().form_valid(form)
