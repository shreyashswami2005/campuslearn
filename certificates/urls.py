from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('<slug:course_slug>/generate/<int:student_id>/', views.generate_certificate, name='generate'),
    path('download/<int:cert_id>/', views.download_certificate, name='download'),
    path('verify/<int:cert_id>/', views.verify_certificate, name='verify'),
]
