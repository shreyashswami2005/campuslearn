from django.shortcuts import render
from django.contrib.auth import get_user_model
from courses.models import Course
from assignments.models import Assignment
from quizzes.models import Quiz
from django.db.models import Count

def dashboard(request):
    """Teacher dashboard with basic analytics.
    Shows total counts and simple Chart.js data placeholders.
    """
    total_students = get_user_model().objects.filter(is_staff=False).count()
    total_courses = Course.objects.count()
    total_assignments = Assignment.objects.count()
    total_quizzes = Quiz.objects.count()
    # Example data for Chart.js (e.g., enrollments per month)
    chart_data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'data': [12, 19, 8, 15, 10, 22],
    }
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_assignments': total_assignments,
        'total_quizzes': total_quizzes,
        'chart_data': chart_data,
    }
    return render(request, 'teacher_dashboard/dashboard.html', context)
