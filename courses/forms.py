from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 rounded-xl bg-gray-700 text-white border border-gray-600 focus:ring-2 focus:ring-indigo-500 outline-none"
            }),
            "teacher": forms.Select(attrs={
                "class": "w-full px-4 py-2 rounded-xl bg-gray-700 text-white border border-gray-600"
            }),
        }