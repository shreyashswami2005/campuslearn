from django.db import models
from django.conf import settings

class Attendance(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.course.title} on {self.date}"

class CourseProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    completed_modules = models.PositiveIntegerField(default=0)
    total_modules = models.PositiveIntegerField()

    @property
    def progress_percent(self):
        return 0 if self.total_modules == 0 else int((self.completed_modules / self.total_modules) * 100)

    def __str__(self):
        return f"{self.student.username} - {self.course.title} progress"

class Mark(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    assignment = models.ForeignKey('assignments.Assignment', null=True, blank=True, on_delete=models.SET_NULL)
    quiz = models.ForeignKey('quizzes.Quiz', null=True, blank=True, on_delete=models.SET_NULL)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)

    @property
    def percent(self):
        return 0 if self.max_score == 0 else int((self.score / self.max_score) * 100)

    def __str__(self):
        return f"{self.student.username} - {self.course.title} mark"
