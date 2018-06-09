# -*- coding: utf-8 -*-
from django.apps import AppConfig

class VehicleCheckConfig(AppConfig):
    name = 'vehiclecheck'
    label = 'vehiclecheck'
    verbose_name = u"Verificación de vehículos"

    # def ready(self):
    # 	import paqueteria.signals