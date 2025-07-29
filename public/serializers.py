"""
API DATA FORMAT LAYER
This file defines how model data is converted to/from JSON for API responses.
Think of serializers as translators between Python objects and JSON data.

BEGINNER TIP: Read this file AFTER models.py to understand how data is formatted for APIs.
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


class NoticeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notice
        fields = "__all__"
