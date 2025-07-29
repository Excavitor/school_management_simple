from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Notice, AdmissionApplication
from .utils import apply_search_filter, NOTICE_SEARCH_FIELDS


class HomeView(TemplateView):
    template_name = 'public/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NoticeListView(ListView):
    model = Notice
    template_name = 'public/notice_list.html'
    context_object_name = 'notices'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Notice.objects.filter(is_active=True)
        search = self.request.GET.get('search')
        return apply_search_filter(queryset, search, NOTICE_SEARCH_FIELDS)


class AdmissionFormView(CreateView):
    model = AdmissionApplication
    template_name = 'public/admission_form.html'
    fields = [
        'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
        'gender', 'address', 'previous_school', 'grade_applying_for',
        'parent_name', 'parent_phone', 'parent_email'
    ]
    success_url = reverse_lazy('public:admission_success')
    
    def form_valid(self, form):
        messages.success(self.request, 'Your admission application has been submitted successfully!')
        return super().form_valid(form)


class AdmissionSuccessView(TemplateView):
    template_name = 'public/admission_success.html'
