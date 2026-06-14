from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from students.models import Grade
from homework.models import Homework
from schedule.models import Schedule


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('cabinet')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                profile = user.profile
                if profile.role == role:
                    login(request, user)
                    return redirect('cabinet')
                else:
                    messages.error(request, f'Вы выбрали неверный тип аккаунта!')
            except Profile.DoesNotExist:
                messages.error(request, 'Профиль не найден. Обратитесь к администратору.')
        else:
            messages.error(request, 'Неверный логин или пароль.')
    
    return render(request, 'registration/login.html')


@login_required
def cabinet(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('dashboard')

    if profile.is_teacher:
        return redirect('teacher_cabinet')
    else:
        return redirect('student_cabinet')


@login_required
def student_cabinet(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return render(request, 'accounts/no_profile.html')

    student = profile.student
    if not student:
        return render(request, 'accounts/no_profile.html')

    grades = Grade.objects.filter(student=student).select_related('course')
    homeworks = Homework.objects.filter(group=student.group).select_related('course')
    schedule = Schedule.objects.filter(group=student.group).select_related('course')

    return render(request, 'accounts/student_cabinet.html', {
        'student': student,
        'grades': grades,
        'homeworks': homeworks,
        'schedule': schedule,
    })


@login_required
def teacher_cabinet(request):
    from students.models import Student
    from groups.models import Group
    from courses.models import Course

    students = Student.objects.select_related('group')
    groups = Group.objects.all()
    courses = Course.objects.all()
    grades = Grade.objects.select_related('student', 'course')

    return render(request, 'accounts/teacher_cabinet.html', {
        'students': students,
        'groups': groups,
        'courses': courses,
        'grades': grades,
    })