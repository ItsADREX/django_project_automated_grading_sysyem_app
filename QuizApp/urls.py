from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('add_questions/<int:quiz_id>/', views.add_questions, name='add_questions'),
    path('take_quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz_results/<int:score>/<str:quiz_session>/', views.quiz_results, name='quiz_results'),
    path('instructor_dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('edit_quiz/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('download_pdf/<int:quiz_id>/', views.download_pdf, name='download_pdf'),
    path('quiz_results/<int:quiz_id>/', views.quiz_results, name='quiz_results'),
]

