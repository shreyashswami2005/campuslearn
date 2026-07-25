from django.contrib import admin

from .models import Attendance, Course, Enrollment, Lesson, Result


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    ordering = ['order']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'created_by', 'created_at')
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'description', 'category')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]
    autocomplete_fields = ['created_by']

    def save_model(self, request, obj, form, change):
        if not change and not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'content')
    autocomplete_fields = ['course']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
    list_filter = ('course',)
    search_fields = ('student__username', 'course__title')
    autocomplete_fields = ['student', 'course']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'course',
        'title',
        'exam_type',
        'marks_obtained',
        'max_marks',
        'grade',
        'exam_date',
    )
    list_filter = ('exam_type', 'course', 'grade')
    search_fields = ('student__username', 'title', 'course__title')
    autocomplete_fields = ['student', 'course']
    date_hierarchy = 'exam_date'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status', 'remarks')
    list_filter = ('status', 'course', 'date')
    search_fields = ('student__username', 'course__title')
    autocomplete_fields = ['student', 'course']
    date_hierarchy = 'date'
