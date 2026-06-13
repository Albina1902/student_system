from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=50)
    faculty = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['faculty', 'name']
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return f"{self.name} ({self.faculty})"

    def student_count(self):
        return self.students.count()