from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from .views import Login, Register, Logout, Account


class ViewTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='user', password='pass')
        self.client = Client()

    def test_account_page_without_login(self):
        response = self.client.get('/account/account/', follow=True)
        self.assertEqual(response.redirect_chain[-1][0], Account.login_url + '?next=/account/account/')

    def test_account_page_with_login(self):
        self.client.login(username='user', password='pass')
        response = self.client.get('/account/account/')
        self.assertEqual(response.status_code, 200)

class AuthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.client = Client()

    # -------------------------------- #
    #           Login
    # -------------------------------- #

    def assertLogin(self):
        response = self.client.get('/')
        self.assertEqual(response.context['user'].is_authenticated, True)

    def assertNotLogin(self):
        response = self.client.get('/')
        self.assertEqual(response.context['user'].is_authenticated, False)

    def test_login_correct(self):
        response = self.client.post('/account/login/', {'username': 'user', 'password': 'pass'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, Login.success_url)
        self.assertLogin()

    def test_login_account_disabled(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post('/account/login/', {'username': 'user', 'password': 'pass'})
        self.assertEqual(response.status_code, 200)
        self.assertNotLogin()

    def test_login_wrong_password(self):
        response = self.client.post('/account/login/', {'username': 'user', 'password': '1234'})
        self.assertEqual(response.status_code, 200)
        self.assertNotLogin()

    def test_login_unknown_username(self):
        response = self.client.post('/account/login/', {'username': 'unknown', 'password': 'pass'})
        self.assertEqual(response.status_code, 200)
        self.assertNotLogin()

    def test_login_without_data(self):
        response = self.client.post('/account/login/')
        self.assertEqual(response.status_code, 200)
        self.assertNotLogin()

    # -------------------------------- #
    #           Register
    # -------------------------------- #

    def test_register_correct(self):
        response = self.client.post('/account/register/', {'username': 'usertwo', 'password': 'pass', 'confirm': 'pass'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, Register.success_url)
        self.assertLogin()

    def test_register_invalid_username(self):
        response = self.client.post('/account/register/', {'username': 'user_two', 'password': 'pass', 'confirm': 'pass'})
        self.assertEqual(response.status_code, 200)
        self.assertNotLogin()

    def test_register_username_taken(self):
        response = self.client.post('/account/register/', {'username': 'user', 'password': 'pass', 'confirm': 'pass'})
        self.assertEqual(response.status_code, 200)
        self.assertNotLogin()

    def test_register_passwords_dont_match(self):
        response = self.client.post('/account/register/', {'username': 'usertwo', 'password': 'pass', 'confirm': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertNotLogin()

    def test_register_without_data(self):
        response = self.client.post('/account/register/')
        self.assertEqual(response.status_code, 200)
        self.assertNotLogin()

    # -------------------------------- #
    #           Logout
    # -------------------------------- #

    def test_logout(self):
        self.client.login(username='user', password='pass')
        response = self.client.get('/account/logout', follow=True)
        self.assertEqual(response.redirect_chain[-1][0], Logout.success_url)
        self.assertNotLogin()

    def test_logout_whithout_login(self):
        response = self.client.get('/account/logout', follow=True)
        self.assertEqual(response.redirect_chain[-1][0], Logout.success_url)
        self.assertNotLogin()