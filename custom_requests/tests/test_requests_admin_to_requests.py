from django.test import TestCase
from rest_framework.test import APIClient

from custom_requests.factories import (
    UsersFactory,
    UserRolesFactory,
    RequestsFactory,
)


class RequestsApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        admin_role = UserRolesFactory(role_name='adm')
        self.user = UsersFactory()
        self.user.extendinguser.roles.clear()
        self.user.extendinguser.roles.add(admin_role)
        self.client.force_authenticate(user=self.user)

        self.request = RequestsFactory()

    def test_get_request(self):
        response = self.client.get(f'/api/requests/{self.request.id}/', follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_requests_list(self):
        RequestsFactory()
        response = self.client.get('/api/requests/', follow=True)
        self.assertEqual(response.status_code, 403)

    def test_create_request(self):
        response = self.client.post('/api/requests/',
                                    {'text': 'new_test_request_text'},
                                    follow=True)
        self.assertEqual(response.status_code, 403)

    def test_update_request(self):
        response = self.client.patch(f'/api/requests/{self.request.id}/',
                                     {'id': self.request.id, 'text': 'renew_text'},
                                     follow=True)
        self.assertEqual(response.status_code, 403)

    def test_delete_request(self):
        response = self.client.delete(f'/api/requests/{self.request.id}/', follow=True)
        self.assertEqual(response.status_code, 403)
