from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
import re

from .models import Employee

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

class EmployeeForm(forms.ModelForm):

    gender = forms.ChoiceField(
        choices=[('', '--- Select Gender ---')] + GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'border: 2px solid #0d6efd; padding: 8px; font-size: 14px; border-radius: 6px; color: #000000; background: #ffffff;'
        })
    )

    class Meta:
        model = Employee
        fields = [
            'user', 'first_name', 'last_name', 'email',
            'gender', 'department', 'role', 'salary', 'phone', 'address',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Please enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Please enter your last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Please enter your email'}),
            'department': forms.TextInput(attrs={'placeholder': 'Please enter your department'}),
            'role': forms.TextInput(attrs={'placeholder': 'Please enter your role'}),
            'salary': forms.NumberInput(attrs={'placeholder': 'Please enter your salary'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Please enter your phone number'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Please enter your address'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^[0-9]{10}$', phone):
            raise ValidationError("Invalid phone number! It must be exactly 10 digits.")
        return phone

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary and salary <= 0:
            raise ValidationError("Salary must be a positive number.")
        return salary

    @property
    def help_section(self):
        html_code = """
        <div class="card shadow-sm mt-4 p-4" style="background-color: #f8f9fa; border-radius: 8px; font-family: sans-serif; border: 3px solid #0d6efd;">
            <h3 class="border-bottom pb-2 mb-3" style="color: #0d6efd; border-bottom: 1px solid #dee2e6; font-weight: bold;">💡 Quick Help & FAQ</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 20px;">
                <div style="flex: 1; min-width: 250px;">
                    <h6 style="font-weight: bold; margin-bottom: 5px; color: #002244;">❓ Name field showing errors?</h6>
                    <p style="color: #6c757d; font-size: 14px; margin-top: 0;"><strong>Ans:</strong> Please enter only letters. Do not use numbers or special characters.</p>
                    <h6 style="font-weight: bold; margin-bottom: 5px; margin-top: 15px; color: #002244;">❓ What is the correct Phone format?</h6>
                    <p style="color: #6c757d; font-size: 14px; margin-top: 0;"><strong>Ans:</strong> Enter exactly 10 digits. Do not include spaces, dashes, or country codes.</p>
                </div>
                <div style="flex: 1; min-width: 250px;">
                    <h6 style="font-weight: bold; margin-bottom: 5px; color: #002244;">❓ Facing Department or Role issues?</h6>
                    <p style="color: #6c757d; font-size: 14px; margin-top: 0;"><strong>Ans:</strong> Type the official department name clearly (e.g., "IT", "HR"). Avoid confusing shortcuts.</p>
                    <h6 style="font-weight: bold; margin-bottom: 5px; margin-top: 15px; color: #002244;">❓ Form is not submitting?</h6>
                    <p style="color: #6c757d; font-size: 14px; margin-top: 0;"><strong>Ans:</strong> Check for any red error messages. Make sure the Salary is positive and Email is valid.</p>
                </div>
            </div>
        </div>
        """
        return mark_safe(html_code)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email']