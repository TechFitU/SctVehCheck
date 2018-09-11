from __future__ import unicode_literals

import uuid

import pytz
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import gettext_lazy as _


class BaseProfile(models.Model):
    CHOICES = [(v, v) for v in pytz.common_timezones]
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                primary_key=True)
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False, verbose_name=_("Slug"))
    # Add more user profile fields here. Make sure they are nullable
    # or with default values
    picture = models.ImageField(_('Profile picture'),
                                upload_to='profile_pics/%Y-%m-%d/',
                                null=True,
                                blank=True)
    bio = models.CharField(_("Short Biography"), max_length=200, blank=True, null=True)
    email_verified = models.BooleanField(_("Email verified"), default=False)
    timezone = models.CharField(_("Timezone"), max_length=45, default=settings.TIME_ZONE, \
                                choices=CHOICES)

    class Meta:
        abstract = True


from django.utils.text import format_lazy
@python_2_unicode_compatible
class Profile(BaseProfile):
    def __str__(self):
        return format_lazy("{}'s profile", self.user)
