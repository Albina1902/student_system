from groups.models import Group
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
class StudentRegistrationForm(forms.Form):
    username = forms.CharField(
        label='Имя пользователя (логин)',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите логин',
        })
    )
    first_name = forms.CharField(
        label='Имя',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя',
        })
    )
    last_name = forms.CharField(
        label='Фамилия',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваша фамилия',
        })
    )
    email = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.com',
        })
    )
    birth_date = forms.DateField(
    label='Дата рождения',
    widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date',
    })
)
    group = forms.ModelChoiceField(
    label='Группа',
    queryset=Group.objects.all(),
    widget=forms.Select(attrs={
        'class': 'form-select',
    })
)
    password = forms.CharField(
        label='Пароль',
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Минимум 6 символов',
        })
    )
    password_confirm = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают.')
        return cleaned_data