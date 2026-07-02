from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Employee(models.Model):
    # 1. Define the choices FIRST
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
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )

    # 2. Changed to ForeignKey to allow multiple employees per user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_employees',
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    # 3. Apply the choices defined above
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    phone = models.CharField(
        max_length=10,
        validators=[phone_regex], # Add the validator here
        blank=False
    )
    address = models.TextField(blank=True)
    date_hired = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_role_display()}"

    # 4. Custom validation to enforce the max 10 rule
    def clean(self):
        super().clean()
        if self.user:
            current_count = Employee.objects.filter(user=self.user).exclude(pk=self.pk).count()

            if current_count >= 10:
                raise ValidationError({
                    'user': 'This user is already linked to the maximum of 10 employees.'
                })
