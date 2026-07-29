from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('<slug:course_slug>/mark/', views.mark_attendance, name='mark'),
    path('view/', views.view_attendance, name='view'),
    path('<slug:course_slug>/report/<int:year>/<int:month>/', views.monthly_report, name='report'),
]
