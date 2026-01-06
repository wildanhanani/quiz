from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('quiz/<int:category_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    path('history/', views.history, name='history'),
]
