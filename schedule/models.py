from django.db import models


class Schedule(models.Model):
    DAY_CHOICES = [
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
    ]

    group = models.ForeignKey(
        'groups.Group',
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='Группа'
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='Курс'
    )
    day_of_week = models.IntegerField(choices=DAY_CHOICES, verbose_name='День недели')
    time_start = models.TimeField(verbose_name='Начало')
    time_end = models.TimeField(verbose_name='Конец')
    room = models.CharField(max_length=50, verbose_name='Аудитория')

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Расписание'
        ordering = ['day_of_week', 'time_start']

    def __str__(self):
        return f'{self.get_day_of_week_display()} {self.time_start} — {self.course} ({self.group})'
