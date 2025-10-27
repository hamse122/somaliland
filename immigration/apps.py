from django.apps import AppConfig


class ImmigrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'immigration'
    
    def ready(self):
        """Import signals when app is ready."""
        import immigration.signals  # noqa