from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),  # Головна сторінка
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='quiz/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/add_question/', views.add_question, name='add_question'),
    
    # НОВІ МАРШРУТИ
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('result/<int:result_id>/', views.quiz_result, name='quiz_result'),
    path('quiz/<int:quiz_id>/leaderboard/', views.leaderboard, name='leaderboard'),
    path('quiz/<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    path('quiz/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),
]