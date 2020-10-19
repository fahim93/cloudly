from django import forms

from oeta.models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = '__all__'