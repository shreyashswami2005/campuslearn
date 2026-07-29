from django.contrib import admin
from .models import Quiz, Question, Choice, StudentQuizAttempt, StudentAnswer

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    inlines = [ChoiceInline]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'active', 'duration')
    inlines = [QuestionInline]

admin.site.register(StudentQuizAttempt)
admin.site.register(StudentAnswer)
