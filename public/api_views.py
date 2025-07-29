from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Notice, AdmissionApplication
from .serializers import NoticeSerializer, NoticeListSerializer, AdmissionApplicationSerializer


class NoticeViewSet(viewsets.ModelViewSet):
    serializer_class = NoticeSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Notice.objects.all()
        
        if not self.request.user.is_authenticated or not self.request.user.has_perm('public.view_notice'):
            queryset = queryset.filter(is_active=True)
            
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NoticeListSerializer
        return NoticeSerializer
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_notices = Notice.objects.filter(is_active=True)[:3]
        serializer = NoticeListSerializer(recent_notices, many=True)
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
        
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) | 
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        if grade_filter:
            queryset = queryset.filter(grade_applying_for=grade_filter)
            
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save()