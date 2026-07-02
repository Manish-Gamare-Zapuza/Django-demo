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
            department='Engineering',
            role='Developer',
            salary=50000,
            phone='9876543210',
            address='Pune',
        )

    def test_employee_list_requires_login(self):
        response = self.client.get(reverse('employee_list'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_employee_list_shows_employees_after_login(self):
        self.client.login(username='teacher', password='testpass123')

        response = self.client.get(reverse('employee_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Asha Patel')
        self.assertContains(response, 'Engineering')

    def test_create_employee(self):
        self.client.login(username='teacher', password='testpass123')

        response = self.client.post(reverse('employee_create'), {
            'user': '',
            'first_name': 'Rahul',
            'last_name': 'Sharma',
            'email': 'rahul@example.com',
            'department': 'HR',
            'role': 'Manager',
            'salary': '65000',
            'phone': '9999999999',
            'address': 'Mumbai',
        })

        self.assertRedirects(response, reverse('employee_list'))
        self.assertTrue(Employee.objects.filter(email='rahul@example.com').exists())

    def test_update_employee(self):
        self.client.login(username='teacher', password='testpass123')

        response = self.client.post(reverse('employee_update', args=[self.employee.pk]), {
            'user': self.user.pk,
            'first_name': 'Asha',
            'last_name': 'Patel',
            'email': 'asha@example.com',
            'department': 'Product',
            'role': 'Lead Developer',
            'salary': '75000',
            'phone': '9876543210',
            'address': 'Pune',
        })

        self.assertRedirects(response, reverse('employee_detail', args=[self.employee.pk]))
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.department, 'Product')
        self.assertEqual(self.employee.role, 'Lead Developer')

    def test_delete_employee(self):
        self.client.login(username='teacher', password='testpass123')

        response = self.client.post(reverse('employee_delete', args=[self.employee.pk]))

        self.assertRedirects(response, reverse('employee_list'))
        self.assertFalse(Employee.objects.filter(pk=self.employee.pk).exists())

    def test_search_employees(self):
        self.client.login(username='teacher', password='testpass123')

        # Create another employee to test filtering
        Employee.objects.create(
            user=None,
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            department='HR',
            role='Recruiter',
            salary=40000,
        )

        # 1. Search by name (Asha)
        response = self.client.get(reverse('employee_list'), {'q': 'Asha'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Asha Patel')
        self.assertNotContains(response, 'John Doe')

        # 2. Search by department (HR)
        response = self.client.get(reverse('employee_list'), {'q': 'HR'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertNotContains(response, 'Asha Patel')

        # 3. Search by role (Developer)
        response = self.client.get(reverse('employee_list'), {'q': 'Developer'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Asha Patel')
        self.assertNotContains(response, 'John Doe')

        # 4. Search with no matches
        response = self.client.get(reverse('employee_list'), {'q': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No matches found')

