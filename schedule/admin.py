from django.contrib import admin
from .models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['day_of_week', 'time_start', 'time_end', 'course', 'group', 'room']
    list_filter = ['day_of_week', 'group']
    ordering = ['day_of_week', 'time_start']
