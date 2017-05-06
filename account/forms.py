import re

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    def clean(self):
        form_data = self.cleaned_data

        try:
            form_data['username'] = form_data['username'].lower()
            user = authenticate(
                username=form_data['username'],
                password=form_data['password'],
            )
        except KeyError:
            raise ValidationError({'password': 'All fields are required'}, code='required')

        if not user:
            try:
                inactive_user = User.objects.get(username=form_data['username'])
                if inactive_user.check_password(form_data['password']):
                    raise ValidationError({'password': 'Account disabled'}, code='invalid')
            except User.DoesNotExist:
                pass

            raise ValidationError({'password': 'Wrong password'}, code='invalid')

        return form_data


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, error_messages={'required': 'All fields are required'})
    confirm = forms.CharField(max_length=100)

    def clean(self):
        form_data = self.cleaned_data

        try:
            form_data['username'] = form_data['username'].lower()

            try:
                User.objects.get(username=form_data['username'])
                raise ValidationError({'password': 'Username taken'}, code='invalid')
            except User.DoesNotExist:
                pass

            if not re.match('^[A-Za-z]*$', form_data['username']):
                raise ValidationError({'password': 'Invalid username'}, code='invalid')

            if form_data['password'] != form_data['confirm']:
                raise ValidationError({'password': "Passwords don't match"}, code='invalid')
        except KeyError:
            raise ValidationError({'password': 'All fields are required'}, code='required')

        return form_data

    def save(self, request):
        return User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
        )
