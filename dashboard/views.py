from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Attendance, CourseProgress, Mark
from courses.models import Course

@login_required
def student_dashboard(request):
    student = request.user
    courses = Course.objects.filter(enrollments__student=student)
    attendance = []
    progress = []
    marks = []
    for course in courses:
        total_sessions = Attendance.objects.filter(student=student, course=course).count()
        present_sessions = Attendance.objects.filter(student=student, course=course, present=True).count()
        attendance.append({"course": course, "percent": int(present_sessions / total_sessions * 100) if total_sessions else 0})
        prog = CourseProgress.objects.filter(student=student, course=course).first()
        progress.append({"course": course, "percent": prog.progress_percent if prog else 0})
        qs = Mark.objects.filter(student=student, course=course)
        if qs.exists():
            avg_score = sum(m.score for m in qs) / qs.count()
            avg_max = sum(m.max_score for m in qs) / qs.count()
            percent = int((avg_score / avg_max) * 100) if avg_max else 0
        else:
            percent = 0
        marks.append({"course": course, "percent": percent})
    return render(request, "dashboard/student_dashboard.html", {
        "attendance": attendance,
        "progress": progress,
        "marks": marks,
    })
