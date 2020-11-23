from django.contrib.auth.models import User
from django.db import models


REQUESTS_STATUS_TEXT = 'Select requests status'
REQUESTS_STATUS = [
    ('drf', 'draft'),
    ('snt', 'sent'),
    ('acc', 'accepted'),
    ('rej', 'rejected')
]


class Requests(models.Model):
    text = models.CharField(max_length=100, help_text="Enter the text of your application")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=REQUESTS_STATUS, help_text=REQUESTS_STATUS_TEXT)

    def __str__(self):
        return '{0} /{1} /{2}'.format(self.user, self.creation_date, self.status)

    class Meta:
        verbose_name = 'User request'
        verbose_name_plural = 'User requests'
