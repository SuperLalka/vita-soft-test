from django.apps import AppConfig


class CustomRequestsConfig(AppConfig):
    name = 'custom_requests'

    def ready(self):
        from custom_requests import signals
