from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('', views.material_list, name='list'),
    path('upload/', views.material_upload, name='upload'),
    path('<int:pk>/download/', views.material_download, name='download'),
]
