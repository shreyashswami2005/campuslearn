from django.urls import path
from . import views

app_name = 'marks'

urlpatterns = [
    path('<slug:course_slug>/upload/', views.upload_marks, name='upload'),
    path('my/', views.my_marks, name='my_marks'),
]
