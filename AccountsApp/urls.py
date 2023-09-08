from django.urls import path
from . import views

app_name = 'AccountsApp'

urlpatterns = [
    path('register_student/', views.register_student, name='register_student'),
    path('register_instructor/', views.register_instructor, name='register_instructor'),
    path('login_student/', views.login_student, name='login_student'),
    path('login_instructor/', views.login_instructor, name='login_instructor'),
]
