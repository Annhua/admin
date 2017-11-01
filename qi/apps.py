from django.apps import AppConfig

from django.utils.module_loading import autodiscover_modules
class QiConfig(AppConfig):
    name = 'qi'
    def ready(self):

        autodiscover_modules('ninbin')

