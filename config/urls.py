from django.contrib import admin
from django.urls import include, path
from django.conf import settings
import django.views.static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False), name='root'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('teacher/', include('teacher.urls')),
    path('assignments/', include('assignments.urls')),
    path('courses/', include('courses.urls')),
    path('quizzes/', include('quizzes.urls')),
    path('videos/', include('videos.urls')),
    # Media files in development
    path('media/<path:path>', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),
]
