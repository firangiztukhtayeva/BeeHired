from django.urls import path
from .views import register_view, login_view, logout_view
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', views.profile_dashboard, name='dashboard'),
    path('resume/edit/', views.edit_resume, name='edit_resume'),
]