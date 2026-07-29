from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Assignment, Submission
from .forms import AssignmentForm, SubmissionForm, SubmissionReviewForm

# Simple teacher check – customize as needed
def is_teacher(user):
    return user.is_staff

@method_decorator(login_required, name='dispatch')
class AssignmentListView(ListView):
    model = Assignment
    template_name = 'assignments/list.html'
    context_object_name = 'assignments'

@method_decorator(login_required, name='dispatch')
class AssignmentDetailView(DetailView):
    model = Assignment
    template_name = 'assignments/detail.html'
    context_object_name = 'assignment'

@login_required
@user_passes_test(is_teacher)
def submission_review(request, pk):
    """Teacher reviews a student's submission, assigns grade and feedback."""
    submission = get_object_or_404(Submission, pk=pk)
    if request.method == 'POST':
        form = SubmissionReviewForm(request.POST)
        if form.is_valid():
            submission.grade = form.cleaned_data['grade']
            submission.feedback = form.cleaned_data['feedback']
            submission.save()
            return redirect('assignments:detail', pk=submission.assignment.id)
    else:
        form = SubmissionReviewForm(instance=submission)
    return render(request, 'assignments/review.html', {'form': form, 'submission': submission})

@method_decorator([login_required, user_passes_test(is_teacher)], name='dispatch')
class AssignmentCreateView(CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/form.html'
    success_url = reverse_lazy('assignments:list')

@method_decorator([login_required, user_passes_test(is_teacher)], name='dispatch')
class AssignmentUpdateView(UpdateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/form.html'
    success_url = reverse_lazy('assignments:list')

@method_decorator([login_required, user_passes_test(is_teacher)], name='dispatch')
class AssignmentDeleteView(DeleteView):
    model = Assignment
    template_name = 'assignments/confirm_delete.html'
    success_url = reverse_lazy('assignments:list')

@login_required
def submit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission_file = form.cleaned_data['file']
            import os
            from django.conf import settings
            sub_dir = os.path.join('submissions', str(assignment.id))
            full_dir = os.path.join(settings.MEDIA_ROOT, sub_dir)
            os.makedirs(full_dir, exist_ok=True)
            file_path = os.path.join(full_dir, submission_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in submission_file.chunks():
                    destination.write(chunk)
            return redirect('assignments:detail', pk=assignment.id)
    else:
        form = SubmissionForm()
    return render(request, 'assignments/submit.html', {'form': form, 'assignment': assignment})
