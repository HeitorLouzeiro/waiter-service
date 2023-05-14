from django.apps import AppConfig


class WaiterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'waiter'

    def ready(self):
        import waiter.signals  # noqa
