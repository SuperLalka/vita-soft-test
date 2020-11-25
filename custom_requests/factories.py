import factory
from datetime import datetime

from . import models


class UsersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Faker('first_name')


class UserRolesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UserRoles

    role = 'usr'


class ExtendingUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ExtendingUser

    user = factory.SubFactory(UsersFactory)
    roles = factory.SubFactory(UserRolesFactory)


class RequestsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Requests

    text = factory.Faker('text', max_nb_chars=50)
    user = factory.SubFactory(UsersFactory)
    status = 'drf'
    created_at = factory.LazyFunction(datetime.now)
