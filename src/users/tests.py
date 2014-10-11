from django.test import TestCase
from models import User
from forms import UserRegisterForm, UserLoginForm
from django.core.urlresolvers import reverse


class UserRegisterTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='user@mail.ru', password='secret')
        self.user = user
        self.data_for_existing_user = {'email': self.user.email, 'password': 'pass', 'confirm_password': 'pass'}
        self.data_for_password_ne_confirm = {'email': 'some@email.com', 'password': 'pass', 'confirm_password': 'other'}
        self.data_valid = {'email': 'some@email.com', 'password': 'pass', 'confirm_password': 'pass'}

    def tearDown(self):
        user = self.user
        user.delete()

    def test_request_form_existing_email(self):
        response = self.client.post(reverse('users:sign_up'), self.data_for_existing_user)
        self.assertFormError(response, 'form', 'email', 'User with this email already exists')

    def test_form_existing_email(self):
        form = UserRegisterForm(data=self.data_for_existing_user)
        self.assertIn('User with this email already exists', form.errors['email'])

    def test_form_confirm_password_is_not_equal_to_password(self):
        form = UserRegisterForm(data=self.data_for_password_ne_confirm)
        self.assertIn('Password and Confirm password should be equal', form.errors['__all__'])

    def tests_form_validates_valid_data(self):
        form = UserRegisterForm(data=self.data_valid)
        self.assertTrue(form.is_valid())

    def test_form_valid_data_adds_user(self):
        initial_count = User.objects.count()
        self.client.post(reverse('users:sign_up'), self.data_valid)
        self.assertEqual(User.objects.count(), initial_count + 1)

    def test_form_valid_data_redirects_to_tasks_page(self):
        response = self.client.post(reverse('users:sign_up'), self.data_valid)
        #fixme redirect should be tested not in that cheated way.
        self.assertIn('/tasks', response.url)


class UserLogInTestCase(TestCase):
    def setUp(self):
        self.valid_data = {'email': 'user@email.com', 'password': 'secret'}
        self.user = User.objects.create(**self.valid_data)
        self.wrong_password_user = {'email': self.user.email, 'password': 'some'}
        self.not_existing_user = {'email': 'some@email.com', 'password': 'some'}

    def tearDown(self):
        self.user.delete()
        self.client.logout()

    def test_form_validates_valid_data(self):
        form = UserLoginForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_user_with_valid_data_is_logged_in(self):
        self.client.post(reverse('users:login'), data=self.valid_data)
        self.assertEqual(self.client.session['_auth_user_id'], self.user.pk)

    def test_not_existing_user_not_logged_in(self):
        form = UserLoginForm(data=self.not_existing_user)
        self.assertFalse(form.is_valid())

    def test_user_with_wrong_password(self):
        self.client.post(reverse('users:login'), data=self.wrong_password_user)
        self.assertEqual(self.client.session.get('_auth_user_id', 'No user here'), 'No user here')


class UserLogoutTestCase(TestCase):
    def setUp(self):
        self.valid_data = dict(email='user@mail.ru', password='secret')
        user = User.objects.create_user(**self.valid_data)
        self.user = user
        self.client.post(reverse('users:login'), data=self.valid_data)
    
    def tearDown(self):
        self.user.delete()

    def test_user_logout(self):
        user_id_before = self.client.session.get('_auth_user_id', 'No user here')
        self.client.get(reverse('users:logout'))
        user_id_after = self.client.session.get('_auth_user_id', 'No user here')
        self.assertNotEqual(user_id_before, user_id_after)
