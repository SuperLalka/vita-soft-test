from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.response import Response

from . import models, permissions, serializers


class RequestsViewSet(viewsets.ModelViewSet):
    queryset = models.Requests.objects.all()
    serializer_class = serializers.RequestsSerializer
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

    def create(self, request, *args, **kwargs):
        request.data['status'] = 'drf'
        request.data['user'] = request.user.id
        return super(RequestsViewSet, self).create(request)

    def list(self, request, *args, **kwargs):
        if request.user.extendinguser.is_user:
            queryset = models.Requests.objects.filter(user_id=request.user.id, status='drf')
        else:
            queryset = models.Requests.objects.filter(status='snt')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        if (request.user.extendinguser.is_user and instance.user_id == request.user.id or
                request.user.extendinguser.is_operator and instance.status == 'snt'):
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        if request.user.extendinguser.is_user:
            return Response("Нельзя просматривать чужие заявки")
        return Response("Статус заявки не 'отправлено'")

    def update(self, request, pk=None, *args, **kwargs):
        if request.user.extendinguser.is_user:
            data = {'text': request.data['text']}
        else:
            data = {'status': request.data['status']}

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UsersSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AdminPermission]
