from django.urls import path
from . import views

app_name = 'public'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('notices/', views.NoticeListView.as_view(), name='notice_list'),
    path('admission/', views.AdmissionFormView.as_view(), name='admission_form'),
    path('admission/success/', views.AdmissionSuccessView.as_view(), name='admission_success'),
]