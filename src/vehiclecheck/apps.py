# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext_lazy
class VehicleCheckConfig(AppConfig):
    name = 'vehiclecheck'
    label = 'vehiclecheck'
    verbose_name = gettext_lazy(u"Vehicle inspection")

    # def ready(self):
    # 	import paqueteria.signals