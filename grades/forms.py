# forms.py
from django import forms
from .models import Grade


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'course', 'value', 'date', 'comment']
        widgets = {
            'student': forms.Select(attrs={'class': 'edu-select'}),
            'course':  forms.Select(attrs={'class': 'edu-select'}),
            'value':   forms.Select(attrs={'class': 'edu-select'}),
            'date':    forms.DateInput(attrs={'type': 'date', 'class': 'edu-input'}),
            'comment': forms.Textarea(attrs={'class': 'edu-input', 'rows': 3}),
        }
