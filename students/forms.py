from django import forms
from .models import Student, Grade

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = '__all__'
