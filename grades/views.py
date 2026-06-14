from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Grade
from students.models import Student
from .forms import GradeForm
from students.models import Student
from courses.models import Course


@login_required
def grade_list(request):
    if request.user.is_staff:
        grades = Grade.objects.select_related('student', 'course')
        student_id = request.GET.get('student')
        course_id = request.GET.get('course')
        if student_id:
            grades = grades.filter(student_id=student_id)
        if course_id:
            grades = grades.filter(course_id=course_id)
        return render(request, 'grades/grade_list.html', {
            'grades': grades,
            'students': Student.objects.all(),
            'courses': Course.objects.all(),
            'selected_student': student_id,
            'selected_course': course_id,
        })
    else:
        from students.models import Grade as OldGrade
        student = request.user.student
        grades = Grade.objects.filter(student=student).select_related('course')
        if not grades.exists():
            grades = OldGrade.objects.filter(student=student).select_related('course')
        avg = grades.aggregate(avg=Avg('value'))['avg']
        return render(request, 'grades/student_grades.html', {
            'student': student,
            'grades': grades,
            'avg': round(avg, 2) if avg else None,
        })


@login_required
def grade_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Только преподаватели могут добавлять оценки.')
        return redirect('grade_list')
    form = GradeForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Оценка добавлена.')
        return redirect('grade_list')
    return render(request, 'grades/grade_form.html', {'form': form, 'title': 'Добавить оценку'})


@login_required
def grade_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Только преподаватели могут редактировать оценки.')
        return redirect('grade_list')
    obj = get_object_or_404(Grade, pk=pk)
    form = GradeForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Оценка обновлена.')
        return redirect('grade_list')
    return render(request, 'grades/grade_form.html', {'form': form, 'title': 'Редактировать оценку', 'obj': obj})


@login_required
def grade_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Только преподаватели могут удалять оценки.')
        return redirect('grade_list')
    obj = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Оценка удалена.')
        return redirect('grade_list')
    return render(request, 'grades/grade_confirm_delete.html', {'obj': obj})


@login_required
def student_grades(request, student_id):
    if not request.user.is_staff:
        student = request.user.student
    else:
        student = get_object_or_404(Student, pk=student_id)
    grades = Grade.objects.filter(student=student).select_related('course')
    avg = grades.aggregate(avg=Avg('value'))['avg']
    return render(request, 'grades/student_grades.html', {
        'student': student,
        'grades': grades,
        'avg': round(avg, 2) if avg else None,
    })
