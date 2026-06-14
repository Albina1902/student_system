import json
import urllib.request
import urllib.error
import ssl
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from .models import Homework, AIExplanation
from .forms import HomeworkForm
from courses.models import Course


@login_required
def homework_list(request):
    course_id = request.GET.get('course')

    if request.user.is_staff:
        homeworks = Homework.objects.select_related('course', 'group')
        if course_id:
            homeworks = homeworks.filter(course_id=course_id)
        courses = Course.objects.all()
    else:
        student = request.user.student
        homeworks = Homework.objects.filter(group=student.group).select_related('course', 'group')
        if course_id:
            homeworks = homeworks.filter(course_id=course_id)
        courses = Course.objects.filter(homeworks__group=student.group).distinct()

    return render(request, 'homework/homework_list.html', {
        'homeworks': homeworks,
        'courses': courses,
        'selected_course': course_id,
    })


@login_required
def homework_detail(request, pk):
    hw = get_object_or_404(Homework, pk=pk)
    explanations = hw.explanations.all()[:10]
    return render(request, 'homework/homework_detail.html', {
        'hw': hw,
        'explanations': explanations,
    })


@login_required
def homework_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Только преподаватели могут создавать задания.')
        return redirect('homework_list')
    form = HomeworkForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        messages.success(request, 'Задание создано.')
        return redirect('homework_list')
    return render(request, 'homework/homework_form.html', {'form': form, 'title': 'Новое задание'})

@login_required
def homework_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Только преподаватели могут редактировать задания.')
        return redirect('homework_list')
    obj = get_object_or_404(Homework, pk=pk)
    form = HomeworkForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Задание обновлено.')
        return redirect('homework_list')
    return render(request, 'homework/homework_form.html', {'form': form, 'title': 'Редактировать задание', 'obj': obj})


@login_required
def homework_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Только преподаватели могут удалять задания.')
        return redirect('homework_list')
    obj = get_object_or_404(Homework, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Задание удалено.')
        return redirect('homework_list')
    return render(request, 'homework/homework_confirm_delete.html', {'obj': obj})


@login_required
def ai_explain(request, pk):
    """AJAX-эндпоинт: задаём вопрос AI по теме задания"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    hw = get_object_or_404(Homework, pk=pk)

    try:
        body = json.loads(request.body)
        question = body.get('question', '').strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Неверный формат запроса'}, status=400)

    if not question:
        return JsonResponse({'error': 'Вопрос не может быть пустым'}, status=400)

    # Формируем системный промпт с контекстом задания
    system_prompt = f"""Ты помощник-преподаватель в учебной системе EduSystem.
Студент изучает предмет "{hw.course.title}" и работает над заданием:

Название: {hw.title}
Описание: {hw.description}

Твоя задача — объяснять темы понятно и по-русски.
Давай конкретные примеры. Отвечай кратко, но исчерпывающе.
Если вопрос не по теме — вежливо перенаправь на тему задания."""

    api_key = getattr(settings, 'ANTHROPIC_API_KEY', '')
    if not api_key:
        return JsonResponse({'error': 'API ключ не настроен. Добавьте ANTHROPIC_API_KEY в settings.py'}, status=500)

    payload = json.dumps({
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 1024,
        "system": system_prompt,
        "messages": [{"role": "user", "content": question}]
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01',
        },
        method='POST'
    )

    try:
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            data = json.loads(resp.read())
            answer = data['content'][0]['text']
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        return JsonResponse({'error': f'Ошибка API: {e.code} — {error_body}'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    # Сохраняем в кеш
    AIExplanation.objects.create(homework=hw, question=question, answer=answer)

    return JsonResponse({'answer': answer})
@login_required
def homework_submit(request, pk):
    """Студент сдаёт ДЗ"""
    if request.user.is_staff:
        return redirect('homework_list')

    hw = get_object_or_404(Homework, pk=pk)
    student = request.user.student

    # Проверяем — уже сдавал?
    existing = hw.submissions.filter(student=student).first()

    if request.method == 'POST':
        answer = request.POST.get('answer', '').strip()
        if answer:
            if existing:
                existing.answer = answer
                existing.status = 'submitted'
                existing.save()
                messages.success(request, 'Ответ обновлён!')
            else:
                from .models import HomeworkSubmission
                HomeworkSubmission.objects.create(
                    homework=hw,
                    student=student,
                    answer=answer
                )
                messages.success(request, 'Задание сдано!')
            return redirect('homework_list')

    return render(request, 'homework/homework_submit.html', {
        'hw': hw,
        'existing': existing,
    })


@login_required
def homework_submissions(request, pk):
    """Преподаватель видит все ответы на задание"""
    if not request.user.is_staff:
        return redirect('homework_list')

    hw = get_object_or_404(Homework, pk=pk)
    submissions = hw.submissions.select_related('student').all()

    if request.method == 'POST':
        sub_id = request.POST.get('submission_id')
        comment = request.POST.get('comment', '')
        status = request.POST.get('status', 'checked')
        from .models import HomeworkSubmission
        sub = get_object_or_404(HomeworkSubmission, pk=sub_id)
        sub.teacher_comment = comment
        sub.status = status
        sub.save()
        messages.success(request, 'Комментарий сохранён!')
        return redirect('homework_submissions', pk=pk)

    return render(request, 'homework/homework_submissions.html', {
        'hw': hw,
        'submissions': submissions,
    })