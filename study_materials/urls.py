from django.urls import path
from . import views

app_name = 'study_materials'

urlpatterns = [
    path('', views.material_list, name='material_list'),
    path('upload/', views.material_upload, name='material_upload'),
    path('download/<int:pk>/', views.material_download, name='material_download'),
]
