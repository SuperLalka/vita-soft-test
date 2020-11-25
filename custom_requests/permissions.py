from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and
                    request.user.extendinguser.check_group('usr'))


class OperatorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and
                    request.user.extendinguser.check_group('opr'))


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and
                    request.user.extendinguser.check_group('adm'))
