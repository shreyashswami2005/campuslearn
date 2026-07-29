from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Quiz, Question, Choice, StudentQuizAttempt, StudentAnswer
from courses.models import Course

@login_required
def all_quizzes(request):
    quizzes = Quiz.objects.filter(active=True)
    return render(request, 'quizzes/quiz_list.html', {'course': None, 'quizzes': quizzes})

@login_required
def quiz_list(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    quizzes = course.quizzes.filter(active=True)
    return render(request, 'quizzes/quiz_list.html', {'course': course, 'quizzes': quizzes})

@login_required
def quiz_detail(request, course_slug, quiz_id):
    course = get_object_or_404(Course, slug=course_slug)
    quiz = get_object_or_404(Quiz, pk=quiz_id, course=course, active=True)
    # Get or create attempt
    attempt, created = StudentQuizAttempt.objects.get_or_create(student=request.user, quiz=quiz)
    if request.method == 'POST':
        # Process answers
        for question in quiz.questions.all():
            choice_id = request.POST.get(str(question.id))
            if choice_id:
                choice = get_object_or_404(Choice, pk=choice_id, question=question)
                StudentAnswer.objects.update_or_create(attempt=attempt, question=question, defaults={'selected_choice': choice})
        # Calculate score
        total = quiz.questions.count()
        correct = sum(1 for ans in attempt.answers.select_related('selected_choice') if ans.selected_choice.is_correct)
        attempt.score = (correct / total) * 100 if total else 0
        attempt.end_time = timezone.now()
        attempt.save()
        return redirect('quizzes:quiz_result', course_slug=course.slug, quiz_id=quiz.id)
    else:
        # Render form
        return render(request, 'quizzes/quiz_detail.html', {'course': course, 'quiz': quiz, 'attempt': attempt})

@login_required
def quiz_result(request, course_slug, quiz_id):
    course = get_object_or_404(Course, slug=course_slug)
    quiz = get_object_or_404(Quiz, pk=quiz_id, course=course)
    attempt = get_object_or_404(StudentQuizAttempt, student=request.user, quiz=quiz)
    # Gather data for display
    answers = attempt.answers.select_related('question', 'selected_choice')
    return render(request, 'quizzes/quiz_result.html', {'course': course, 'quiz': quiz, 'attempt': attempt, 'answers': answers})
