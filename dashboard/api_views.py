from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.db.models import Q
from public.models import Notice, AdmissionApplication
from .serializers import (
    DashboardStatsSerializer, UserManagementSerializer, 
    GroupManagementSerializer, PermissionSerializer
)

User = get_user_model()


class DashboardStatsAPIView(APIView):
    """API view for dashboard statistics - replaces direct template context data"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get dashboard statistics for authenticated user"""
        user = request.user
        
        # Basic stats for all users
        stats_data = {
            'notice_count': Notice.objects.filter(is_active=True).count(),
            'user_groups_count': user.groups.count()
        }
        
        # Additional stats for users with permissions
        if user.has_perm('public.view_admissionapplication'):
            stats_data['admission_count'] = AdmissionApplication.objects.count()
        
        serializer = DashboardStatsSerializer(stats_data)
        return Response(serializer.data)


class UserPermissionsAPIView(APIView):
    """API view for user permissions - replaces template permission checks"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get user permissions for frontend navigation"""
        user = request.user
        
        permissions_data = {
            'can_view_notices': user.has_perm('public.view_notice'),
            'can_add_notices': user.has_perm('public.add_notice'),
            'can_change_notices': user.has_perm('public.change_notice'),
            'can_delete_notices': user.has_perm('public.delete_notice'),
            'can_view_admissions': user.has_perm('public.view_admissionapplication'),
            'can_add_admissions': user.has_perm('public.add_admissionapplication'),
            'can_change_admissions': user.has_perm('public.change_admissionapplication'),
            'can_delete_admissions': user.has_perm('public.delete_admissionapplication'),
            'can_manage_roles': (
                user.has_perm('auth.view_group') or 
                user.has_perm('auth.add_group') or 
                user.has_perm('auth.change_group') or 
                user.has_perm('auth.delete_group')
            ),
            'can_manage_users': (
                user.has_perm('accounts.view_user') or 
                user.has_perm('accounts.add_user') or 
                user.has_perm('accounts.change_user') or 
                user.has_perm('accounts.delete_user')
            )
        }
        
        return Response(permissions_data)


class UserManagementViewSet(viewsets.ModelViewSet):
    """API ViewSet for user management - replaces direct model access in dashboard"""
    queryset = User.objects.all()
    serializer_class = UserManagementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter users based on search and role parameters"""
        queryset = User.objects.all().prefetch_related('groups')
        
        search = self.request.query_params.get('search', None)
        role_filter = self.request.query_params.get('role', None)
        
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) | 
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        if role_filter:
            queryset = queryset.filter(groups__id=role_filter)
            
        return queryset.order_by('email')
    
    @action(detail=True, methods=['post'])
    def update_roles(self, request, pk=None):
        """Update user roles - replaces form-based role assignment"""
        user = self.get_object()
        group_ids = request.data.get('groups', [])
        
        # Clear existing groups and add new ones
        user.groups.clear()
        if group_ids:
            groups = Group.objects.filter(id__in=group_ids)
            user.groups.set(groups)
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class GroupManagementViewSet(viewsets.ModelViewSet):
    """API ViewSet for role/group management - replaces direct model access"""
    queryset = Group.objects.all()
    serializer_class = GroupManagementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return all groups with related data"""
        return Group.objects.all().prefetch_related('permissions', 'user_set')


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for permissions - used in role management"""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return permissions organized by content type"""
        return Permission.objects.all().select_related('content_type').order_by('content_type__name', 'name')