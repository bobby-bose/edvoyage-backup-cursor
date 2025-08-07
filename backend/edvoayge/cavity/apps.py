from django.apps import AppConfig


class CavityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cavity'
    verbose_name = 'Cavity - Social Platform'

    def ready(self):
        """Import signals when the app is ready"""
        try:
            import cavity.signals
        except ImportError:
            pass
