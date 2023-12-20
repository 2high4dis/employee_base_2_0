import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import EmployeeForm
from .models import Employee


class EmployeeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Employee.objects.create(
            full_name='Leonid Danylov', hire_date=datetime.date.today())

    def test_full_name_label(self):
        employee = Employee.objects.last()
        field_label = employee._meta.get_field('full_name').verbose_name
        self.assertEquals(field_label, 'full name')

    def test_hire_date_label(self):
        employee = Employee.objects.last()
        field_label = employee._meta.get_field('hire_date').verbose_name
        self.assertEquals(field_label, 'hire date')

    def test_post_label(self):
        employee = Employee.objects.last()
        field_label = employee._meta.get_field('post').verbose_name
        self.assertEquals(field_label, 'post')

    def test_email_label(self):
        employee = Employee.objects.last()
        field_label = employee._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'email')

    def test_parent_label(self):
        employee = Employee.objects.last()
        field_label = employee._meta.get_field('parent').verbose_name
        self.assertEquals(field_label, 'boss ID')

    def test_full_name_max_length(self):
        employee = Employee.objects.last()
        field_label = employee._meta.get_field('full_name').max_length
        self.assertEquals(field_label, 250)

    def test_object_name_is_full_name_point_post(self):
        employee = Employee.objects.last()
        expected_object_name = f'{employee.full_name}. ({employee.get_post_display()})'
        self.assertEquals(expected_object_name, str(employee))

    def test_get_absolute_url(self):
        employee = Employee.objects.last()
        self.assertEquals(employee.get_absolute_url(), f'/{employee.id}/')

    def test_default_post_value(self):
        employee = Employee.objects.create(
            full_name='New Employee', hire_date=datetime.date.today())
        self.assertEquals(employee.post, Employee.PostChoice.PHARMACIST)


class EmployeeFormTest(TestCase):
    def test_employee_form_parent_field_label(self):
        form = EmployeeForm()
        self.assertTrue(form.fields['parent'].label ==
                        'Boss ID' or form.fields['parent'].label == None)

    def test_employee_form_hire_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=20)
        form_data = {'hire_date': date,
                     'full_name': 'Leonid Danylov',
                     'email': 'danylov.lv@gmail.com',
                     'post': Employee.PostChoice.PHARMACIST}
        form = EmployeeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_employee_form_hire_date_in_future(self):
        date = datetime.date.today() + datetime.timedelta(days=20)
        form_data = {'hire_date': date,
                     'full_name': 'Leonid Danylov',
                     'email': 'danylov.lv@gmail.com',
                     'post': Employee.PostChoice.PHARMACIST}
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())


class EmployeeListViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('employee_list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('employee_list'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'employee/list.html')


class EmployeeCRUDViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            username='test_user', password='test_user123')
        test_user.save()

        employee = Employee.objects.create(
            full_name='Leonid Danylov', hire_date=datetime.date.today())
        employee.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('employee_create'))

        self.assertRedirects(resp, '/accounts/login/?next=/add/')

    def test_logged_in_uses_correct_template(self):
        employee = Employee.objects.first()

        login = self.client.login(
            username='test_user', password='test_user123')

        resp_create = self.client.get(reverse('employee_create'))
        resp_update = self.client.get(
            reverse('employee_update', kwargs={'pk': employee.id}))
        resp_delete = self.client.get(
            reverse('employee_delete', kwargs={'pk': employee.id}))

        self.assertTrue(str(resp_create.context['user']) == 'test_user' and
                        str(resp_update.context['user']) == 'test_user' and
                        str(resp_delete.context['user']) == 'test_user')
        self.assertTrue(resp_create.status_code == 200 and
                        resp_update.status_code == 200 and
                        resp_delete.status_code == 200)

        self.assertTemplateUsed(resp_create, 'employee/form.html')
        self.assertTemplateUsed(resp_update, 'employee/form.html')
        self.assertTemplateUsed(
            resp_delete, 'employee/delete_confirmation.html')

    def test_swap_bosses_ajax_request_logged_off(self):
        employee = Employee.objects.first()
        parent_new = Employee.objects.last()
        parent_old = employee.parent

        self.assertEqual(employee.parent, parent_old)

        resp = self.client.post(reverse('swap_bosses'), {
                                'parent_id': parent_new.id, 'child_id': employee.id})

        self.assertNotEqual(resp.status_code, 200)

        employee.refresh_from_db()

        self.assertNotEqual(employee.parent, parent_new)

    def test_swap_bosses_ajax_request_works(self):
        employee = Employee.objects.first()
        parent_new = Employee.objects.last()
        parent_old = employee.parent

        login = self.client.login(
            username='test_user', password='test_user123')

        self.assertEqual(employee.parent, parent_old)

        resp = self.client.post(reverse('swap_bosses'), {
                                'parent_id': parent_new.id, 'child_id': employee.id})

        self.assertEqual(resp.status_code, 200)

        employee.refresh_from_db()

        self.assertEqual(employee.parent, parent_new)


class EmployeeDetailViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        employee = Employee.objects.last()
        resp = self.client.get(f'/{employee.id}/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        employee = Employee.objects.last()
        resp = self.client.get(
            reverse('employee_detail', kwargs={'pk': employee.id}))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        employee = Employee.objects.last()
        resp = self.client.get(
            reverse('employee_detail', kwargs={'pk': employee.id}))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'employee/detail.html')

    def test_view_status_pk_out_of_range(self):
        wrong_employee_id = Employee.objects.count() + 10000
        resp = self.client.get(
            reverse('employee_detail', kwargs={'pk': wrong_employee_id}))
        self.assertEqual(resp.status_code, 404)
