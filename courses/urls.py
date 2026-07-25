from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='list'),
    path('courses/<slug:slug>/', views.course_detail, name='detail'),
    path('courses/<slug:slug>/enroll/', views.enroll, name='enroll'),
    path('courses/<slug:slug>/lessons/<int:lesson_id>/', views.lesson_detail, name='lesson'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('my-results/', views.my_results, name='my_results'),
    path('my-attendance/', views.my_attendance, name='my_attendance'),
]
