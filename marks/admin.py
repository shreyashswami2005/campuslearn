from django.contrib import admin
from .models import Component, InternalMark

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight')
    search_fields = ('name',)

@admin.register(InternalMark)
class InternalMarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'component', 'score', 'max_score', 'date_recorded')
    list_filter = ('component', 'course')
    search_fields = ('student__username', 'course__title')
