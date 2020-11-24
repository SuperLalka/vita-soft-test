from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from . import models


@receiver(post_save, sender=User)
def create_extending_user(instance, **kwargs):
    extending_user, _ = models.ExtendingUser.objects.get_or_create(user_id=instance.id)
    extending_user.save()
