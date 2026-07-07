from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'user',
            'first_name',
            'last_name',
            'email',
            'department',
            'role',
            'salary',
            'phone',
            'address',
            'profile_photo',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




