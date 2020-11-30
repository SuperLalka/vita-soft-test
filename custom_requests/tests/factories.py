import factory
from datetime import datetime

from custom_requests import models


class UsersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Sequence(lambda n: 'user%d' % n)


class UserRolesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UserRoles

    role_name = 'usr'


class ExtendingUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ExtendingUser

    user = factory.SubFactory(UsersFactory)


class RequestsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Requests

    text = factory.Faker('text', max_nb_chars=50)
    user = factory.SubFactory(UsersFactory)
    status = 'drf'
    created_at = factory.LazyFunction(datetime.now)
