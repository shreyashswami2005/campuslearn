from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Video, VideoProgress
from courses.models import Course

@login_required
def all_videos(request):
    videos = Video.objects.all()
    return render(request, 'videos/video_list.html', {'course': None, 'videos': videos})

@login_required
def video_list(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    videos = course.videos.all()
    return render(request, 'videos/video_list.html', {'course': course, 'videos': videos})

@login_required
def video_detail(request, course_slug, video_id):
    course = get_object_or_404(Course, slug=course_slug)
    video = get_object_or_404(Video, pk=video_id, course=course)
    # Get or create progress record
    progress, _ = VideoProgress.objects.get_or_create(student=request.user, video=video)
    if request.method == 'POST':
        # Expect 'last_position' in POST to update progress
        last_position = int(request.POST.get('last_position', 0))
        progress.last_position = last_position
        progress.save()
        return redirect('videos:video_detail', course_slug=course.slug, video_id=video.id)
    return render(request, 'videos/video_detail.html', {'course': course, 'video': video, 'progress': progress})
