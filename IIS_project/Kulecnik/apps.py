from django.apps import AppConfig



class KulecnikConfig(AppConfig):
    name = 'Kulecnik'
    def ready(self):
        import Kulecnik.signals