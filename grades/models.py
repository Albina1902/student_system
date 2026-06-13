from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Grade(models.Model):
    GRADE_CHOICES = [(5, '5 — Отлично'), (4, '4 — Хорошо'), (3, '3 — Удовл.'), (2, '2 — Неудовл.')]

    student = models.ForeignKey(
        'students.Student', on_delete=models.CASCADE,
        related_name='grade_records', verbose_name='Студент'
    )
    course = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE,
        related_name='grade_records', verbose_name='Курс'
    )
    value = models.IntegerField(
        choices=GRADE_CHOICES,
        validators=[MinValueValidator(2), MaxValueValidator(5)],
        verbose_name='Оценка'
    )
    date = models.DateField(verbose_name='Дата')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        ordering = ['-date']

    def __str__(self):
        return f'{self.student} — {self.course}: {self.value}'

    @property
    def badge_class(self):
        return {5: 'badge-success', 4: 'badge-primary', 3: 'badge-warning', 2: 'badge-danger'}.get(self.value, '')
    