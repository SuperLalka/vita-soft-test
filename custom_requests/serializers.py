from django.contrib.auth.models import User

from rest_framework import serializers

from . import models
from .models import ExtendingUser


class RequestsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Requests
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        extending_user = ExtendingUser.objects.get(user=instance.id)
        for key in ExtendingUserSerializer(extending_user).data:
            representation[key] = ExtendingUserSerializer(extending_user).data[key]
        return representation


class ExtendingUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExtendingUser
        fields = ['is_user', 'is_operator', 'is_admin']
