from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api_views import (
    DashboardStatsAPIView,
    UserPermissionsAPIView,
    UserManagementViewSet,
    GroupManagementViewSet,
    PermissionViewSet,
)

# API router for dashboard endpoints
router = DefaultRouter()
router.register("users", UserManagementViewSet, basename="user")
router.register("groups", GroupManagementViewSet, basename="group")
router.register("permissions", PermissionViewSet, basename="permission")

urlpatterns = [
    path("stats/", DashboardStatsAPIView.as_view(), name="dashboard-stats"),
    path("permissions/", UserPermissionsAPIView.as_view(), name="user-permissions"),
    path("", include(router.urls)),
]
