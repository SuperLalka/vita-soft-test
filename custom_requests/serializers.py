from django.contrib.auth.models import User

from rest_framework import serializers

from . import models


class HyphenSeparationField(serializers.CharField):
    def to_representation(self, value):
        return '-'.join(value)


class CustomerRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Requests
        fields = '__all__'

    def validate_status(self, value):
        if self.context['request'].user.extendinguser.check_group('usr') and \
                self.instance and value not in ['drf', 'snt']:
            raise serializers.ValidationError(
                "The user can change the status of his request only to 'sent'")
        return value

    def validate_user(self, value):
        raise serializers.ValidationError(
            "You cannot change the author of the request")


class OperatorRequestsSerializer(serializers.ModelSerializer):
    text = HyphenSeparationField()

    class Meta:
        model = models.Requests
        fields = '__all__'

    def validate_status(self, value):
        if self.context['request'].user.extendinguser.check_group('opr') and \
                value not in ['acc', 'rej']:
            raise serializers.ValidationError(
                "The operator can change the status of requests only to 'accepted' and 'rejected'")
        return value

    def validate_text(self, value):
        if self.context['request'].user.extendinguser.check_group('opr'):
            raise serializers.ValidationError(
                "The operator cannot change the text of user requests")
        return value


class UsersSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(max_length=3, required=False, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'role_name']

    def validate_role_name(self, value):
        if value != 'opr':
            raise serializers.ValidationError(
                "The administrator can only designate a user as an 'operator'")
        return self.instance.extendinguser.roles.all()

    def update(self, instance, validated_data):
        operator_role, _ = models.UserRoles.objects.get_or_create(role_name='opr')
        for x in validated_data['role_name']:
            if x.role_name == 'usr':
                instance.extendinguser.roles.clear()
        instance.extendinguser.roles.add(operator_role)
        return instance
