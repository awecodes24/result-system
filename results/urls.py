from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='results/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Core
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('students/<int:pk>/delete/', views.delete_student, name='delete_student'),
    path('students/<int:pk>/report/', views.student_report, name='student_report'),
    path('students/<int:pk>/export/', views.export_csv, name='export_csv'),

    # Results
    path('results/add/', views.add_result, name='add_result'),
    path('results/search/', views.search_result, name='search_result'),
    path('logout-confirm/', TemplateView.as_view(template_name='results/logout.html'), name='logout_confirm'),
]
