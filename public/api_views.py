from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notice, AdmissionApplication
from .serializers import NoticeSerializer, AdmissionApplicationSerializer
from .utils import apply_search_filter, check_api_permission, NOTICE_SEARCH_FIELDS, ADMISSION_SEARCH_FIELDS


class NoticeViewSet(viewsets.ModelViewSet):
    serializer_class = NoticeSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Notice.objects.all()
        
        if not self.request.user.is_authenticated or not self.request.user.has_perm('public.view_notice'):
            queryset = queryset.filter(is_active=True)
            
        search = self.request.query_params.get('search', None)
        queryset = apply_search_filter(queryset, search, NOTICE_SEARCH_FIELDS)
        
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        return NoticeSerializer
    
    def create(self, request, *args, **kwargs):
        """Create notice - requires add_notice permission"""
        permission_check = check_api_permission(request.user, 'public.add_notice')
        if permission_check:
            return permission_check
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Update notice - requires change_notice permission"""
        permission_check = check_api_permission(request.user, 'public.change_notice')
        if permission_check:
            return permission_check
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Partial update notice - requires change_notice permission"""
        permission_check = check_api_permission(request.user, 'public.change_notice')
        if permission_check:
            return permission_check
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Delete notice - requires delete_notice permission"""
        permission_check = check_api_permission(request.user, 'public.delete_notice')
        if permission_check:
            return permission_check
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_notices = Notice.objects.filter(is_active=True)[:3]
        serializer = NoticeSerializer(recent_notices, many=True)
        return Response(serializer.data)


class AdmissionApplicationViewSet(viewsets.ModelViewSet):
    queryset = AdmissionApplication.objects.all()
    serializer_class = AdmissionApplicationSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = AdmissionApplication.objects.all()
        
        search = self.request.query_params.get('search', None)
        grade_filter = self.request.query_params.get('grade', None)
        
        queryset = apply_search_filter(queryset, search, ADMISSION_SEARCH_FIELDS)
        
        if grade_filter and grade_filter != '':
            queryset = queryset.filter(grade_applying_for=grade_filter)
            
        return queryset.order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        """List admissions - requires view_admissionapplication permission"""
        permission_check = check_api_permission(request.user, 'public.view_admissionapplication')
        if permission_check:
            return permission_check
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve admission - requires view_admissionapplication permission"""
        permission_check = check_api_permission(request.user, 'public.view_admissionapplication')
        if permission_check:
            return permission_check
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Update admission - requires change_admissionapplication permission"""
        permission_check = check_api_permission(request.user, 'public.change_admissionapplication')
        if permission_check:
            return permission_check
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Partial update admission - requires change_admissionapplication permission"""
        permission_check = check_api_permission(request.user, 'public.change_admissionapplication')
        if permission_check:
            return permission_check
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Delete admission - requires delete_admissionapplication permission"""
        permission_check = check_api_permission(request.user, 'public.delete_admissionapplication')
        if permission_check:
            return permission_check
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save()