from django.test import TestCase
from models import User
from forms import UserRegisterForm
# Create your tests here.


class UserRegisterTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(email='user@mail.ru', password='secret')

    def test_form_existing_email(self):
        user = User.objects.get()
        form_data = {'email': user.email, 'password': '123', 'confirm_password': '123'}
        print user.email
        response = UserRegisterForm(data=form_data)
        self.assertFormError(response, 'form', 'something', 'This field is required.')