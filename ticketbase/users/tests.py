from random import randint

from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .users.models import User


def create_test_user_client(**user_data):
    user_data.update({
        "username": "tester%s" % randint(1, 999999),
        "first_name": "tester%s" % randint(1, 999999),
        "email": "tester%s@test.com" % randint(1, 999999)
    })
    user = User.objects.create(**user_data)
    Token.objects.create(user=user)

    client = APIClient()
    client.default_format = 'json'
    client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)

    return client, user



class SimpleTestCase(TestCase):
    """
    A simple test that logs in to the admin panel.
    """
    def setUp(self):
        self.client, self.user = create_test_user_client()
        self.user.is_staff = True
        self.user.is_superuser = True
        self.password = '123456'
        self.user.set_password(self.password)
        self.user.save()

    def test_login(self):
        self.client.login(username=self.user.username, password=self.password)
        resp = self.client.get('/admin/auth/')
        self.assertEqual(resp.status_code, 200)

