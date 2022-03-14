from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self):
        from website.core.signals import init as init_signals
        from website.core.tasks import start_processing_tasks_in_background
        init_signals()
        start_processing_tasks_in_background()
