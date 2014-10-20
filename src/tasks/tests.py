# -*- coding: utf-8 -*-
import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from users.models import User
from tasks.models import Task


class BaseTestCase(TestCase):
    user_data = {
        'email': 'foo@bar.com',
        'password': '12345'
    }

    def setUp(self):
        self.user = User.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

    def tearDown(self):
        User.objects.all().delete()

    def assertObjectAttrs(self, obj, **attrs):
        for attr, value in attrs.items():
            self.assertEqual(getattr(obj, attr), value)


class TaskDetailTests(BaseTestCase):
    def setUp(self):
        super(TaskDetailTests, self).setUp()
        self.task = Task.objects.create(
            title='New task',
            created_by=self.user,
            status=Task.TASK_STATUS.OPEN,
            due_date=datetime.datetime.now().date()
        )

        self.other_task = Task.objects.create(
            title='Other task',
            created_by=User.objects.create_user(email='foo@baz.bar', password='12345'),
            status=Task.TASK_STATUS.OPEN,
            due_date=datetime.datetime.now().date()
        )

    def tearDown(self):
        super(TaskDetailTests, self).tearDown()
        Task.objects.all().delete()

    def test_task_detail(self):
        response = self.client.get(reverse('tasks:task_detail', args=(self.task.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')

    def test_try_to_see_other_user_task(self):
        url = reverse('tasks:task_detail', args=(self.other_task.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class TasksListTests(BaseTestCase):

    def setUp(self):
        super(TasksListTests, self).setUp()
        self.second_user = User.objects.create_user(
            email='foo@baz.bar',
            password='12345'
        )
        self.task1 = Task.objects.create(
            created_by=self.user,
            title='Task 1',
            status=Task.TASK_STATUS.OPEN,
            due_date=datetime.datetime.now()
        )
        self.task2 = Task.objects.create(
            created_by=self.user,
            title='Task 2',
            status=Task.TASK_STATUS.OPEN,
            due_date=datetime.datetime.now()
        )

        self.task3 = Task.objects.create(
            created_by=self.second_user,
            title='Task of other user',
            status=Task.TASK_STATUS.OPEN,
            due_date=datetime.datetime.now()
        )

    def tearDown(self):
        super(TasksListTests, self).tearDown()
        Task.objects.all().delete()

    def test_anonymous_user_redirects_lo_login(self):
        self.client.logout()
        response = self.client.get(reverse('tasks:task_list'))
        self.assertRedirects(response, reverse('users:login') + '?next=/tasks/')

    def test_queries_count(self):
        with self.assertNumQueries(2):
            self.client.get(reverse('tasks:task_list'))

    def test_user_see_only_own_tasks(self):
        response = self.client.get(reverse('tasks:task_list'))
        self.assertNotContains(response, self.task3.title)


class CreateTaskTests(BaseTestCase):

    def setUp(self):
        super(CreateTaskTests, self).setUp()

    def tearDown(self):
        super(CreateTaskTests, self).tearDown()
        Task.objects.all().delete()

    def get_task_data(self, **kwargs):
        task_data = {
            'title': 'New task',
            'description': 'test',
            'status': Task.TASK_STATUS.OPEN,
            'due_date': '10/29/2014',
        }
        task_data.update(kwargs)
        return task_data

    def test_create(self):
        task_data = self.get_task_data()
        response = self.client.post(reverse('tasks:task_new'), task_data)
        self.assertRedirects(response, reverse('tasks:task_list'))
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertObjectAttrs(
            task,
            title=task_data['title'],
            description=task_data['description'],
            status=task_data['status'],
            due_date=datetime.date(2014, 10, 29)
        )

    def test_anonymous_user(self):
        self.client.logout()
        response = self.client.post(reverse('tasks:task_new'), self.get_task_data())
        self.assertRedirects(response, reverse('users:login') + '?next=/tasks/new')


class EditTaskTests(BaseTestCase):

    def setUp(self):
        super(EditTaskTests, self).setUp()
        self.task = Task.objects.create(
            created_by=self.user,
            title='Task 1',
            status=Task.TASK_STATUS.OPEN,
            due_date=datetime.datetime.now()
        )

    def tearDown(self):
        super(EditTaskTests, self).tearDown()
        Task.objects.all().delete()

    def get_task_data(self, **kwargs):
        task_data = {
            'title': 'New task',
            'description': 'test',
            'status': Task.TASK_STATUS.RESOLVED,
            'due_date': '10/29/2014',
        }
        task_data.update(kwargs)
        return task_data

    def test_edit_success(self):
        task_data = self.get_task_data()
        url = reverse('tasks:task_edit', args=(self.task.pk,))

        response = self.client.post(url, task_data)
        self.assertRedirects(response, self.task.get_absolute_url())
        task = Task.objects.first()
        self.assertObjectAttrs(
            task,
            title=task_data['title'],
            description=task_data['description'],
            status=task_data['status'],
            due_date=datetime.date(2014, 10, 29)
        )
