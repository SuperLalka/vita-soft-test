from django.test import TestCase
from rest_framework.test import APIClient
from hamcrest import *

from custom_requests.factories import (
    UsersFactory,
    UserRolesFactory,
    RequestsFactory
)


class RequestsApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        consumer_role = UserRolesFactory()
        self.user = UsersFactory()
        self.user.extendinguser.roles.add(consumer_role)
        self.client.force_authenticate(user=self.user)

        self.consumers_request_in_drf = RequestsFactory(status='drf', user=self.user)
        self.consumers_request_in_snt = RequestsFactory(status='snt', user=self.user)
        self.request_in_drf = RequestsFactory(status='drf')

    def test_get_consumers_request_in_drf(self):
        response = self.client.get(f'/api/requests/{self.consumers_request_in_drf.id}/')
        self.assertEqual(response.status_code, 200)
        assert_that(response.json(), has_entries({
            'id': self.consumers_request_in_drf.id,
            'text': self.consumers_request_in_drf.text
        }))

    def test_get_consumers_request_in_snt(self):
        response = self.client.get(f'/api/requests/{self.consumers_request_in_snt.id}/')
        self.assertEqual(response.status_code, 404)

    def test_get_not_consumers_request_in_drf(self):
        RequestsFactory(status='drf')
        response = self.client.get(f'/api/requests/{self.request_in_drf.id}/')
        self.assertEqual(response.status_code, 404)

    def test_get_requests_list(self):
        [RequestsFactory(status='drf', user=self.user) for x in range(0, 3)]
        response = self.client.get('/api/requests/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    def test_create_request(self):
        response = self.client.post('/api/requests/',
                                    {'text': 'new_test_request_text'},
                                    follow=True)
        self.assertEqual(response.status_code, 201)
        assert_that(response.json(), has_entries({
            'text': 'new_test_request_text'
        }))

    def test_update_request_text(self):
        response = self.client.patch(f'/api/requests/{self.consumers_request_in_drf.id}/',
                                     {'text': 'renew_text'},
                                     follow=True)
        self.assertEqual(response.status_code, 200)
        assert_that(response.json(), has_entries({
            'id': self.consumers_request_in_drf.id,
            'text': 'renew_text'
        }))

    def test_update_request_status(self):
        response = self.client.patch(f'/api/requests/{self.consumers_request_in_drf.id}/',
                                     {'status': 'snt'},
                                     follow=True)
        self.assertEqual(response.status_code, 200)
        self.request_in_drf.refresh_from_db()
        assert_that(response.json(), has_entries({
            'id': self.consumers_request_in_drf.id,
            'status': 'snt'
        }))

    def test_delete_request(self):
        response = self.client.delete(f'/api/requests/{self.consumers_request_in_drf.id}/', follow=True)
        self.assertEqual(response.status_code, 403)
