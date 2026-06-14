from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Schedule
from .forms import ScheduleForm
from groups.models import Group


@login_required
def schedule_list(request):
    group_id = request.GET.get('group')

    if request.user.is_staff:
        schedules = Schedule.objects.select_related('group', 'course', 'course__teacher')
        if group_id:
            schedules = schedules.filter(group_id=group_id)
        groups = Group.objects.all()
    else:
        student = request.user.student
        schedules = Schedule.objects.filter(group=student.group).select_related('group', 'course', 'course__teacher')
        groups = Group.objects.filter(id=student.group.id)
        group_id = student.group.id

    # Группируем по дням
    days_data = {}
    for num, name in Schedule.DAY_CHOICES:
        day_qs = schedules.filter(day_of_week=num)
        if day_qs.exists():
            days_data[name] = day_qs

    return render(request, 'schedule/schedule_list.html', {
        'days_data': days_data,
        'groups': groups,
        'selected_group': group_id,
    })


@login_required
def schedule_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Только преподаватели могут создавать расписание.')
        return redirect('schedule_list')
    form = ScheduleForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Занятие добавлено.')
        return redirect('schedule_list')
    return render(request, 'schedule/schedule_form.html', {'form': form, 'title': 'Добавить занятие'})


@login_required
def schedule_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Только преподаватели могут редактировать расписание.')
        return redirect('schedule_list')
    obj = get_object_or_404(Schedule, pk=pk)
    form = ScheduleForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Занятие обновлено.')
        return redirect('schedule_list')
    return render(request, 'schedule/schedule_form.html', {'form': form, 'title': 'Редактировать', 'obj': obj})


@login_required
def schedule_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Только преподаватели могут удалять расписание.')
        return redirect('schedule_list')
    obj = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Занятие удалено.')
        return redirect('schedule_list')
    return render(request, 'schedule/schedule_confirm_delete.html', {'obj': obj})