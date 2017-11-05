from django.apps import AppConfig


class WdcMainConfig(AppConfig):
    name = 'wdc_main'

    def ready(self):
        import wdc_main.receivers
