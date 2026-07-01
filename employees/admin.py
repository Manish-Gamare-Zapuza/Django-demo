from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'department', 'role','status', 'user')
    list_filter = ('department', 'role', 'status')
    search_fields = ('first_name', 'last_name', 'email', 'department', 'role', 'status')
