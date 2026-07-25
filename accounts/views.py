from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import CreateView

from courses.models import Attendance, Enrollment, Result

from .forms import ProfileForm
from .models import StudentProfile


def get_or_create_profile(user):
    profile, _ = StudentProfile.objects.get_or_create(user=user)
    return profile


@method_decorator(never_cache, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


@method_decorator(never_cache, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('courses:home')


@login_required
def dashboard(request):
    profile = get_or_create_profile(request.user)
    enrollments = (
        Enrollment.objects.filter(student=request.user)
        .select_related('course')
        .order_by('-enrolled_at')[:6]
    )
    enrollment_count = Enrollment.objects.filter(student=request.user).count()
    recent_results = (
        Result.objects.filter(student=request.user)
        .select_related('course')
        .order_by('-exam_date', '-recorded_at')[:5]
    )
    result_count = Result.objects.filter(student=request.user).count()
    recent_attendance = (
        Attendance.objects.filter(student=request.user)
        .select_related('course')
        .order_by('-date', '-id')[:5]
    )
    attendance_qs = Attendance.objects.filter(student=request.user)
    attendance_total = attendance_qs.count()
    attendance_present = attendance_qs.filter(
        status__in=[Attendance.STATUS_PRESENT, Attendance.STATUS_LATE]
    ).count()
    attendance_percent = (
        round((attendance_present / attendance_total) * 100, 1) if attendance_total else None
    )
    return render(
        request,
        'accounts/dashboard.html',
        {
            'profile': profile,
            'enrollments': enrollments,
            'enrollment_count': enrollment_count,
            'recent_results': recent_results,
            'result_count': result_count,
            'recent_attendance': recent_attendance,
            'attendance_percent': attendance_percent,
        },
    )

@login_required
@never_cache
def edit_profile(request):
    profile = get_or_create_profile(request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:dashboard')
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form, 'profile': profile})


def csrf_failure(request, reason=''):
    """Recover from stale CSRF (e.g. login in another tab) with a refresh prompt."""
    messages.warning(
        request,
        'Your form expired for security. Please try again.',
    )
    referer = request.META.get('HTTP_REFERER', '')
    if '/accounts/login' in referer:
        return redirect('accounts:login')
    if '/accounts/register' in referer:
        return redirect('accounts:register')
    if request.path.startswith('/accounts/login'):
        return redirect('accounts:login')
    if request.path.startswith('/accounts/register'):
        return redirect('accounts:register')
    return redirect(reverse('courses:home'))
