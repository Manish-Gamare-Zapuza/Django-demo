from django.contrib.auth.models import User
from django.test import TestCase
from django.template.context import BaseContext, Context, RequestContext
from django.urls import reverse

from .models import Employee


def _copy_base_context(self):
    duplicate = self.__class__.__new__(self.__class__)
    duplicate.dicts = self.dicts[:]
    return duplicate


def _copy_context(self):
    duplicate = _copy_base_context(self)
    duplicate.autoescape = self.autoescape
    duplicate.use_l10n = self.use_l10n
    duplicate.use_tz = self.use_tz
    duplicate.template_name = self.template_name
    duplicate.render_context = self.render_context.__copy__()
    duplicate.template = self.template
    return duplicate


def _copy_request_context(self):
    duplicate = _copy_context(self)
    duplicate.request = self.request
    duplicate._processors = self._processors
    duplicate._processors_index = self._processors_index
    return duplicate


# Django 4.2's built-in context copy implementation is not compatible with
# Python 3.14, but the application itself is still valid on Django 4.x.
BaseContext.__copy__ = _copy_base_context
Context.__copy__ = _copy_context
RequestContext.__copy__ = _copy_request_context


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
            date_hired='2026-01-15',
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
        self.assertContains(response, 'AP')

    def test_login_shows_welcome_message(self):
        response = self.client.post(reverse('login'), {
            'username': 'teacher',
            'password': 'testpass123',
        }, follow=True)

        self.assertContains(response, 'Welcome back, teacher!')

    def test_employee_search_filters_results(self):
        Employee.objects.create(
            first_name='Rahul',
            last_name='Sharma',
            email='rahul@example.com',
            department='HR',
            role='Manager',
            salary=65000,
            phone='9999999999',
            address='Mumbai',
            date_hired='2026-02-01',
        )
        self.client.login(username='teacher', password='testpass123')

        response = self.client.get(reverse('employee_list'), {'q': 'Engineering'})

        self.assertContains(response, 'Asha Patel')
        self.assertNotContains(response, 'Rahul Sharma')
        self.assertContains(response, 'value="Engineering"')

    def test_employee_sorting_by_email_desc(self):
        Employee.objects.create(
            first_name='Rahul',
            last_name='Sharma',
            email='rahul@example.com',
            department='HR',
            role='Manager',
            salary=65000,
            phone='9999999999',
            address='Mumbai',
            date_hired='2026-02-01',
        )
        self.client.login(username='teacher', password='testpass123')

        response = self.client.get(reverse('employee_list'), {
            'sort': 'email',
            'order': 'desc',
        })

        employees = list(response.context['employees'])
        self.assertEqual(employees[0].email, 'rahul@example.com')
        self.assertEqual(employees[1].email, 'asha@example.com')

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
            'date_hired': '2026-02-01',
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
            'date_hired': '2026-01-15',
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
