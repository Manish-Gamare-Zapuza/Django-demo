from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'profile_photo',
            'user',
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'department',
            'role',
            'salary',
            'date_hired',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'date_hired': forms.DateInput(attrs={'type': 'date'}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
