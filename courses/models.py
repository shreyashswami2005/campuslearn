from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses_created',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or 'course'
            slug = base
            counter = 1
            while Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField(help_text='Lesson body (plain text or simple HTML).')
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']
        unique_together = [('course', 'order')]

    def __str__(self):
        return f'{self.course.title}: {self.title}'

    def get_absolute_url(self):
        return reverse(
            'courses:lesson',
            kwargs={'slug': self.course.slug, 'lesson_id': self.pk},
        )


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('student', 'course')]
        ordering = ['-enrolled_at']

    def __str__(self):
        return f'{self.student.username} → {self.course.title}'


class Result(models.Model):
    EXAM_QUIZ = 'quiz'
    EXAM_ASSIGNMENT = 'assignment'
    EXAM_MIDTERM = 'midterm'
    EXAM_FINAL = 'final'
    EXAM_OTHER = 'other'
    EXAM_CHOICES = [
        (EXAM_QUIZ, 'Quiz'),
        (EXAM_ASSIGNMENT, 'Assignment'),
        (EXAM_MIDTERM, 'Midterm'),
        (EXAM_FINAL, 'Final'),
        (EXAM_OTHER, 'Other'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='results',
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='results')
    title = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=20, choices=EXAM_CHOICES, default=EXAM_OTHER)
    marks_obtained = models.DecimalField(max_digits=7, decimal_places=2)
    max_marks = models.DecimalField(max_digits=7, decimal_places=2, default=100)
    grade = models.CharField(max_length=10, blank=True)
    remarks = models.CharField(max_length=255, blank=True)
    exam_date = models.DateField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-exam_date', '-recorded_at']

    def __str__(self):
        return f'{self.student.username} — {self.title} ({self.course.title})'

    @property
    def percentage(self):
        if not self.max_marks:
            return None
        return round((float(self.marks_obtained) / float(self.max_marks)) * 100, 1)


class Attendance(models.Model):
    STATUS_PRESENT = 'present'
    STATUS_ABSENT = 'absent'
    STATUS_LATE = 'late'
    STATUS_EXCUSED = 'excused'
    STATUS_CHOICES = [
        (STATUS_PRESENT, 'Present'),
        (STATUS_ABSENT, 'Absent'),
        (STATUS_LATE, 'Late'),
        (STATUS_EXCUSED, 'Excused'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendance_records',
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PRESENT)
    remarks = models.CharField(max_length=255, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-id']
        unique_together = [('student', 'course', 'date')]

    def __str__(self):
        return f'{self.student.username} — {self.course.title} ({self.date}: {self.status})'
