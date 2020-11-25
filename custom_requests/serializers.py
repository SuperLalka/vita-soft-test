from django.contrib.auth.models import User

from rest_framework import serializers

from . import models


class RequestsForUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Requests
        fields = '__all__'
        # read_only_fields = ['user', 'status', 'created_at']

    def validate_status(self, value):
        if self.instance:
            raise serializers.ValidationError("The user cannot change the status of his request")
        return value

    def validate_user(self, value):
        raise serializers.ValidationError("You cannot change the author of the request")


class RequestsForOperatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Requests
        fields = '__all__'
        # read_only_fields = ['user', 'text', 'created_at']

    def validate_text(self, value):
        raise serializers.ValidationError("The operator cannot change the text of user requests")

    def validate_status(self, value):
        if value == 'drf':
            raise serializers.ValidationError("The operator can only accept or reject user requests")
        return value

    def validate_user(self, value):
        raise serializers.ValidationError("You cannot change the author of the request")


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
