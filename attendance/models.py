from django.db import models
from django.conf import settings
from courses.models import Course

class Attendance(models.Model):
    """Attendance record for a student in a specific course on a given date."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('course', 'student', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {self.date} - {'Present' if self.present else 'Absent'}"
