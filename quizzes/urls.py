from django.urls import path
from . import views

app_name = "quizzes"

urlpatterns = [
    path('<slug:course_slug>/', views.quiz_list, name='quiz_list'),
    path('<slug:course_slug>/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('<slug:course_slug>/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
]
