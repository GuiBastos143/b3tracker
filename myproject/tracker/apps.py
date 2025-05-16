from django.apps import AppConfig


class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'
    def ready(self):
        from .models import Asset
        Asset.objects.all().delete()