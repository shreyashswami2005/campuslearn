from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import Attendance
from .forms import AttendanceForm
from courses.models import Course, Enrollment

# Simple teacher check – can be refined
def is_teacher(user):
    return user.is_staff

@login_required
@user_passes_test(is_teacher)
def mark_attendance(request, course_slug):
    """Teacher marks attendance for all students in a course on a selected date."""
    course = get_object_or_404(Course, slug=course_slug)
    if request.method == 'POST':
        date_str = request.POST.get('date')
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        for enrollment in course.enrollments.all():
            present = request.POST.get(f'present_{enrollment.student.id}') == 'on'
            Attendance.objects.update_or_create(
                course=course,
                student=enrollment.student,
                date=date,
                defaults={'present': present}
            )
        return redirect('attendance:mark', course_slug=course.slug)
    else:
        # Default to today
        today = timezone.now().date()
        # Prepare existing records for today if any
        existing = {a.student.id: a.present for a in Attendance.objects.filter(course=course, date=today)}
        enrollments = course.enrollments.select_related('student').all()
        return render(request, 'attendance/mark.html', {
            'course': course,
            'date': today,
            'enrollments': enrollments,
            'existing': existing,
        })

@login_required
def view_attendance(request):
    """Student views their own attendance records across all courses."""
    records = Attendance.objects.filter(student=request.user).select_related('course').order_by('-date')
    return render(request, 'attendance/view.html', {'records': records})

@login_required
@user_passes_test(is_teacher)
def monthly_report(request, course_slug, year, month):
    """Generate a simple monthly attendance report for a course."""
    course = get_object_or_404(Course, slug=course_slug)
    records = Attendance.objects.filter(course=course, date__year=year, date__month=month)
    # Aggregate per student
    summary = {}
    for rec in records:
        summary.setdefault(rec.student.username, {'present': 0, 'total': 0})
        summary[rec.student.username]['total'] += 1
        if rec.present:
            summary[rec.student.username]['present'] += 1
    return render(request, 'attendance/report.html', {
        'course': course,
        'year': year,
        'month': month,
        'summary': summary,
    })
