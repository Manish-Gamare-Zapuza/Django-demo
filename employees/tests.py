from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Employee

class EmployeeViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teacher', password='testpass123')
        self.employee = Employee.objects.create(
            user=self.user,
            first_name='Asha',
            last_name='Patel',
            email='asha@example.com',
            department='ENG',
            role='DEV',
            salary=50000,
            phone='9876543210',
            address='Pune',
        )

    def test_employee_list_requires_login(self):
        response = self.client.get(reverse('employee_list'))
        self.assertEqual(response.status_code, 302)

    def test_employee_list_shows_employees_after_login(self):
        self.client.login(username='teacher', password='testpass123')
        response = self.client.get(reverse('employee_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Asha Patel')

    def test_create_employee(self):
        self.client.login(username='teacher', password='testpass123')
        response = self.client.post(reverse('employee_create'), {
            'user': self.user.pk,
            'first_name': 'Rahul',
            'last_name': 'Sharma',
            'email': 'rahul@example.com',
            'department': 'HR',
            'role': 'MGR',
            'salary': '65000',
            'phone': '9999999999',
            'address': 'Mumbai',
        })
        self.assertRedirects(response, reverse('employee_list'))

    def test_update_employee(self):
        self.client.login(username='teacher', password='testpass123')
        response = self.client.post(reverse('employee_update', args=[self.employee.pk]), {
            'user': self.user.pk,
            'first_name': 'Asha',
            'last_name': 'Patel',
            'email': 'asha@example.com',
            'department': 'PROD',
            'role': 'LEAD',
            'salary': '75000',
            'phone': '9876543210',
            'address': 'Pune',
        })
        self.assertRedirects(response, reverse('employee_detail', args=[self.employee.pk]))

    def test_delete_employee(self):
        self.client.login(username='teacher', password='testpass123')
        response = self.client.post(reverse('employee_delete', args=[self.employee.pk]))
        self.assertRedirects(response, reverse('employee_list'))