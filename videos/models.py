from django.db import models
from django.conf import settings

class Video(models.Model):
    """Video lecture associated with a course"""
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='videos/')  # stores in MEDIA_ROOT/videos/
    order = models.PositiveIntegerField(default=1)
    duration = models.PositiveIntegerField(help_text='Duration in seconds', blank=True, null=True)

    class Meta:
        ordering = ['order']
        unique_together = [('course', 'order')]

    def __str__(self):
        return f"{self.course.title} – {self.title}"

class VideoProgress(models.Model):
    """Tracks how far a student has watched a video"""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_progress')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='progress_records')
    last_position = models.PositiveIntegerField(default=0, help_text='Last watched position in seconds')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('student', 'video')]

    def __str__(self):
        return f"{self.student.username} – {self.video.title} ({self.last_position}s)"
