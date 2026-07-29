from django.urls import path
from . import views

app_name = 'assignments'

urlpatterns = [
    path('', views.AssignmentListView.as_view(), name='list'),
    path('<int:pk>/', views.AssignmentDetailView.as_view(), name='detail'),
    path('create/', views.AssignmentCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.AssignmentUpdateView.as_view(), name='edit'),
    path('<int:pk>/review/', views.submission_review, name='review'),
    path('<int:pk>/submit/', views.submit_assignment, name='submit'),
]
