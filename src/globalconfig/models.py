# -*- coding: utf-8 -*-
from django.db import models
from django.utils.text import gettext_lazy
from solo.models import SingletonModel


# Create your models here.
class SiteConfiguration(SingletonModel):
    nombre_sitio = models.CharField(gettext_lazy("Site name"), max_length=255, default='www.pepito.com')
    empresa = models.CharField(gettext_lazy("Company name"), max_length=255, default=gettext_lazy('Company X'))
    mode_mantenimiento = models.BooleanField(gettext_lazy("Maintenance mode"), default=False)
    no_aprobacion = models.CharField(gettext_lazy(u"Approval No."), default="UV/SCT/CFM/14/016", max_length=25)
    no_acreditacion = models.CharField(gettext_lazy(u"Accreditation No."), default="UVSCTAT016", max_length=25)

    def __str__(self):
        return gettext_lazy(u"Company %(company)s hosted in %(site_name)s") % {'company': self.empresa,
                                                                               'site_name': self.nombre_sitio}

    class Meta:
        verbose_name = gettext_lazy(u"Company settings")
