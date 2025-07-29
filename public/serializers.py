"""
Serializers for converting model data to/from JSON for API responses.
"""

from rest_framework import serializers
from .models import Notice, AdmissionApplication


class NoticeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notice
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class AdmissionApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdmissionApplication
        fields = "__all__"
        read_only_fields = ["id", "created_at"]



