from django import forms
from .models import Schedule


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['group', 'course', 'day_of_week', 'time_start', 'time_end', 'room']
        widgets = {
            'group':       forms.Select(attrs={'class': 'edu-select'}),
            'course':      forms.Select(attrs={'class': 'edu-select'}),
            'day_of_week': forms.Select(attrs={'class': 'edu-select'}),
            'time_start':  forms.TimeInput(attrs={'type': 'time', 'class': 'edu-input'}),
            'time_end':    forms.TimeInput(attrs={'type': 'time', 'class': 'edu-input'}),
            'room':        forms.TextInput(attrs={'class': 'edu-input', 'placeholder': 'Например: 301А'}),
        }

    def clean(self):
        data = super().clean()
        if data.get('time_end') and data.get('time_start'):
            if data['time_end'] <= data['time_start']:
                raise forms.ValidationError('Время конца должно быть позже начала.')
        return data
