from django.contrib import admin
from .models import Quiz, Question, Choice, StudentQuizAttempt, StudentAnswer

# Inline for choices within a question admin
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

# Admin for Question to manage its choices
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'order', 'text')
    # inlines = [ChoiceInline]  # Disabled to prevent nested inlines

# Inline for questions within a quiz admin (no nested inlines)
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'active', 'duration')
    inlines = [QuestionInline]

admin.site.register(StudentQuizAttempt)
admin.site.register(StudentAnswer)
