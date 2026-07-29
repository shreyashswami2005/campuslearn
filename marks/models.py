from django.conf import settings
from django.db import models
from django.utils import timezone

class Component(models.Model):
    """Component of evaluation (e.g., Assignment, Quiz, Midterm, Final)."""
    name = models.CharField(max_length=50, unique=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text='Weight as percentage of final grade')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.weight}%)"

class InternalMark(models.Model):
    """Marks entered by teachers for a specific component of a course."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='internal_marks')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='internal_marks')
    component = models.ForeignKey(Component, on_delete=models.PROTECT, related_name='marks')
    score = models.DecimalField(max_digits=7, decimal_places=2, help_text='Score obtained')
    max_score = models.DecimalField(max_digits=7, decimal_places=2, default=100, help_text='Maximum possible score')
    date_recorded = models.DateField(default=timezone.now)

    class Meta:
        unique_together = [('student', 'course', 'component')]
        ordering = ['-date_recorded']

    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {self.component.name}: {self.score}/{self.max_score}"
