# Create your models here.
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _


class Role(Group):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = _('Role')
