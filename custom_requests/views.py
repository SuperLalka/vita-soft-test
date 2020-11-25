from django.contrib.auth.models import User

from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from . import models, permissions, serializers


class RequestsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    permission_classes_by_action = {'create': [permissions.UserPermission],
                                    'retrieve': [permissions.OperatorPermission | permissions.UserPermission],
                                    'list': [permissions.OperatorPermission | permissions.UserPermission],
                                    'update': [permissions.UserPermission],
                                    'partial_update': [permissions.UserPermission],
                                    'destroy': []}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        if self.request.user.extendinguser.check_group('usr'):
            return models.Requests.objects.filter(user=self.request.user, status='drf')
        elif self.request.user.extendinguser.check_group('opr'):
            return models.Requests.objects.filter(status='snt')

    def get_serializer_class(self):
        if self.request.user.extendinguser.check_group('usr'):
            return serializers.RequestsForUserSerializer
        elif self.request.user.extendinguser.check_group('opr'):
            return serializers.RequestsForOperatorSerializer


class UsersViewSet(mixins.ListModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    serializer_class = serializers.UsersSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AdminPermission]

    def get_queryset(self):
        users_list = list(models.AssignedRoles.objects.filter(
            role__role_name='usr').values_list('user__user_id', flat=True))
        return models.User.objects.filter(id__in=users_list)
