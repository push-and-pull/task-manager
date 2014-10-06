# coding: utf-8

from django import forms
from django.core.exceptions import ValidationError
from models import User


class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password", "confirm_password")
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            User.objects.get(email=data)
        except User.DoesNotExist:
            return data
        else:
            raise forms.ValidationError('User with this email already exists')

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Password and Confirm password should be equal')


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "password")
        widgets = {'password': forms.PasswordInput()}

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            User.objects.get(email=data)
        except User.DoesNotExist:
            raise forms.ValidationError('User with this email does not exist')
        else:
            return data

    def clean(self):
        data = self.cleaned_data
        return data

