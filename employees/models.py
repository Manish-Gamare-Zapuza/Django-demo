from django.conf import settings
from django.db import models


class Employee(models.Model):
    # --- IMPROVEMENTS: Define Choices ---
    DEPARTMENT_CHOICES = [
        ('HR', 'Human Resources'),
        ('ENG', 'Engineering'),
        ('SALES', 'Sales'),
        ('PROD', 'Product'),
    ]

    ROLE_CHOICES = [
        ('DEV', 'Developer'),
        ('LEAD', 'Lead Developer'),
        ('MGR', 'Manager'),
        ('DIR', 'Director'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employee_profile',
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    # --- IMPROVEMENTS: Apply Choices ---
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_hired = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_role_display()}"