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
class HomeworkSubmission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Сдано'),
        ('checked', 'Проверено'),
        ('revision', 'На доработку'),
    ]

    homework = models.ForeignKey(
        Homework, on_delete=models.CASCADE,
        related_name='submissions', verbose_name='Задание'
    )
    student = models.ForeignKey(
        'students.Student', on_delete=models.CASCADE,
        related_name='submissions', verbose_name='Студент'
    )
    answer = models.TextField(verbose_name='Ответ студента')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='submitted', verbose_name='Статус'
    )
    teacher_comment = models.TextField(
        blank=True, verbose_name='Комментарий преподавателя'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    checked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Ответ на задание'
        verbose_name_plural = 'Ответы на задания'
        ordering = ['-submitted_at']
        unique_together = ('homework', 'student')

    def __str__(self):
        return f'{self.student} → {self.homework.title}'