from django.conf import settings as django_settings
from django.contrib.auth.models import User
from django.db import models

from vita_soft import constants

REQUESTS_STATUS_TEXT = 'Select requests status'
USER_ROLES_TEXT = 'Select user role'


class Requests(models.Model):
    text = models.CharField(max_length=100, help_text="Enter the text of your application")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=constants.REQUESTS_STATUS,
                              help_text=REQUESTS_STATUS_TEXT, default='drf')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return '{0} /{1} /{2}'.format(self.user, self.created_at, self.status)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'User request'
        verbose_name_plural = 'User requests'


class ExtendingUser(models.Model):
    user = models.OneToOneField(django_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    roles = models.ManyToManyField('UserRoles')

    def __str__(self):
        return 'Extending info for user {}'.format(self.user.username)

    def check_group(self, group):
        user_roles = list(self.roles.values_list('role_name', flat=True))
        return group in user_roles

    class Meta:
        ordering = ['user']
        verbose_name = 'Extending User info'
        verbose_name_plural = 'Extending User info'


class UserRoles(models.Model):
    role_name = models.CharField(max_length=20, choices=constants.USER_ROLES,
                                 help_text=USER_ROLES_TEXT,
                                 default='usr')

    def __str__(self):
        return self.role_name

    class Meta:
        ordering = ['id']
        verbose_name = 'User role'
        verbose_name_plural = 'User roles'
