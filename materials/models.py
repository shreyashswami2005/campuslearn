from django.db import models
from django.conf import settings

class Material(models.Model):
    """Study material associated with a course"""
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='materials/')  # stored under MEDIA_ROOT/materials/
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} – {self.title}"
