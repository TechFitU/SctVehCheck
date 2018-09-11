# -*- coding: utf-8 -*-
# Register your models here.
from globalconfig.models import SiteConfiguration
from solo.admin import SingletonModelAdmin
#from vehiclecheck.myadmin import admin_site
from django.contrib import admin
# from vehiclecheck.myadmin import admin_site
from django.contrib import admin
from globalconfig.models import SiteConfiguration
from solo.admin import SingletonModelAdmin

admin.site.register(SiteConfiguration, SingletonModelAdmin)
