from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator # NEW IMPORT

from .models import Employee


class EmployeeForm(forms.ModelForm):
    # --- IMPROVEMENT: Phone Validation ---
    phone_validator = RegexValidator(
        regex=r'^\d{10,15}$',
        message="Phone number must be entered in the format: '999999999'. Up to 10 digits allowed."
    )
    phone = forms.CharField(validators=[phone_validator], required=False)

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
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
