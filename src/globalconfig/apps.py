# -*- coding: utf-8 -*-
from django.apps import AppConfig

class GlobalConfig(AppConfig):
    name = 'globalconfig'
    label = 'globalconfig'
    verbose_name = u"Configuración global"

    # def ready(self):
    # 	import paqueteria.signals