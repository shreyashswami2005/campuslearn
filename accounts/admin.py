from django.contrib import admin

from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'college', 'department', 'year_of_study', 'student_id', 'updated_at')
    search_fields = ('user__username', 'user__email', 'college', 'student_id')
    autocomplete_fields = ['user']
