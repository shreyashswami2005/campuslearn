from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render
from courses.models import Course

def staff_user(user):
    return user.is_staff

@user_passes_test(staff_user)
@login_required
def dashboard(request):
    total_students = User.objects.filter(is_staff=False).count()
    total_courses = Course.objects.count()
    # Placeholder values – will be replaced with real queries when those apps exist
    pending_assignments = 0
    recent_activities = []
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'pending_assignments': pending_assignments,
        'recent_activities': recent_activities,
    }
    return render(request, 'teacher/dashboard.html', context)
