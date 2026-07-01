from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmployeeForm, RegisterForm
from .models import Employee
from django.db import models

def home(request):
    if request.user.is_authenticated:
        return redirect('employee_list')
    return render(request, 'employees/home.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('employee_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('employee_list')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def employee_list(request):
    employees = Employee.objects.select_related('user').order_by('first_name', 'last_name')
    search_query = request.GET.get('search', '')
    if search_query:
        employees = employees.filter(
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query) |
            models.Q(email__icontains=search_query) |
            models.Q(department__icontains=search_query) |
            models.Q(role__icontains=search_query)
        )
    return render(request, 'employees/employee_list.html', {'employees': employees, 'search_query': search_query})


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee.objects.select_related('user'), pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})


@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Add Employee',
    })


@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Update Employee',
    })


@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully.')
        return redirect('employee_list')

    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})
