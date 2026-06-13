from django.contrib import admin
from .models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'value', 'date']
    list_filter = ['value', 'course']
    search_fields = ['student__first_name', 'student__last_name']
    ordering = ['-date']
