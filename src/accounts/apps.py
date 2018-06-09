from __future__ import unicode_literals
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "accounts"
    verbose_name = 'User Accounts'

    def ready(self):
        from . import signals   # noqa
