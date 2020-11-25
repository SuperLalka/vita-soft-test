from django.test import TestCase
from rest_framework.test import APIClient
from hamcrest import *

from . import models
from .factories import (
    UsersFactory,
    UserRolesFactory,
    ExtendingUserFactory,
    RequestsFactory
)


class RequestsApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.test_user = UsersFactory()
        self.test_request = RequestsFactory(user=self.test_user)

    def test_get_request(self):
        response = self.client.get(f'/api/requests/{self.test_request.id}/')
        self.assertEqual(response.status_code, 200)
        assert_that(response.json(), has_entries({
            'id': self.test_request.id,
            'text': self.test_request.text,
            'user': self.test_user.id
        }))

    def test_get_requests_list(self):
        RequestsFactory()
        response = self.client.get('/api/requests/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_create_request(self):
        response = self.client.post('/api/requests/',
                                    {'text': 'new_test_request_text'},
                                    follow=True)
        self.assertEqual(response.status_code, 201)
        assert_that(response.json(), has_entries({
            'id': 2,
            'text': 'new_test_request_text'
        }))

    def test_update_request(self):
        response = self.client.patch(f'/api/requests/{self.test_request.id}/',
                                     {'id': self.test_request.id, 'text': 'renew_text'},
                                     follow=True)
        self.assertEqual(response.status_code, 200)
        self.test_request.refresh_from_db()
        self.assertEqual(self.test_request.text, 'renew_text')

    def test_delete_request(self):
        response = self.client.delete(f'/api/requests/{self.test_request.id}/', follow=True)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(models.Requests.objects.filter(id=self.test_request.id).exists())


class UsersApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.test_user = UsersFactory()

    def test_get_user(self):
        response = self.client.get(f'/api/users/{self.test_user.id}/', follow=True)
        self.assertEqual(response.status_code, 200)
        assert_that(response.json(), has_entries({
            'id': self.test_user.id,
            'username': self.test_user.username
        }))

    def test_get_users_list(self):
        UsersFactory()
        response = self.client.get('/api/users/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_create_user(self):
        response = self.client.post('/api/users/',
                                    {'username': 'new_user', 'password': '123456ww'},
                                    follow=True)
        self.assertEqual(response.status_code, 201)
        assert_that(response.json(), has_entries({
            'id': self.test_user.id + 1,
            'username': 'new_user'
        }))

    def test_update_user(self):
        response = self.client.patch(f'/api/users/{self.test_user.id}/',
                                     {'id': self.test_user.id, 'username': 'new_name'},
                                     follow=True)
        self.assertEqual(response.status_code, 200)
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.username, 'new_name')

    def test_delete_user(self):
        response = self.client.delete(f'/api/users/{self.test_user.id}/', follow=True)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(models.User.objects.filter(id=self.test_user.id).exists())
