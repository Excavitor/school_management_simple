from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from public.models import Notice, AdmissionApplication

User = get_user_model()


class DashboardStatsSerializer(serializers.Serializer):
    notice_count = serializers.IntegerField()
    admission_count = serializers.IntegerField(required=False)
    user_groups_count = serializers.IntegerField()


class UserManagementSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True, read_only=True)
    groups_list = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'phone', 
            'is_staff', 'is_active', 'groups', 'groups_list', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def get_groups_list(self, obj):
        return list(obj.groups.values_list('id', flat=True))


class GroupManagementSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Permission.objects.all(),
        required=False
    )
    permissions_list = serializers.SerializerMethodField()
    user_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions', 'permissions_list', 'user_count']
    
    def get_permissions_list(self, obj):
        return [
            {
                'id': perm.id,
                'name': perm.name,
                'codename': perm.codename,
                'content_type': perm.content_type.name
            }
            for perm in obj.permissions.all()
        ]
    
    def get_user_count(self, obj):
        return obj.user_set.count()


class PermissionSerializer(serializers.ModelSerializer):
    content_type_name = serializers.CharField(source='content_type.name', read_only=True)
    
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type', 'content_type_name']