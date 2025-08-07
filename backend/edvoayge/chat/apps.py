from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    verbose_name = 'Chat - Messaging Platform'

    def ready(self):
        """Import signals when the app is ready"""
        try:
            import chat.signals
        except ImportError:
            pass
