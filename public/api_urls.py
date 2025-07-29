"""
API URL routing for public app endpoints.
"""
from rest_framework.routers import DefaultRouter
from .api_views import NoticeViewSet, AdmissionApplicationViewSet

# API router for public app endpoints
# Creates URLs like: /api/public/notices/, /api/public/admissions/
router = DefaultRouter()
router.register('notices', NoticeViewSet, basename='notice')
router.register('admissions', AdmissionApplicationViewSet, basename='admission')

urlpatterns = router.urls