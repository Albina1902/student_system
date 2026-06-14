from django.shortcuts import render, redirect, get_object_or_404
import qrcode
import io
import base64
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student
from .forms import StudentForm, GradeForm, StudentRegistrationForm
from django.core.paginator import Paginator


@login_required
def student_list(request):
    if request.user.is_staff:
        query = request.GET.get('q')
        students = Student.objects.select_related('group').all()
        if query:
            students = students.filter(first_name__icontains=query)
        paginator = Paginator(students, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'students/student_list.html', {
            'page_obj': page_obj,
            'students': page_obj,
        })
    else:
        student = request.user.student
        return redirect('student_detail', pk=student.pk)


@login_required
def student_detail(request, pk):
    if request.user.is_staff:
        student = get_object_or_404(Student.objects.select_related('group'), pk=pk)
    else:
        student = request.user.student
    grades = student.grades.select_related('course').order_by('-date')
    average = student.average_grade()
    return render(request, 'students/student_detail.html', {
        'student': student,
        'grades': grades,
        'average': average,
    })


@login_required
def student_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Только преподаватели могут добавлять студентов.')
        return redirect('student_list')
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('student_list')

@login_required
def student_update(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Только преподаватели могут редактировать студентов.')
        return redirect('student_list')
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'students/student_form.html', {'form': form})


@login_required
def student_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Только преподаватели могут удалять студентов.')
        return redirect('student_list')
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})


@login_required
def grade_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Только преподаватели могут добавлять оценки.')
        return redirect('student_list')
    form = GradeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'students/grade_form.html', {'form': form})
def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            from django.contrib.auth.models import User
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким именем уже существует.')
                return render(request, 'students/register.html', {'form': form})

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_staff=False,
            )
            Student.objects.create(
    user=user,
    first_name=first_name,
    last_name=last_name,
    email=email,
    birth_date=form.cleaned_data['birth_date'],
    group=form.cleaned_data['group'],
)
            messages.success(request, f'Аккаунт создан! Войдите как {username}.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'students/register.html', {'form': form})


@login_required
def qr_code_view(request):
    if not request.user.is_staff:
        return HttpResponse('Доступ запрещён', status=403)

    host = request.get_host().replace('127.0.0.1', '192.168.1.101')
    register_url = f'http://{host}/students/register/'

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(register_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'students/qr_code.html', {
        'qr_image': img_base64,
        'register_url': register_url,
    })