from django.urls import path
from . import views

app_name = "videos"

urlpatterns = [
    path('<slug:course_slug>/', views.video_list, name='video_list'),
    path('<slug:course_slug>/<int:video_id>/', views.video_detail, name='video_detail'),
]
