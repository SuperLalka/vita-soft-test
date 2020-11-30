from django.test import TestCase
from rest_framework.test import APIClient

from custom_requests.tests.factories import (
    UsersFactory,
    RequestsFactory
)


class RequestsApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.test_user = UsersFactory()
        self.test_request = RequestsFactory(user=self.test_user)

    def test_get_request(self):
        response = self.client.get(f'/api/requests/{self.test_request.id}/')
        self.assertEqual(response.status_code, 401)

    def test_get_requests_list(self):
        RequestsFactory()
        response = self.client.get('/api/requests/', follow=True)
        self.assertEqual(response.status_code, 401)

    def test_create_request(self):
        response = self.client.post('/api/requests/',
                                    {'text': 'new_test_request_text'},
                                    follow=True)
        self.assertEqual(response.status_code, 401)

    def test_update_request(self):
        response = self.client.patch(f'/api/requests/{self.test_request.id}/',
                                     {'id': self.test_request.id, 'text': 'renew_text'},
                                     follow=True)
        self.assertEqual(response.status_code, 401)

    def test_delete_request(self):
        response = self.client.delete(f'/api/requests/{self.test_request.id}/', follow=True)
        self.assertEqual(response.status_code, 401)
