from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from . import models


@receiver(post_save, sender=User)
def create_extending_user(instance, **kwargs):
    if not models.ExtendingUser.objects.filter(user_id=instance.id).exists():
        extending_user = models.ExtendingUser.objects.create(user_id=instance.id)
        extending_user.save()
        role, _ = models.UserRoles.objects.get_or_create(role_name='usr')
        user_role, _ = models.AssignedRoles.objects.get_or_create(
            user_id=extending_user.id, role=role)
        user_role.save()
