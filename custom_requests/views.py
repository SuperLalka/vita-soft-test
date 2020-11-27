from rest_framework import viewsets, mixins
from rest_framework import permissions as drf_permissions
from rest_framework.viewsets import GenericViewSet

from . import models, permissions, serializers


class RequestsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    permission_classes = [drf_permissions.IsAuthenticated]
    permission_classes_by_action = {
        'create': [permissions.UserPermission],
        'retrieve': [permissions.OperatorPermission | permissions.UserPermission],
        'list': [permissions.OperatorPermission | permissions.UserPermission],
        'update': [permissions.OperatorPermission | permissions.UserPermission],
        'partial_update': [permissions.OperatorPermission | permissions.UserPermission],
        'destroy': [drf_permissions.IsAdminUser]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        if self.request.user.extendinguser.check_group('opr'):
            return models.Requests.objects.filter(status='snt')
        return models.Requests.objects.filter(user=self.request.user, status='drf')

    def get_serializer_class(self):
        if self.request.user.extendinguser.check_group('opr'):
            return serializers.OperatorRequestsSerializer
        return serializers.CustomerRequestsSerializer


class UsersViewSet(mixins.ListModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    serializer_class = serializers.UsersSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AdminPermission]

    def get_queryset(self):
        role, _ = models.UserRoles.objects.get_or_create(role_name='usr')
        users_list = list(models.ExtendingUser.objects.filter(roles=role).
                          values_list('user__id', flat=True))
        return models.User.objects.filter(id__in=users_list)
