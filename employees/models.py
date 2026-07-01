from django.conf import settings
from django.db import models

class Employee(models.Model):
    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        PREFER_NOT_TO_SAY = "PREFER NOT TO SAY", "Prefer not to say"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employee_profile',
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=20,
        choices=Gender.choices,
        default=Gender.PREFER_NOT_TO_SAY,
    )
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_hired = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"
