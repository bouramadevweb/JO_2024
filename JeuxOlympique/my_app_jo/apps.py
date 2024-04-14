from django.apps import AppConfig
from django_cron import CronJobManager


class MyAppJoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_app_jo'

    """_summary_
    """
    def ready(self):
        import  my_app_jo.signals
    # def ready(self):
    #     # Enregistrer votre tâche cron lorsque l'application est prête
    #         CronJobManager.register(UpdateCodeJob)    
