from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from groups.models import Group

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='students'
    )

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def average_grade(self):
        grades = self.grades.all()
        if not grades:
            return None
        return round(sum(g.value for g in grades) / len(grades), 2)


class Grade(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='grades'
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='grades'
    )
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # один студент = одна оценка за курс
        ordering = ['-date']
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'

    def __str__(self):
        return f"{self.student} — {self.course} — {self.value}"