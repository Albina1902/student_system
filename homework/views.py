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
    homeworks = Homework.objects.select_related('course', 'group')
    course_id = request.GET.get('course')
    if course_id:
        homeworks = homeworks.filter(course_id=course_id)
    return render(request, 'homework/homework_list.html', {
        'homeworks': homeworks,
        'courses': Course.objects.all(),
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
    obj = get_object_or_404(Homework, pk=pk)
    form = HomeworkForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Задание обновлено.')
        return redirect('homework_list')
    return render(request, 'homework/homework_form.html', {'form': form, 'title': 'Редактировать задание', 'obj': obj})


@login_required
def homework_delete(request, pk):
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
