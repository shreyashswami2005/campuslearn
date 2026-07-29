from django.urls import path
from . import views

app_name = "teacher"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
