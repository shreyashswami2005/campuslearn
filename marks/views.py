from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import InternalMarkForm
from .models import InternalMark, Component
from courses.models import Course

@login_required
def upload_marks(request, course_slug):
    """Teacher uploads internal marks for a given course.
    Only staff users (or a custom Teacher group) are allowed.
    """
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to upload marks.")
    course = get_object_or_404(Course, slug=course_slug)
    if request.method == "POST":
        form = InternalMarkForm(request.POST)
        if form.is_valid():
            mark = form.save(commit=False)
            mark.course = course
            mark.save()
            return redirect('marks:my_marks')
    else:
        form = InternalMarkForm()
    return render(request, 'marks/upload.html', {'form': form, 'course': course})

@login_required
def my_marks(request):
    """Student view of their internal marks across courses."""
    marks = InternalMark.objects.filter(student=request.user).select_related('course', 'component')
    return render(request, 'marks/view.html', {'marks': marks})
