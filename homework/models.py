from django.db import models
from django.contrib.auth.models import User


class Homework(models.Model):
    course = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE,
        related_name='homeworks', verbose_name='Курс'
    )
    group = models.ForeignKey(
        'groups.Group', on_delete=models.CASCADE,
        related_name='homeworks', verbose_name='Группа'
    )
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание задания')
    due_date = models.DateField(verbose_name='Срок сдачи')
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        verbose_name='Создал'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'
        ordering = ['-due_date']

    def __str__(self):
        return f'{self.title} ({self.course})'


class AIExplanation(models.Model):
    """Кеш объяснений от AI — чтобы не делать лишние запросы"""
    homework = models.ForeignKey(
        Homework, on_delete=models.CASCADE,
        related_name='explanations'
    )
    question = models.TextField(verbose_name='Вопрос студента')
    answer = models.TextField(verbose_name='Ответ AI')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Объяснение AI'
        verbose_name_plural = 'Объяснения AI'
        ordering = ['-created_at']
