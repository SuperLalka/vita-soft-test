from django.test import TestCase
from rest_framework.test import APIClient

from custom_requests.factories import (
    UsersFactory,
    UserRolesFactory
)


class UsersApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        admin_role = UserRolesFactory(role_name='adm')
        self.user = UsersFactory()
        self.user.extendinguser.roles.clear()
        self.user.extendinguser.roles.add(admin_role)
        self.client.force_authenticate(user=self.user)

        self.consumer = UsersFactory()

    def test_get_user(self):
        response = self.client.get(f'/api/users/{self.consumer.id}/', follow=True)
        self.assertEqual(response.status_code, 405)

    def test_get_users_list(self):
        response = self.client.get('/api/users/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_create_user(self):
        response = self.client.post('/api/users/',
                                    {'username': 'new_user', 'password': '123456ww'},
                                    follow=True)
        self.assertEqual(response.status_code, 405)

    def test_update_users_username(self):
        response = self.client.patch(f'/api/users/{self.consumer.id}/',
                                     {'username': 'new_name', 'role_name': 'opr'},
                                     follow=True)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertNotEqual(self.consumer.username, 'new_name')

    def test_update_users_status_to_adm(self):
        response = self.client.patch(f'/api/users/{self.consumer.id}/',
                                     {'role_name': 'adm'},
                                     follow=True)
        self.assertEqual(response.status_code, 400)

    def test_update_users_status_to_opr(self):
        response = self.client.patch(f'/api/users/{self.consumer.id}/',
                                     {'role_name': 'opr'},
                                     follow=True)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.consumer.extendinguser.check_group('opr'), True)

    def test_delete_user(self):
        response = self.client.delete(f'/api/users/{self.consumer.id}/', follow=True)
        self.assertEqual(response.status_code, 405)
