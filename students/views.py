from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm, GradeForm
from django.core.paginator import Paginator


def student_list(request):
    query = request.GET.get('q')
    group_id = request.GET.get('group')
    students = Student.objects.select_related('group').all()
    if query:
        students = students.filter(first_name__icontains=query)
    if group_id:
        students = students.filter(group_id=group_id)
    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'students/student_list.html', {
        'page_obj': page_obj,
        'students': page_obj,
    })


def student_detail(request, pk):
    student = get_object_or_404(Student.objects.select_related('group'), pk=pk)
    grades = student.grades.select_related('course').order_by('-date')
    average = student.average_grade()
    return render(request, 'students/student_detail.html', {
        'student': student,
        'grades': grades,
        'average': average,
    })


def student_create(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'students/student_form.html', {'form': form})


def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'students/student_form.html', {'form': form})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})


def grade_create(request):
    form = GradeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'students/grade_form.html', {'form': form})