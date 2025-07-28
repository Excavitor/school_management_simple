from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from public.models import Notice, AdmissionApplication

User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Basic stats for all users
        context['notice_count'] = Notice.objects.filter(is_active=True).count()
        
        # Additional stats for users with permissions
        if user.has_perm('public.view_admissionapplication'):
            context['admission_count'] = AdmissionApplication.objects.count()
        
        # Check user permissions for sidebar
        context['can_view_notices'] = user.has_perm('public.view_notice')
        context['can_view_admissions'] = user.has_perm('public.view_admissionapplication')
        context['can_manage_roles'] = user.is_superuser or user.has_perm('auth.change_user')
        context['can_manage_users'] = user.is_superuser or user.has_perm('auth.view_user')
        
        return context


# Notice Management Views
class NoticeManagementView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Notice
    template_name = 'dashboard/notice_management.html'
    context_object_name = 'notices'
    permission_required = 'public.view_notice'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Notice.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        return queryset


class NoticeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Notice
    template_name = 'dashboard/notice_form.html'
    fields = ['title', 'content', 'is_active']
    permission_required = 'public.add_notice'
    success_url = reverse_lazy('dashboard:notice_management')
    
    def form_valid(self, form):
        messages.success(self.request, 'Notice created successfully!')
        return super().form_valid(form)


class NoticeDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Notice
    template_name = 'dashboard/notice_detail.html'
    permission_required = 'public.view_notice'


class NoticeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Notice
    template_name = 'dashboard/notice_form.html'
    fields = ['title', 'content', 'is_active']
    permission_required = 'public.change_notice'
    success_url = reverse_lazy('dashboard:notice_management')
    
    def form_valid(self, form):
        messages.success(self.request, 'Notice updated successfully!')
        return super().form_valid(form)


class NoticeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Notice
    template_name = 'dashboard/notice_confirm_delete.html'
    permission_required = 'public.delete_notice'
    success_url = reverse_lazy('dashboard:notice_management')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Notice deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Admission Management Views
class AdmissionManagementView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AdmissionApplication
    template_name = 'dashboard/admission_management.html'
    context_object_name = 'applications'
    permission_required = 'public.view_admissionapplication'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = AdmissionApplication.objects.all()
        search = self.request.GET.get('search')
        grade_filter = self.request.GET.get('grade')
        
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) | 
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        if grade_filter:
            queryset = queryset.filter(grade_applying_for=grade_filter)
            
        return queryset


class AdmissionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = AdmissionApplication
    template_name = 'dashboard/admission_form.html'
    fields = [
        'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
        'gender', 'address', 'previous_school', 'grade_applying_for',
        'parent_name', 'parent_phone', 'parent_email'
    ]
    permission_required = 'public.add_admissionapplication'
    success_url = reverse_lazy('dashboard:admission_management')
    
    def form_valid(self, form):
        messages.success(self.request, 'Admission application created successfully!')
        return super().form_valid(form)


class AdmissionDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = AdmissionApplication
    template_name = 'dashboard/admission_detail.html'
    permission_required = 'public.view_admissionapplication'


class AdmissionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = AdmissionApplication
    template_name = 'dashboard/admission_form.html'
    fields = [
        'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
        'gender', 'address', 'previous_school', 'grade_applying_for',
        'parent_name', 'parent_phone', 'parent_email'
    ]
    permission_required = 'public.change_admissionapplication'
    success_url = reverse_lazy('dashboard:admission_management')
    
    def form_valid(self, form):
        messages.success(self.request, 'Admission application updated successfully!')
        return super().form_valid(form)


class AdmissionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = AdmissionApplication
    template_name = 'dashboard/admission_confirm_delete.html'
    permission_required = 'public.delete_admissionapplication'
    success_url = reverse_lazy('dashboard:admission_management')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Admission application deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Role Management Views
class RoleManagementView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/role_management.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm('auth.change_user')):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('dashboard:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['groups'] = Group.objects.all()
        return context


class UserRoleUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/user_role_update.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm('auth.change_user')):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('dashboard:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_obj'] = get_object_or_404(User, pk=kwargs['pk'])
        context['groups'] = Group.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        user_obj = get_object_or_404(User, pk=kwargs['pk'])
        selected_groups = request.POST.getlist('groups')
        
        user_obj.groups.clear()
        for group_id in selected_groups:
            group = get_object_or_404(Group, pk=group_id)
            user_obj.groups.add(group)
        
        messages.success(request, f'Roles updated for {user_obj.email}')
        return redirect('dashboard:role_management')


# User Management Views
class UserManagementView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'dashboard/user_management.html'
    context_object_name = 'users'
    permission_required = 'auth.view_user'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = User.objects.all().prefetch_related('groups')
        search = self.request.GET.get('search')
        role_filter = self.request.GET.get('role')
        
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) | 
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        if role_filter:
            queryset = queryset.filter(groups__id=role_filter)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = User
    template_name = 'dashboard/user_form.html'
    fields = ['email', 'first_name', 'last_name', 'phone', 'is_staff']
    permission_required = 'auth.add_user'
    success_url = reverse_lazy('dashboard:user_management')
    
    def form_valid(self, form):
        # Set a default password for new users
        user = form.save(commit=False)
        user.set_password('defaultpassword123')  # Users should change this
        user.save()
        messages.success(self.request, f'User {user.email} created successfully! Default password: defaultpassword123')
        return super().form_valid(form)


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = User
    template_name = 'dashboard/user_detail.html'
    permission_required = 'auth.view_user'


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    template_name = 'dashboard/user_form.html'
    fields = ['email', 'first_name', 'last_name', 'phone', 'is_staff', 'is_active']
    permission_required = 'auth.change_user'
    success_url = reverse_lazy('dashboard:user_management')
    
    def form_valid(self, form):
        messages.success(self.request, f'User {form.instance.email} updated successfully!')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    template_name = 'dashboard/user_confirm_delete.html'
    permission_required = 'auth.delete_user'
    success_url = reverse_lazy('dashboard:user_management')
    
    def dispatch(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        # Prevent deletion of superusers by non-superusers
        if user_to_delete.is_superuser and not request.user.is_superuser:
            messages.error(request, 'You cannot delete a superuser.')
            return redirect('dashboard:user_management')
        # Prevent self-deletion
        if user_to_delete == request.user:
            messages.error(request, 'You cannot delete your own account.')
            return redirect('dashboard:user_management')
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        user_email = self.get_object().email
        messages.success(request, f'User {user_email} deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Enhanced Role Management Views with CRUD operations
class RoleCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/role_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'Only superadmins can create roles.')
            return redirect('dashboard:role_management')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = Permission.objects.all().select_related('content_type')
        context['form_title'] = 'Create New Role'
        return context
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '').strip()
        permission_ids = request.POST.getlist('permissions')
        
        if not name:
            messages.error(request, 'Role name is required.')
            return self.get(request, *args, **kwargs)
        
        if Group.objects.filter(name=name).exists():
            messages.error(request, 'A role with this name already exists.')
            return self.get(request, *args, **kwargs)
        
        # Create the group
        group = Group.objects.create(name=name)
        
        # Add permissions
        if permission_ids:
            permissions = Permission.objects.filter(id__in=permission_ids)
            group.permissions.set(permissions)
        
        messages.success(request, f'Role "{name}" created successfully!')
        return redirect('dashboard:role_management')


class RoleUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/role_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'Only superadmins can edit roles.')
            return redirect('dashboard:role_management')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = get_object_or_404(Group, pk=kwargs['pk'])
        context['permissions'] = Permission.objects.all().select_related('content_type')
        context['form_title'] = f'Edit Role: {context["group"].name}'
        return context
    
    def post(self, request, *args, **kwargs):
        group = get_object_or_404(Group, pk=kwargs['pk'])
        name = request.POST.get('name', '').strip()
        permission_ids = request.POST.getlist('permissions')
        
        if not name:
            messages.error(request, 'Role name is required.')
            return self.get(request, *args, **kwargs)
        
        # Check if name already exists (excluding current group)
        if Group.objects.filter(name=name).exclude(pk=group.pk).exists():
            messages.error(request, 'A role with this name already exists.')
            return self.get(request, *args, **kwargs)
        
        # Update the group
        group.name = name
        group.save()
        
        # Update permissions
        if permission_ids:
            permissions = Permission.objects.filter(id__in=permission_ids)
            group.permissions.set(permissions)
        else:
            group.permissions.clear()
        
        messages.success(request, f'Role "{name}" updated successfully!')
        return redirect('dashboard:role_management')


class RoleDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/role_confirm_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'Only superadmins can delete roles.')
            return redirect('dashboard:role_management')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = get_object_or_404(Group, pk=kwargs['pk'])
        return context
    
    def post(self, request, *args, **kwargs):
        group = get_object_or_404(Group, pk=kwargs['pk'])
        group_name = group.name
        group.delete()
        messages.success(request, f'Role "{group_name}" deleted successfully!')
        return redirect('dashboard:role_management')
