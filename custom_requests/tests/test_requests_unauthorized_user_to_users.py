from django.test import TestCase
from rest_framework.test import APIClient

from custom_requests.factories import (
    UsersFactory
)


class UsersApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.test_user = UsersFactory()

    def test_get_user(self):
        response = self.client.get(f'/api/users/{self.test_user.id}/', follow=True)
        self.assertEqual(response.status_code, 401)

    def test_get_users_list(self):
        UsersFactory()
        response = self.client.get('/api/users/', follow=True)
        self.assertEqual(response.status_code, 401)

    def test_create_user(self):
        response = self.client.post('/api/users/',
                                    {'username': 'new_user', 'password': '123456ww'},
                                    follow=True)
        self.assertEqual(response.status_code, 401)

    def test_update_user(self):
        response = self.client.patch(f'/api/users/{self.test_user.id}/',
                                     {'username': 'new_name'},
                                     follow=True)
        self.assertEqual(response.status_code, 401)

    def test_delete_user(self):
        response = self.client.delete(f'/api/users/{self.test_user.id}/', follow=True)
        self.assertEqual(response.status_code, 401)
