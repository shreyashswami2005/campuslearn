from django.conf import settings
from django.db import models


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    phone = models.CharField(max_length=20, blank=True)
    college = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=120, blank=True, help_text='e.g. Computer Science')
    year_of_study = models.CharField(
        max_length=40,
        blank=True,
        help_text='e.g. 1st Year, 2nd Year',
    )
    student_id = models.CharField(max_length=50, blank=True, verbose_name='Student ID')
    bio = models.TextField(blank=True, max_length=500)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profile: {self.user.username}'

    @property
    def display_name(self):
        full = self.user.get_full_name().strip()
        return full or self.user.username
