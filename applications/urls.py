from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('apply/<int:pk>/', views.apply_job, name='apply_job'),
    path('status/<int:pk>/<str:status>/', views.update_application_status, name='update_status'),
    path('save/<int:pk>/', views.toggle_save_job, name='toggle_save_job'),
]