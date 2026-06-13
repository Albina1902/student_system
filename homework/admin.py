from django.contrib import admin
from .models import Homework, AIExplanation


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'group', 'due_date', 'created_by']
    list_filter = ['course', 'group']
    search_fields = ['title']


@admin.register(AIExplanation)
class AIExplanationAdmin(admin.ModelAdmin):
    list_display = ['homework', 'question', 'created_at']
    readonly_fields = ['homework', 'question', 'answer', 'created_at']
