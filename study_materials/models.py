from django.db import models
from django.conf import settings

class Material(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('ppt', 'PowerPoint'),
        ('note', 'Notes'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_materials')
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPE_CHOICES)
    file = models.FileField(upload_to='materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        unique_together = [('title', 'material_type')]

    def __str__(self):
        return f"{self.title} ({self.get_material_type_display()})"

