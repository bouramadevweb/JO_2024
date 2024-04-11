from django.apps import AppConfig


class MyAppJoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_app_jo'

    """_summary_
    """
    def ready(self):
        import  my_app_jo.signals
