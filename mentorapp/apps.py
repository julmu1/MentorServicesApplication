from django.apps import AppConfig


class MentorappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mentorapp'
    
    def ready(self):
        import mentorapp.signals 
