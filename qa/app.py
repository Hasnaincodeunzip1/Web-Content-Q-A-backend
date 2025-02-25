from django.apps import AppConfig

class QaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qa'  # This should match the name of your app directory

    # You can add custom app-level configurations here, but for a simple
    # app like this, the defaults are usually fine.