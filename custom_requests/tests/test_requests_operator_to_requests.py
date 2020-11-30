from django.test import TestCase
from rest_framework.test import APIClient
from hamcrest import *

from custom_requests.tests.factories import (
    UsersFactory,
    UserRolesFactory,
    RequestsFactory
)


class RequestsApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        operator_role = UserRolesFactory(role_name='opr')
        self.user = UsersFactory()
        self.user.extendinguser.roles.clear()
        self.user.extendinguser.roles.add(operator_role)
        self.client.force_authenticate(user=self.user)

        self.request_in_drf = RequestsFactory()
        self.request_in_snt = RequestsFactory(status='snt')

    def test_get_request_in_drf(self):
        response = self.client.get(f'/api/requests/{self.request_in_drf.id}/')
        self.assertEqual(response.status_code, 404)

    def test_get_request_in_snt(self):
        response = self.client.get(f'/api/requests/{self.request_in_snt.id}/')
        self.assertEqual(response.status_code, 200)
        assert_that(response.json(), has_entries({
            'id': self.request_in_snt.id,
            'text': '-'.join(self.request_in_snt.text)
        }))

    def test_get_requests_list(self):
        second_snt_request = RequestsFactory(status='snt')
        response = self.client.get('/api/requests/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

        assert_that(response.json(), contains_inanyorder(
            has_entries(id=second_snt_request.id, text='-'.join(second_snt_request.text)),
            has_entries(id=self.request_in_snt.id, text='-'.join(self.request_in_snt.text)),
        ))

    def test_create_request(self):
        response = self.client.post('/api/requests/',
                                    {'text': 'new_test_request_text'},
                                    follow=True)
        self.assertEqual(response.status_code, 403)

    def test_update_request_text(self):
        response = self.client.patch(f'/api/requests/{self.request_in_snt.id}/',
                                     {'text': 'renew_text'},
                                     follow=True)
        self.assertEqual(response.status_code, 400)

    def test_update_request_status(self):
        response = self.client.patch(f'/api/requests/{self.request_in_snt.id}/',
                                     {'status': 'acc'},
                                     follow=True)
        self.assertEqual(response.status_code, 200)
        self.request_in_drf.refresh_from_db()
        assert_that(response.json(), has_entries({
            'id': self.request_in_snt.id,
            'status': 'acc'
        }))

    def test_delete_request(self):
        response = self.client.delete(f'/api/requests/{self.request_in_snt.id}/', follow=True)
        self.assertEqual(response.status_code, 403)
