from django import forms
from .models import Homework


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['course', 'group', 'title', 'description', 'due_date']
        widgets = {
            'course':      forms.Select(attrs={'class': 'edu-select'}),
            'group':       forms.Select(attrs={'class': 'edu-select'}),
            'title':       forms.TextInput(attrs={'class': 'edu-input'}),
            'description': forms.Textarea(attrs={'class': 'edu-input', 'rows': 5}),
            'due_date':    forms.DateInput(attrs={'type': 'date', 'class': 'edu-input'}),
        }
        labels = {
            'course': 'Курс', 'group': 'Группа', 'title': 'Название',
            'description': 'Описание задания', 'due_date': 'Срок сдачи',
        }
