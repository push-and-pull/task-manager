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
        User.objects.all().delete()
        Task.objects.all().delete()

    def test_anonymous_user_redirects_lo_login(self):
        self.client.logout()
        response = self.client.get(reverse('tasks:task_list'))
        self.assertRedirects(response, reverse('users:login') + '?next=/tasks/')

    def test_quries_count(self):
        with self.assertNumQueries(2):
            self.client.get(reverse('tasks:task_list'))

    def test_user_see_only_own_tasks(self):
        response = self.client.get(reverse('tasks:task_list'))
        self.assertNotContains(response, self.task3.title)


class CreateTaskTest(BaseTestCase):

    def setUp(self):
        super(CreateTaskTest, self).setUp()

    def tearDown(self):
        super(CreateTaskTest, self).tearDown()
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
