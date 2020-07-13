from django.apps import AppConfig


class GdriveConfig(AppConfig):
    name = 'gdrive'

    def ready(self):
        import gdrive.signals
