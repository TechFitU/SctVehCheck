# -*- coding: utf-8 -*-
from django.db import models
from solo.models import SingletonModel
# Create your models here.
class SiteConfiguration(SingletonModel):
    nombre_sitio = models.CharField("Nombre del sitio",max_length=255, default='Nombre del sistema o sitio')
    empresa = models.CharField("Nombre de la empresa", max_length=255, default='Nombre empresa')
    mode_mantenimiento = models.BooleanField("Modo mantenimiento",default=False)
    no_aprobacion = models.CharField(u"No. Aprobación", default="UV/SCT/CFM/14/016", max_length=25)
    no_acreditacion = models.CharField(u"No. Acreditación", default="UVSCTAT016", max_length=25)

    def __str__(self):
        return u"Configuración del sistema"

    class Meta:
        verbose_name = u"Sistema"
