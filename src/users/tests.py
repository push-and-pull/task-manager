from django.test import TestCase
from models import User
from forms import UserRegisterForm
from django.test import Client


class UserRegisterTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='user@mail.ru', password='secret')
        self.user = user

    def test_form_existing_email(self):
        c = Client()
        form = UserRegisterForm(instance=self.user)

        response = c.post('user/sign_in', {'email': self.user.email})

        self.assertFormError(response, 'form', 'email', 'User with this email already exists')

    def test_form_valid_data(self):
        initial_count = User.objects.count()
        c = Client()
        c.post('/user/sign_in', {'email': 'f123@mail.ru', 'password': '123',
                                 'confirm_password': '123'})
        self.assertEqual(User.objects.count(), initial_count + 1)
