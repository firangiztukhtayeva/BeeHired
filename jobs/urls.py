from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('list/', views.job_list, name='job_list'),
    path('create/', views.job_create, name='job_create'),
    path('company/edit/', views.company_edit, name='company_edit'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
]