"""
API ROUTING LAYER
This file maps URL patterns to API ViewSets.
It defines which URLs trigger which API operations.

BEGINNER TIP: Read this file AFTER api_views.py to understand URL patterns.
"""
from rest_framework.routers import DefaultRouter
from .api_views import NoticeViewSet, AdmissionApplicationViewSet

# API router for public app endpoints
# Creates URLs like: /api/public/notices/, /api/public/admissions/
router = DefaultRouter()
router.register('notices', NoticeViewSet, basename='notice')
router.register('admissions', AdmissionApplicationViewSet, basename='admission')

urlpatterns = router.urls