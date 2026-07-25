from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Attendance, Course, Enrollment, Lesson, Result


def home(request):
    courses = Course.objects.filter(is_published=True)[:6]
    return render(request, 'courses/home.html', {'courses': courses})


def course_list(request):
    courses = Course.objects.filter(is_published=True)
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    if q:
        courses = courses.filter(
            Q(title__icontains=q) | Q(description__icontains=q) | Q(category__icontains=q)
        )
    if category:
        courses = courses.filter(category__iexact=category)

    categories = (
        Course.objects.filter(is_published=True)
        .exclude(category='')
        .values_list('category', flat=True)
        .distinct()
        .order_by('category')
    )

    return render(
        request,
        'courses/course_list.html',
        {
            'courses': courses,
            'categories': categories,
            'q': q,
            'selected_category': category,
        },
    )


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lessons = course.lessons.all()
    enrolled = False
    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    return render(
        request,
        'courses/course_detail.html',
        {
            'course': course,
            'lessons': lessons,
            'enrolled': enrolled,
        },
    )


@login_required
@require_POST
def enroll(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    _, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    if created:
        messages.success(request, f'You enrolled in “{course.title}”.')
    else:
        messages.info(request, f'You are already enrolled in “{course.title}”.')
    return redirect('courses:detail', slug=course.slug)


@login_required
def my_courses(request):
    enrollments = (
        Enrollment.objects.filter(student=request.user)
        .select_related('course')
        .order_by('-enrolled_at')
    )
    return render(request, 'courses/my_courses.html', {'enrollments': enrollments})


@login_required
def my_results(request):
    results = (
        Result.objects.filter(student=request.user)
        .select_related('course')
        .order_by('-exam_date', '-recorded_at')
    )
    course_slug = request.GET.get('course', '').strip()
    if course_slug:
        results = results.filter(course__slug=course_slug)

    courses = (
        Course.objects.filter(results__student=request.user)
        .distinct()
        .order_by('title')
    )
    return render(
        request,
        'courses/my_results.html',
        {
            'results': results,
            'courses': courses,
            'selected_course': course_slug,
        },
    )


@login_required
def my_attendance(request):
    records = (
        Attendance.objects.filter(student=request.user)
        .select_related('course')
        .order_by('-date', '-id')
    )
    course_slug = request.GET.get('course', '').strip()
    if course_slug:
        records = records.filter(course__slug=course_slug)

    summary = (
        Attendance.objects.filter(student=request.user)
        .values('status')
        .annotate(total=Count('id'))
    )
    counts = {row['status']: row['total'] for row in summary}
    total = sum(counts.values())
    present_like = counts.get(Attendance.STATUS_PRESENT, 0) + counts.get(
        Attendance.STATUS_LATE, 0
    )
    attendance_percent = round((present_like / total) * 100, 1) if total else None

    by_course = []
    course_qs = Course.objects.filter(attendance_records__student=request.user).distinct()
    for course in course_qs.order_by('title'):
        course_records = Attendance.objects.filter(student=request.user, course=course)
        course_total = course_records.count()
        course_present = course_records.filter(
            status__in=[Attendance.STATUS_PRESENT, Attendance.STATUS_LATE]
        ).count()
        by_course.append(
            {
                'course': course,
                'total': course_total,
                'present': course_present,
                'percent': round((course_present / course_total) * 100, 1) if course_total else 0,
            }
        )

    courses = course_qs.order_by('title')
    return render(
        request,
        'courses/my_attendance.html',
        {
            'records': records,
            'courses': courses,
            'selected_course': course_slug,
            'counts': counts,
            'total_records': total,
            'attendance_percent': attendance_percent,
            'by_course': by_course,
        },
    )


@login_required
def lesson_detail(request, slug, lesson_id):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lesson = get_object_or_404(Lesson, pk=lesson_id, course=course)

    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    if not is_enrolled and not request.user.is_staff:
        messages.warning(request, 'Enroll in this course to read lessons.')
        return redirect('courses:detail', slug=course.slug)

    lessons = list(course.lessons.all())
    current_index = next((i for i, item in enumerate(lessons) if item.pk == lesson.pk), 0)
    prev_lesson = lessons[current_index - 1] if current_index > 0 else None
    next_lesson = lessons[current_index + 1] if current_index < len(lessons) - 1 else None

    return render(
        request,
        'courses/lesson_detail.html',
        {
            'course': course,
            'lesson': lesson,
            'lessons': lessons,
            'prev_lesson': prev_lesson,
            'next_lesson': next_lesson,
        },
    )
