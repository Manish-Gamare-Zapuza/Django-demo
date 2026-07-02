from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'department', 'role', 'user')
    list_filter = ('department', 'role')
    search_fields = ('first_name', 'last_name', 'email', 'department', 'role')

    # --- IMPROVEMENTS ---
    # Performance: Fetches the related 'user' table in the same query
    list_select_related = ('user',)

    list_per_page = 25
    empty_value_display = '-empty-'