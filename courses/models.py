from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )
    groups = models.ManyToManyField(
        'groups.Group',
        blank=True,
        related_name='courses'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.title

    def average_grade(self):
        grades = self.grades.all()
        if not grades:
            return None
        return round(sum(g.value for g in grades) / len(grades), 2)

    def student_count(self):
        return self.grades.values('student').distinct().count()