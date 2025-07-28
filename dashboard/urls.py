from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('notices/', views.NoticeManagementView.as_view(), name='notice_management'),
    path('notices/create/', views.NoticeCreateView.as_view(), name='notice_create'),
    path('notices/<int:pk>/', views.NoticeDetailView.as_view(), name='notice_detail'),
    path('notices/<int:pk>/edit/', views.NoticeUpdateView.as_view(), name='notice_update'),
    path('notices/<int:pk>/delete/', views.NoticeDeleteView.as_view(), name='notice_delete'),
    
    path('admissions/', views.AdmissionManagementView.as_view(), name='admission_management'),
    path('admissions/create/', views.AdmissionCreateView.as_view(), name='admission_create'),
    path('admissions/<int:pk>/', views.AdmissionDetailView.as_view(), name='admission_detail'),
    path('admissions/<int:pk>/edit/', views.AdmissionUpdateView.as_view(), name='admission_update'),
    path('admissions/<int:pk>/delete/', views.AdmissionDeleteView.as_view(), name='admission_delete'),
    
    path('users/', views.UserManagementView.as_view(), name='user_management'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    
    path('roles/', views.RoleManagementView.as_view(), name='role_management'),
    path('roles/create/', views.RoleCreateView.as_view(), name='role_create'),
    path('roles/<int:pk>/edit/', views.RoleUpdateView.as_view(), name='role_update'),
    path('roles/<int:pk>/delete/', views.RoleDeleteView.as_view(), name='role_delete'),
    path('roles/users/<int:pk>/', views.UserRoleUpdateView.as_view(), name='user_role_update'),
]