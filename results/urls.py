from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='results/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Core
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_result, name='add_student'),
    path('students//edit/', views.edit_student, name='edit_student'),
    path('students//delete/', views.delete_student, name='delete_student'),
    path('students//report/', views.student_report, name='student_report'),
    
    # Results
    path('results/add/', views.add_result, name='add_result'),
    path('results/search/', views.search_result, name='search_result'),
]
