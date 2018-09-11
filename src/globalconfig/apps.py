# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.text import gettext_lazy


class GlobalConfig(AppConfig):
    name = 'globalconfig'
    label = 'globalconfig'
    verbose_name = gettext_lazy(u"Global settings")

    # def ready(self):
    # 	import paqueteria.signals