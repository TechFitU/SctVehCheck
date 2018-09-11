from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

from .models import Role

admin.site.unregister(Group)
admin.site.register(Role, GroupAdmin)
